from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr

from app.auth.auth_facade import AuthFacade
from app.auth.dto.token import JwtTokenDto
from app.auth.dto.user import UserRegisterDto
from app.auth.persistence.mappers.register_to_create_mapper import RegisterToCreateMapper
from app.user.user_facade import UserFacade


router = APIRouter()

@router.post(
    '/register',
    response_model=JwtTokenDto,
    responses={status.HTTP_409_CONFLICT: {'description': 'Email already registered'}}
)
async def register(register_data: UserRegisterDto):
    user_facade = UserFacade()
    email_exists = await user_facade.email_exists(register_data.email)
    if email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This email already registered')
    user_create_data = RegisterToCreateMapper().map(register_data)
    user = await user_facade.create_user(user_create_data)
    jwt_token = AuthFacade().create_new_jwt_token(user.user_id)
    return jwt_token

@router.post(
    '/login',
    response_model=JwtTokenDto,
    responses={status.HTTP_400_BAD_REQUEST: {'description': 'Auth data not valid'}}
)
async def login(email: EmailStr, password: str):
    error_text = 'Auth data not valid'
    user_creds = await UserFacade().get_creds_by_email(email)
    if user_creds is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_text)
    auth_facade = AuthFacade()
    password_valid = auth_facade.verify_password(
        plain_password=password,
        hashed_password=user_creds.password
    )
    if not password_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_text)

    jwt_token = auth_facade.create_new_jwt_token(user_creds.user_id)
    return jwt_token

@router.post(
    '/refresh',
    response_model=str,
    responses={status.HTTP_400_BAD_REQUEST: {'description': 'Token is not valid or expired'}}
)
async def refresh(refresh_token: str) -> str:
    auth_facade = AuthFacade()
    token_data = auth_facade.decode_refresh_token(refresh_token)
    if token_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid or expired')
    return auth_facade.create_access_token(token_data.user_id)




