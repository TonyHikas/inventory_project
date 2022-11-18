from datetime import timedelta, datetime, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.auth.dto.token import JwtTokenDto, TokenData, IssuerEnum, SubjectEnum
from core.settings import JWT_SECRET, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_SECONDS, REFRESH_TOKEN_EXPIRE_SECONDS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthFacade:

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
                exp=datetime.now(tz=timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS),
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
                exp=datetime.now(tz=timezone.utc) + timedelta(seconds=REFRESH_TOKEN_EXPIRE_SECONDS),
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
        encoded_jwt = jwt.encode(token.dict(), JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token) -> TokenData:
        return TokenData.parse_obj(jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM]))

    @staticmethod
    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password) -> str:
        return pwd_context.hash(password)
