from fastapi import status
from app.exceptions.base_exception import AppBaseException

class UserNotFoundException(AppBaseException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="USER_NOT_FOUND",
            detail=f"User with email {email} not found"
        )


class UserAlreadyExistException(AppBaseException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code="USER_ALREADY_EXIST",
            detail=f"User with email {email} already exist"
        )


class InvalidCredentialsException(AppBaseException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="INVALID_CREDENTIALS",
            detail="Invalid email or password"
        )
    