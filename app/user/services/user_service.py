import abc

from app.user.dto.user import UserInfoDto, UserCredsDto, CreateUserDto
from app.user.persistence.user_repository import ABCUserRepository
from framework.services.base_service import BaseService


class ABCUserService(BaseService):

    @abc.abstractmethod
    def __init__(self, user_repository: ABCUserRepository) -> None:
        pass

    @abc.abstractmethod
    async def get_one(self, user_id: int) -> UserInfoDto:
        pass

    @abc.abstractmethod
    async def get_creds_by_email(self, email: str) -> UserCredsDto:
        pass

    @abc.abstractmethod
    async def email_exists(self, email: str) -> bool:
        pass

    @abc.abstractmethod
    async def create_user(self, create_user_dto: CreateUserDto) -> UserInfoDto:
        pass


class UserService(ABCUserService):

    def __init__(self, user_repository: ABCUserRepository) -> None:
        self.user_repository = user_repository

    async def get_one(self, user_id: int) -> UserInfoDto:
        return await self.user_repository.get_one(user_id)

    async def get_creds_by_email(self, email: str) -> UserCredsDto:
        return await self.user_repository.get_creds_by_email(email)

    async def email_exists(self, email: str) -> bool:
        return await self.user_repository.email_exists(email)

    async def create_user(self, create_user_dto: CreateUserDto) -> UserInfoDto:
        return await self.user_repository.create_user(create_user_dto)
