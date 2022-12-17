from fastapi import APIRouter, status, Depends

from app.item.dependencies import item_service_dep
from app.item.services.item_service import ABCItemService
from app.movement.communication.schema import MovementResponse
from app.movement.dependencies import movement_service_dep
from app.movement.services.movement_service import ABCMovementService
from app.namespace.dependencies import namespace_service_dep
from app.namespace.exceptions import NamespacePermissionDeniedException
from app.namespace.persistence.models import RightEnum
from app.namespace.services.namespace_service import ABCNamespaceService
from app.user.dependencies.user import current_user_dep
from app.user.dto.user import UserInfoDto

router = APIRouter(prefix='/movement', tags=['movement'])


@router.get(
    '/{item_id}',
    response_model=list[MovementResponse],
    responses={status.HTTP_404_NOT_FOUND: {}}
)
async def get_list(
        item_id: int,
        user: UserInfoDto = Depends(current_user_dep),
        item_service: ABCItemService = Depends(item_service_dep),
        namespace_service: ABCNamespaceService = Depends(namespace_service_dep),
        movement_service: ABCMovementService = Depends(movement_service_dep),
):
    item = await item_service.get_one(item_id, user.id)
    can_view = await namespace_service.check_rights(user.id, item.namespace_id, [RightEnum.VIEW])
    if not can_view:
        raise NamespacePermissionDeniedException
    movement_list = await movement_service.get_list(item_id)
    return [MovementResponse.parse_obj(movement) for movement in movement_list]
