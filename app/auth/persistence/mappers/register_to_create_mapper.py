from datetime import timezone, datetime

from app.auth.auth_facade import AuthFacade
from app.auth.dto.user import UserRegisterDto
from app.user.dto.role import RoleEnum
from app.user.dto.user import CreateUserDto


class RegisterToCreateMapper:

    def map(self, register_data: UserRegisterDto) -> CreateUserDto:
        hashed_password = AuthFacade().get_password_hash(register_data.password)
        current_time = datetime.now(tz=timezone.utc)
        return CreateUserDto(
            first_name=register_data.first_name,
            email=register_data.email,
            phone=register_data.phone,
            password=hashed_password,
            created_at=current_time,
            updated_at=current_time,
            role=RoleEnum.user
        )
