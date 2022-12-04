from sqlalchemy import select

from app.user.dto.user import UserInfoDto, UserCredsDto, CreateUserDto
from app.user.persistence.models import User
from framework.persistence.base_repository import BaseRepository


class ABCUserRepository(BaseRepository):

    async def get_one(self, user_id: int) -> UserInfoDto | None:
        pass

    async def get_creds_by_email(self, email: str) -> UserCredsDto | None:
        pass

    async def email_exists(self, email: str) -> bool:
        pass

    async def create_user(self, create_user_dto: CreateUserDto):
        pass


class UserRepository(BaseRepository):

    async def get_one(self, user_id: int) -> UserInfoDto | None:
        async with self.ro_session() as session:
            stmt = select(
                User.id,
                User.email
            ).where(
                User.id == user_id
            )
        user = await self.database.fetch_one(query, values)
        if user is None:
            return None
        return UserInfoDto.parse_obj(user)

    async def get_creds_by_email(self, email: str) -> UserCredsDto | None:
        query = '''
        SELECT user_id, email, password FROM users WHERE email = :email;
        '''
        values = {
            'email': email,
        }
        user = await self.database.fetch_one(query, values)
        if user is None:
            return None
        return UserCredsDto.parse_obj(user)

    async def email_exists(self, email: str) -> bool:
        query = '''
        SELECT COUNT(1) FROM users WHERE email = :email
        '''
        values = {
            'email': email,
        }
        users_count = await self.database.execute(query, values)
        return users_count > 0

    async def create_user(self, create_user_dto: CreateUserDto):
        query = '''
        INSERT INTO users (first_name, phone, email, password, role, created_at, updated_at) 
        VALUES (:first_name, :phone, :email, :password, :role, :created_at, :updated_at)
        RETURNING user_id, first_name, phone, email, role;
        '''
        values = {
            **create_user_dto.dict()
        }
        user = await self.database.fetch_one(query, values)
        if user is None:
            return None
        return UserInfoDto.parse_obj(user)
