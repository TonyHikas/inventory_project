from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.auth.auth_facade import AuthFacade
from app.user.user_facade import UserFacade

auth_scheme = HTTPBearer()

async def get_current_user(token_info: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = AuthFacade().decode_access_token(token_info.credentials)
    if token_data is None:
        raise credentials_exception
    user = await UserFacade().get_one(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
