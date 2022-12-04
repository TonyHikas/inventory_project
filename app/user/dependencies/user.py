from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.dependencies.auth import auth_service_dep
from app.auth.services.auth_service import ABCAuthService
from app.user.persistence.user_repository import UserRepository
from app.user.services.user_service import UserService, ABCUserService
from framework.dependencies.session import rw_engine_dep, ro_engine_dep

auth_scheme = HTTPBearer()


async def user_repository_dep(
        rw_engine=Depends(rw_engine_dep),
        ro_engine=Depends(ro_engine_dep)
):
    return UserRepository(rw_engine, ro_engine)


async def user_service_dep(
        user_repository=Depends(user_repository_dep)
):
    return UserService(user_repository)


async def current_user_dep(
        token_info: HTTPAuthorizationCredentials = Depends(auth_scheme),
        user_service: ABCUserService = Depends(user_service_dep),
        auth_service: ABCAuthService = Depends(auth_service_dep)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = auth_service.decode_access_token(token_info.credentials)
    if token_data is None:
        raise credentials_exception
    user = await user_service.get_one(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
