from fastapi import APIRouter, Depends

from app.user.dependencies.user import current_user_dep
from app.user.dto.user import UserInfoDto

router = APIRouter()

@router.get('/me', response_model=UserInfoDto)
async def user_info(user=Depends(current_user_dep)):
    return user
