import abc
from datetime import timedelta, datetime, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.auth.dto.token import JwtTokenDto, TokenData, IssuerEnum, SubjectEnum
from core.settings import settings
from framework.services.base_service import BaseService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ABCAuthService(BaseService):

    def create_new_jwt_token(self, user_id: int) -> JwtTokenDto:
        pass

    def create_access_token(self, user_id: int) -> str:
        pass

    def decode_access_token(self, access_token: str) -> TokenData | None:
        pass

    def create_refresh_token(self, user_id: int) -> str:
        pass

    def decode_refresh_token(self, refresh_token: str) -> TokenData | None:
        pass

    @staticmethod
    def create_token(token: TokenData) -> str:
        pass

    @staticmethod
    def decode_token(token) -> TokenData:
        pass

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        pass

    @staticmethod
    def get_password_hash(password) -> str:
        pass


class AuthService(ABCAuthService):

    def create_new_jwt_token(self, user_id: int) -> JwtTokenDto:
        return JwtTokenDto(
            access_token=self.create_access_token(user_id),
            refresh_token=self.create_refresh_token(user_id)
        )

    def create_access_token(self, user_id: int) -> str:
        return self.create_token(
            TokenData(
                iss=IssuerEnum.auth_module,
                sub=SubjectEnum.auth,
                exp=datetime.now(tz=timezone.utc) + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS),
                user_id=user_id
            )
        )

    def decode_access_token(self, access_token: str) -> TokenData | None:
        try:
            token_data = self.decode_token(access_token)
        except JWTError:
            return None
        if token_data.exp > datetime.now(tz=timezone.utc) and token_data.sub is SubjectEnum.auth:
            return token_data
        return None

    def create_refresh_token(self, user_id: int) -> str:
        return self.create_token(
            TokenData(
                iss=IssuerEnum.auth_module,
                sub=SubjectEnum.refresh_auth,
                exp=datetime.now(tz=timezone.utc) + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS),
                user_id=user_id
            )
        )

    def decode_refresh_token(self, refresh_token: str) -> TokenData | None:
        try:
            token_data = self.decode_token(refresh_token)
        except JWTError:
            return None
        if token_data.exp > datetime.now(tz=timezone.utc) and token_data.sub is SubjectEnum.refresh_auth:
            return token_data
        return None

    @staticmethod
    def create_token(token: TokenData) -> str:
        encoded_jwt = jwt.encode(token.dict(), settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token) -> TokenData:
        return TokenData.parse_obj(jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]))

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        return pwd_context.hash(password)
