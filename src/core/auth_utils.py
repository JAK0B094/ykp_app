"""Authentication Utilities: Password hashing, rate limiting, middleware"""
import bcrypt
from functools import wraps
from flask import request, jsonify
from time import time
from src.core.token_manager import TokenManager
from src.core.jwt_config import LOGIN_RATE_LIMIT, REFRESH_RATE_LIMIT


# Rate limit storage (production'da Redis kullan)
_rate_limits = {}


class PasswordManager:
    """Secure password hashing with bcrypt"""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Şifre hash'le (bcrypt)
        
        Args:
            password: Plain text şifre
            
        Returns:
            str: Hashed password
        """
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Şifre doğrula
        
        Args:
            password: Plain text şifre
            hashed: Hash'lenmiş şifre
            
        Returns:
            bool: Doğru mu?
        """
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        except Exception:
            return False


class RateLimiter:
    """Rate limiting decorator"""

    @staticmethod
    def _check_rate_limit(key: str, limit: int, window: int = 60) -> bool:
        """
        Rate limit kontrol
        
        Args:
            key: Rate limit anahtarı (e.g., "login:192.168.1.1")
            limit: İzin verilen request sayısı
            window: Zaman penceresi (saniye)
            
        Returns:
            bool: Limit aşıldı mı?
        """
        global _rate_limits
        now = time()
        
        if key not in _rate_limits:
            _rate_limits[key] = []
        
        # Pencere dışı request'leri temizle
        _rate_limits[key] = [t for t in _rate_limits[key] if now - t < window]
        
        if len(_rate_limits[key]) >= limit:
            return False
        
        _rate_limits[key].append(now)
        return True

    @staticmethod
    def login_limit(f):
        """Login rate limiting decorator"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            key = f"login:{ip}"
            
            if not RateLimiter._check_rate_limit(key, LOGIN_RATE_LIMIT):
                return jsonify({
                    "error": "Çok fazla login denemesi. Lütfen 1 dakika sonra tekrar deneyin."
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def refresh_limit(f):
        """Token refresh rate limiting decorator"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip = request.remote_addr
            key = f"refresh:{ip}"
            
            if not RateLimiter._check_rate_limit(key, REFRESH_RATE_LIMIT):
                return jsonify({
                    "error": "Çok fazla refresh request'i. Lütfen biraz bekleyin."
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function


class AuthMiddleware:
    """JWT authentication middleware"""

    @staticmethod
    def require_auth(f):
        """
        Protected endpoint decorator
        Authorization: Bearer <token> header'ı kontrol eder
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            
            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing or invalid Authorization header"}), 401
            
            token = auth_header.split(" ", 1)[1]
            user_info = TokenManager.get_user_from_token(token)
            
            if not user_info:
                return jsonify({"error": "Invalid or expired token"}), 401
            
            # Token'dan user info'yu request context'e ekle
            request.user_id = user_info["user_id"]
            request.username = user_info["username"]
            
            return f(*args, **kwargs)
        return decorated_function


class TokenBlacklist:
    """Logout için token blacklist (production'da Redis kullan)"""
    
    _blacklist = set()
    
    @classmethod
    def add_to_blacklist(cls, token: str):
        """Token'ı blacklist'e ekle"""
        # Token'dan expiry time'ı al ve expire olana kadar tut
        payload = TokenManager.decode_token(token)
        if payload:
            cls._blacklist.add(token)
    
    @classmethod
    def is_blacklisted(cls, token: str) -> bool:
        """Token blacklist'te mi?"""
        return token in cls._blacklist
    
    @classmethod
    def clear_expired(cls):
        """Expired token'ları temizle (CRON job olarak çalış)"""
        # Production'da: Redis'te automatic expiration var
        cls._blacklist = set()
