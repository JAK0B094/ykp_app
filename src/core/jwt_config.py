"""JWT Konfigürasyonu ve Sabitleri"""
import os
from datetime import timedelta

# JWT Secret Key (environment variable'dan veya default)
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jkb-jwt-secret-key-2026-gizli")

# Token Expiration Times
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 dakika
REFRESH_TOKEN_EXPIRE_DAYS = 7     # 7 gün

# JWT Algorithm
ALGORITHM = "HS256"

# Token Types
TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"

# Rate Limiting (requests/minute)
LOGIN_RATE_LIMIT = 5  # Login denemesi: 5/dakika
REFRESH_RATE_LIMIT = 10  # Refresh: 10/dakika

# Password Requirements
PASSWORD_MIN_LENGTH = 6
PASSWORD_MAX_LENGTH = 32

# CORS Configuration
CORS_ORIGINS = [
    "http://localhost:*",
    "http://127.0.0.1:*",
    "https://*",
]

CORS_ALLOW_HEADERS = [
    "Content-Type",
    "Authorization",
]

CORS_EXPOSE_HEADERS = [
    "Content-Type",
]


def get_token_expiry(token_type):
    """Token geçerlilik süresi döndür"""
    if token_type == TOKEN_TYPE_ACCESS:
        return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    elif token_type == TOKEN_TYPE_REFRESH:
        return timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return timedelta(minutes=15)
