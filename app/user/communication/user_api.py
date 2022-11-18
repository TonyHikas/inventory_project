from fastapi import APIRouter, Depends

from app.user.dependencies.user import get_current_user
from app.user.dto.user import UserInfoDto
from app.user.user_facade import UserFacade

router = APIRouter()

@router.get('/me', response_model=UserInfoDto)
async def user_info(user=Depends(get_current_user)):
    return user
