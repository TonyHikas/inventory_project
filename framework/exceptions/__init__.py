from typing import Any

from fastapi import HTTPException


class AppException(HTTPException):

    def __init__(self, status_code: int = None, detail: Any = None) -> None:
        super().__init__(
            status_code=status_code or self.status_code,
            detail=detail or self.detail
        )
