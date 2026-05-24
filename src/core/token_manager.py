"""Token Manager: JWT oluşturma, doğrulama ve refresh işlemleri"""
import jwt
from datetime import datetime, timedelta
from src.core.jwt_config import (
    SECRET_KEY,
    ALGORITHM,
    TOKEN_TYPE_ACCESS,
    TOKEN_TYPE_REFRESH,
    get_token_expiry,
)


class TokenManager:
    """JWT token yönetimi"""

    @staticmethod
    def create_tokens(user_id: str, username: str):
        """
        Access + Refresh token üret
        
        Args:
            user_id: Kullanıcı ID
            username: Kullanıcı adı
            
        Returns:
            dict: {"access_token": "...", "refresh_token": "...", "expires_in": seconds}
        """
        now = datetime.utcnow()

        # Access Token
        access_payload = {
            "sub": user_id,
            "username": username,
            "type": TOKEN_TYPE_ACCESS,
            "iat": now,
            "exp": now + get_token_expiry(TOKEN_TYPE_ACCESS),
        }
        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)

        # Refresh Token
        refresh_payload = {
            "sub": user_id,
            "username": username,
            "type": TOKEN_TYPE_REFRESH,
            "iat": now,
            "exp": now + get_token_expiry(TOKEN_TYPE_REFRESH),
        }
        refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
            "expires_in": int(get_token_expiry(TOKEN_TYPE_ACCESS).total_seconds()),
        }

    @staticmethod
    def verify_token(token: str, token_type: str = TOKEN_TYPE_ACCESS):
        """
        Token doğrula
        
        Args:
            token: JWT token
            token_type: "access" veya "refresh"
            
        Returns:
            tuple: (is_valid, payload_or_error)
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            # Token type kontrol
            if payload.get("type") != token_type:
                return False, f"Invalid token type. Expected {token_type}"
            
            return True, payload
        except jwt.ExpiredSignatureError:
            return False, "Token has expired"
        except jwt.InvalidTokenError as e:
            return False, f"Invalid token: {str(e)}"
        except Exception as e:
            return False, f"Error verifying token: {str(e)}"

    @staticmethod
    def decode_token(token: str):
        """
        Token'ı decode et (doğrulama olmadan - test için)
        
        Args:
            token: JWT token
            
        Returns:
            dict: payload
        """
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except Exception:
            return None

    @staticmethod
    def refresh_access_token(refresh_token: str):
        """
        Refresh token ile yeni access token üret
        
        Args:
            refresh_token: Refresh token
            
        Returns:
            dict: {"access_token": "...", "expires_in": seconds} veya None
        """
        is_valid, payload = TokenManager.verify_token(
            refresh_token, token_type=TOKEN_TYPE_REFRESH
        )
        
        if not is_valid:
            return None
        
        user_id = payload.get("sub")
        username = payload.get("username")
        
        if not user_id or not username:
            return None
        
        # Yeni access token üret
        now = datetime.utcnow()
        access_payload = {
            "sub": user_id,
            "username": username,
            "type": TOKEN_TYPE_ACCESS,
            "iat": now,
            "exp": now + get_token_expiry(TOKEN_TYPE_ACCESS),
        }
        new_access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
        
        return {
            "access_token": new_access_token,
            "token_type": "Bearer",
            "expires_in": int(get_token_expiry(TOKEN_TYPE_ACCESS).total_seconds()),
        }

    @staticmethod
    def get_user_from_token(token: str):
        """
        Token'dan kullanıcı bilgisi çıkar
        
        Args:
            token: JWT token
            
        Returns:
            dict: {"user_id": "...", "username": "..."} veya None
        """
        is_valid, payload = TokenManager.verify_token(token, token_type=TOKEN_TYPE_ACCESS)
        
        if not is_valid:
            return None
        
        return {
            "user_id": payload.get("sub"),
            "username": payload.get("username"),
        }
