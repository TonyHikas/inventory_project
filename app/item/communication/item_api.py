from fastapi import APIRouter, status, Depends, Query

from app.item.communication.schema import ItemResponse, ItemRequest
from app.item.dependencies import item_service_dep
from app.item.dto.item import ItemDTO
from app.item.services.item_service import ABCItemService
from app.user.dependencies.user import current_user_dep
from app.user.dto.user import UserInfoDto

router = APIRouter(prefix='/item', tags=['item'])


@router.get(
    '/{item_id}',
    response_model=ItemResponse,
    responses={status.HTTP_404_NOT_FOUND: {}}
)
async def get_one(
        item_id: int,
        user: UserInfoDto = Depends(current_user_dep),
        item_service: ABCItemService = Depends(item_service_dep)
):
    namespace = await item_service.get_one(item_id, user.id)
    return ItemResponse(**namespace.dict())


@router.get(
    '/',
    response_model=list[ItemResponse]
)
async def get_list(
        namespace_id: int,
        limit: int = Query(default=20, ge=0, le=50),
        offset: int = Query(default=0, ge=0),
        user: UserInfoDto = Depends(current_user_dep),
        item_service: ABCItemService = Depends(item_service_dep)
):
    item_list = await item_service.get_list(
        namespace_id=namespace_id,
        user_id=user.id,
        limit=limit,
        offset=offset
    )
    return [ItemResponse(**item.dict()) for item in item_list]


@router.post(
    '/',
    response_model=ItemResponse
)
async def create(
        item_request: ItemRequest,
        user: UserInfoDto = Depends(current_user_dep),
        item_service: ABCItemService = Depends(item_service_dep)
):
    item_dto = ItemDTO.parse_obj(
        item_request
    )
    item = await item_service.create(item_dto, user.id)
    return ItemResponse.parse_obj(item)


@router.put(
    '/{item_id}',
    response_model=ItemResponse
)
async def update(
        item_id: int,
        item_request: ItemRequest,
        user: UserInfoDto = Depends(current_user_dep),
        item_service: ABCItemService = Depends(item_service_dep)
):
    item_dto = ItemDTO.parse_obj(
        item_request
    )
    item_dto.id = item_id
    item = await item_service.update(item_dto, user.id)
    return ItemResponse.parse_obj(item)


@router.delete(
    '/{item_id}',
    response_model=ItemResponse
)
async def delete(
        item_id: int,
        user: UserInfoDto = Depends(current_user_dep),
        item_service: ABCItemService = Depends(item_service_dep)
):
    item = await item_service.delete(item_id, user.id)

    return ItemResponse.parse_obj(item)
