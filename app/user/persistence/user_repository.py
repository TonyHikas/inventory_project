from app.user.dto.user import UserInfoDto, UserCredsDto, CreateUserDto
from framework.persistence.base_repository import BaseRepository


class UserRepository(BaseRepository):

    async def get_one(self, user_id: int) -> UserInfoDto | None:
        query = '''
        SELECT user_id, first_name, phone, email, role FROM users WHERE user_id = :user_id;
        '''
        values = {
            'user_id': user_id,
        }
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
