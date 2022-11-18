from app.user.dto.user import UserInfoDto, UserCredsDto, CreateUserDto
from app.user.persistence.user_repository import UserRepository


class UserFacade:

    async def get_one(self, user_id: int) -> UserInfoDto:
        return await UserRepository().get_one(user_id)

    async def get_creds_by_email(self, email: str) -> UserCredsDto:
        return await UserRepository().get_creds_by_email(email)

    async def email_exists(self, email: str) -> bool:
        return await UserRepository().email_exists(email)

    async def create_user(self, create_user_dto: CreateUserDto) -> UserInfoDto:
        return await UserRepository().create_user(create_user_dto)
