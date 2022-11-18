from datetime import datetime

from pydantic import BaseModel


class UserDto(BaseModel):
    first_name: str
    phone: str | None
    email: str
    role: str

class UserInfoDto(UserDto):
    user_id: int

class UserCredsDto(BaseModel):
    user_id: int
    email: str
    password: str

class CreateUserDto(UserDto):
    password: str
    created_at: datetime
    updated_at: datetime
