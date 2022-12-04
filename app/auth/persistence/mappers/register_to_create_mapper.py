from datetime import timezone, datetime

from app.auth.dto.user import UserRegisterDto
from app.user.dto.role import RoleEnum
from app.user.dto.user import CreateUserDto


class RegisterToCreateMapper:

    def map(self, register_data: UserRegisterDto, hashed_password: str) -> CreateUserDto:
        return CreateUserDto(
            email=register_data.email,
            password=hashed_password,
        )
