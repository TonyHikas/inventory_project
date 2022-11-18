from datetime import datetime
from enum import Enum

from pydantic import BaseModel

class IssuerEnum(str, Enum):
    auth_module = 'auth_module'

class SubjectEnum(str, Enum):
    auth = 'auth'  # access token
    refresh_auth = 'refresh_auth'  # refresh token

class JwtTokenDto(BaseModel):
    access_token: str
    refresh_token: str

class TokenData(BaseModel):
    iss: IssuerEnum
    sub: SubjectEnum
    exp: datetime
    user_id: int
