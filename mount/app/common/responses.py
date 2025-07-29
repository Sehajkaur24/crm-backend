from typing import Any, Generic, TypeVar
from pydantic import BaseModel

# Type variables for generic typing
T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    meta: dict[str, Any] = {}
    data: T | None = None
    error: dict[str, Any] = {}

def success(
    data: Any = None,
    meta: dict[str, Any] = {},
) -> dict:
    """
    Create a generic success response.
    
    Args:
        data: The data to return (generic type T)
        meta: Metadata (pagination, etc.)
    
    Returns:
        dict with ResponseModel structure
    """
    response = {
        "meta": meta,
        "data": data,
        "error": {}
    }
    
    return response


def failure(
    error_code: str,
    error_detail: Any,
) -> dict:
    """
    Create a generic failure response.
    
    Args:
        error: Error information dictionary
    
    Returns:
        dict with ResponseModel structure
    """
    response = {
        "meta": {},
        "data": None,
        "error": {
            "code": error_code,
            "detail": error_detail
        }
    }
    
    return response