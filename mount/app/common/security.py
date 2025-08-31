from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.common.settings import settings


def create_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_expiration_minutes
    )
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key)
    return encoded_jwt


def hash_password(password: str) -> str:
    pw = password.encode()
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(pw, salt).decode()
    return password_hash


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())
