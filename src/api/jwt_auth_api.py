"""
Güvenli JWT Authentication API
Mobil ve PWA uygulamaları için
"""
from flask import Blueprint, request, jsonify
from src.core.auth_utils import (
    PasswordManager,
    RateLimiter,
    AuthMiddleware,
    TokenBlacklist,
)
from src.core.token_manager import TokenManager
from src.core.jwt_config import PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH
from src.data.kimlik_dogrulama import KimlikDogrulama

jwt_auth_api = Blueprint("jwt_auth_api", __name__, url_prefix="/api/auth")
db = KimlikDogrulama()


# ─────────────────────────────────────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────────────────────────────────────
@jwt_auth_api.route("/register", methods=["POST"])
def register():
    """
    Yeni kullanıcı kaydı
    
    Request:
        {
            "username": "kullanici_adi",
            "email": "email@example.com",
            "password": "sifre123",
            "password_confirm": "sifre123"
        }
    
    Response:
        {
            "message": "Kayıt başarılı",
            "user": {
                "username": "kullanici_adi",
                "email": "email@example.com"
            }
        }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body required"}), 400
        
        username = (data.get("username") or "").strip()
        email = (data.get("email") or "").strip().lower()
        password = data.get("password", "")
        password_confirm = data.get("password_confirm", "")
        
        # Validation
        if not username or not email or not password:
            return jsonify({"error": "Eksik bilgi: username, email ve password gerekli"}), 400
        
        if len(username) < 3 or len(username) > 32:
            return jsonify({"error": "Kullanıcı adı 3-32 karakter arası olmalıdır"}), 400
        
        if password != password_confirm:
            return jsonify({"error": "Şifreler uyuşmuyor"}), 400
        
        if len(password) < PASSWORD_MIN_LENGTH or len(password) > PASSWORD_MAX_LENGTH:
            return jsonify({
                "error": f"Şifre {PASSWORD_MIN_LENGTH}-{PASSWORD_MAX_LENGTH} karakter arası olmalıdır"
            }), 400
        
        # Kullanıcı adı kontrolü
        data_dict = db.veri_oku()
        if username in data_dict.get("kullanicilar", {}):
            return jsonify({"error": "Bu kullanıcı adı zaten kullanılıyor"}), 409
        
        # E-posta kontrolü
        for user_data in data_dict.get("kullanicilar", {}).values():
            if user_data.get("eposta", "").lower() == email:
                return jsonify({"error": "Bu e-posta zaten kayıtlı"}), 409
        
        # Kaydı gerçekleştir (hash'lenmiş şifre ile)
        hashed_password = PasswordManager.hash_password(password)
        success, message = db.kayit_et(username, hashed_password, email)
        
        if not success:
            return jsonify({"error": message}), 400
        
        return jsonify({
            "message": "Kayıt başarılı",
            "user": {
                "username": username,
                "email": email
            }
        }), 201
    
    except Exception as e:
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500


# ─────────────────────────────────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────────────────────────────────
@jwt_auth_api.route("/login", methods=["POST"])
@RateLimiter.login_limit
def login():
    """
    Kullanıcı girişi (JWT token döndür)
    
    Request:
        {
            "username": "kullanici_adi",
            "password": "sifre123"
        }
    
    Response:
        {
            "message": "Giriş başarılı",
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "token_type": "Bearer",
            "expires_in": 900,
            "user": {
                "username": "kullanici_adi"
            }
        }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body required"}), 400
        
        username = (data.get("username") or "").strip()
        password = data.get("password", "")
        
        if not username or not password:
            return jsonify({"error": "Eksik bilgi: username ve password gerekli"}), 400
        
        # Kullanıcı bul ve şifre doğrula
        data_dict = db.veri_oku()
        user_data = data_dict.get("kullanicilar", {}).get(username)
        
        if not user_data:
            return jsonify({"error": "Kullanıcı adı veya şifre hatalı"}), 401
        
        # Şifre doğrulama
        stored_password_hash = user_data.get("sifre")
        if not stored_password_hash:
            return jsonify({"error": "Kullanıcı adı veya şifre hatalı"}), 401
        
        if not PasswordManager.verify_password(password, stored_password_hash):
            return jsonify({"error": "Kullanıcı adı veya şifre hatalı"}), 401
        
        # Token oluştur
        tokens = TokenManager.create_tokens(username, username)
        
        return jsonify({
            "message": "Giriş başarılı",
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": tokens["token_type"],
            "expires_in": tokens["expires_in"],
            "user": {
                "username": username
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500


# ─────────────────────────────────────────────────────────────────────────
# REFRESH TOKEN
# ─────────────────────────────────────────────────────────────────────────
@jwt_auth_api.route("/refresh", methods=["POST"])
@RateLimiter.refresh_limit
def refresh():
    """
    Refresh token ile yeni access token al
    
    Request:
        {
            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
        }
    
    Response:
        {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
            "token_type": "Bearer",
            "expires_in": 900
        }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body required"}), 400
        
        refresh_token = data.get("refresh_token", "").strip()
        if not refresh_token:
            return jsonify({"error": "refresh_token gerekli"}), 400
        
        # Blacklist kontrol
        if TokenBlacklist.is_blacklisted(refresh_token):
            return jsonify({"error": "Token geçersiz (logout edilmiş)"}), 401
        
        # Yeni access token üret
        result = TokenManager.refresh_access_token(refresh_token)
        if not result:
            return jsonify({"error": "Geçersiz veya süresi dolmuş refresh token"}), 401
        
        return jsonify({
            "access_token": result["access_token"],
            "token_type": result["token_type"],
            "expires_in": result["expires_in"]
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500


# ─────────────────────────────────────────────────────────────────────────
# LOGOUT
# ─────────────────────────────────────────────────────────────────────────
@jwt_auth_api.route("/logout", methods=["POST"])
@AuthMiddleware.require_auth
def logout():
    """
    Oturumu kapat (token'ı blacklist'e ekle)
    
    Headers:
        Authorization: Bearer <access_token>
    
    Response:
        {
            "message": "Başarıyla çıkış yapıldı"
        }
    """
    try:
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.split(" ", 1)[1]
        
        # Token'ı blacklist'e ekle
        TokenBlacklist.add_to_blacklist(token)
        
        return jsonify({
            "message": "Başarıyla çıkış yapıldı"
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500


# ─────────────────────────────────────────────────────────────────────────
# GET CURRENT USER
# ─────────────────────────────────────────────────────────────────────────
@jwt_auth_api.route("/me", methods=["GET"])
@AuthMiddleware.require_auth
def get_me():
    """
    Mevcut kullanıcı bilgisini al (Protected endpoint)
    
    Headers:
        Authorization: Bearer <access_token>
    
    Response:
        {
            "user": {
                "username": "kullanici_adi",
                "email": "email@example.com"
            }
        }
    """
    try:
        username = request.username
        
        # Kullanıcı bilgisini veritabanından al
        data_dict = db.veri_oku()
        user_data = data_dict.get("kullanicilar", {}).get(username, {})
        
        return jsonify({
            "user": {
                "username": username,
                "email": user_data.get("eposta", ""),
                "telefon": user_data.get("telefon", ""),
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"Sunucu hatası: {str(e)}"}), 500
