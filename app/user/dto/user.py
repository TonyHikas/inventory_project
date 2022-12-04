from pydantic import BaseModel


class UserDto(BaseModel):
    email: str

class UserInfoDto(UserDto):
    id: int

class UserCredsDto(BaseModel):
    id: int
    email: str
    password: str

class CreateUserDto(UserDto):
    password: str
