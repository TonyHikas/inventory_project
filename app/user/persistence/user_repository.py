import abc

from sqlalchemy import select, exists, insert

from app.user.dto.user import UserInfoDto, UserCredsDto, CreateUserDto
from app.user.persistence.models import User
from framework.persistence.base_repository import BaseRepository, ABCBaseRepository


class ABCUserRepository(ABCBaseRepository, abc.ABC):

    @abc.abstractmethod
    async def get_one(self, user_id: int) -> UserInfoDto | None:
        pass

    @abc.abstractmethod
    async def get_creds_by_email(self, email: str) -> UserCredsDto | None:
        pass

    @abc.abstractmethod
    async def email_exists(self, email: str) -> bool:
        pass

    @abc.abstractmethod
    async def create_user(self, create_user_dto: CreateUserDto):
        pass


class UserRepository(ABCUserRepository, BaseRepository):

    async def get_one(self, user_id: int) -> UserInfoDto | None:
        async with self.ro_session() as session:
            stmt = select(
                User.id,
                User.email
            ).where(
                User.id == user_id
            )
            result = await session.execute(stmt)
            row = result.first()
        if row is None:
            return None
        return UserInfoDto.parse_obj(row)

    async def get_creds_by_email(self, email: str) -> UserCredsDto | None:
        async with self.ro_session() as session:
            stmt = select(
                User.id,
                User.email,
                User.password
            ).where(
                User.email == email
            )
            result = await session.execute(stmt)
            row = result.first()
        if row is None:
            return None
        return UserCredsDto.parse_obj(row)

    async def email_exists(self, email: str) -> bool:
        async with self.ro_session() as session:
            stmt = exists(User).where(
                User.email == email
            ).select()
            result = await session.execute(stmt)
        return result.scalars().first()

    async def create_user(self, create_user_dto: CreateUserDto):
        async with self.ro_session() as session:
            stmt = insert(
                User
            ).values(
                **create_user_dto.dict()
            ).returning(
                User.id,
                User.email
            )
            result = await session.execute(stmt)
            row = result.first()
        return UserInfoDto.parse_obj(row)
