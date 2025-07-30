from datetime import datetime, timedelta, timezone

import bcrypt
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.common.settings import settings
from app.database.core import Base


class User(Base):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    password_hash: Mapped[str] = mapped_column(String)
    user_type: Mapped[str] = mapped_column(String, default="employee")
    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisations.id"))

    @property
    def token(self):
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.jwt_expiration_minutes
        )
        to_encode = {"sub": str(self.id), "exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key)
        return encoded_jwt

    def set_password(self, password: str) -> None:
        pw = password.encode()
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(pw, salt).decode()

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    @staticmethod
    def verify_token(token: str) -> dict | None:
        """
        Verifies the JWT token and returns the decoded payload if valid.

        Raises:
            ExpiredSignatureError: if the token has expired.
            JWTError: if the token is invalid.
        """
        try:
            payload = jwt.decode(token, settings.jwt_secret_key)
            return payload
        except ExpiredSignatureError:
            print("Token has expired.")
        except JWTError:
            print("Invalid token.")
        return None
