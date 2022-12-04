from datetime import datetime

from pydantic import BaseModel


class UserDto(BaseModel):
    email: str

class UserInfoDto(UserDto):
    user_id: int

class UserCredsDto(BaseModel):
    user_id: int
    email: str
    password: str

class CreateUserDto(UserDto):
    password: str
