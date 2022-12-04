from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import EmailStr

from app.auth.dependencies.auth import auth_service_dep
from app.auth.dto.token import JwtTokenDto
from app.auth.dto.user import UserRegisterDto
from app.auth.persistence.mappers.register_to_create_mapper import RegisterToCreateMapper
from app.auth.services.auth_service import ABCAuthService
from app.user.dependencies.user import user_service_dep
from app.user.services.user_service import ABCUserService

router = APIRouter()

@router.post(
    '/register',
    response_model=JwtTokenDto,
    responses={status.HTTP_409_CONFLICT: {'description': 'Email already registered'}}
)
async def register(
        register_data: UserRegisterDto,
        user_service: ABCUserService = Depends(user_service_dep),
        auth_service: ABCAuthService = Depends(auth_service_dep),
):
    email_exists = await user_service.email_exists(register_data.email)
    if email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This email already registered')
    hashed_password = auth_service.get_password_hash(register_data.password)
    user_create_data = RegisterToCreateMapper().map(register_data, hashed_password)
    user = await user_service.create_user(user_create_data)
    jwt_token = auth_service.create_new_jwt_token(user.user_id)
    return jwt_token

@router.post(
    '/login',
    response_model=JwtTokenDto,
    responses={status.HTTP_400_BAD_REQUEST: {'description': 'Auth data not valid'}}
)
async def login(
        email: EmailStr,
        password: str,
        user_service: ABCUserService = Depends(user_service_dep),
        auth_service: ABCAuthService = Depends(auth_service_dep),
):
    error_text = 'Auth data not valid'
    user_creds = await user_service.get_creds_by_email(email)
    if user_creds is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_text)
    password_valid = auth_service.verify_password(
        plain_password=password,
        hashed_password=user_creds.password
    )
    if not password_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_text)

    jwt_token = auth_service.create_new_jwt_token(user_creds.user_id)
    return jwt_token

@router.post(
    '/refresh',
    response_model=str,
    responses={status.HTTP_400_BAD_REQUEST: {'description': 'Token is not valid or expired'}}
)
async def refresh(
        refresh_token: str,
        auth_service: ABCAuthService = Depends(auth_service_dep),
) -> str:
    token_data = auth_service.decode_refresh_token(refresh_token)
    if token_data is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token is not valid or expired')
    return auth_service.create_access_token(token_data.user_id)




