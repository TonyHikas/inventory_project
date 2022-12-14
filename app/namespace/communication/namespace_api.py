from fastapi import APIRouter, status, Depends, Query

from app.namespace.communication.schema import NamespaceResponse, NamespaceRequest
from app.namespace.dependencies import namespace_service_dep
from app.namespace.dto.namespace import NamespaceDTO
from app.namespace.exceptions import NamespaceNotFoundException
from app.namespace.services.namespace_service import ABCNamespaceService
from app.user.dependencies.user import current_user_dep
from app.user.dto.user import UserInfoDto

router = APIRouter(prefix='/namespace', tags=['namespace'])


@router.get(
    '/{namespace_id}',
    response_model=NamespaceResponse,
    responses={status.HTTP_404_NOT_FOUND: {}}
)
async def get_one(
        namespace_id: int,
        user: UserInfoDto = Depends(current_user_dep),
        namespace_service: ABCNamespaceService = Depends(namespace_service_dep)
):
    namespace = await namespace_service.get_one(namespace_id, user.id)
    return NamespaceResponse(**namespace.dict())


@router.get(
    '/',
    response_model=list[NamespaceResponse]
)
async def get_list(
        user: UserInfoDto = Depends(current_user_dep),
        limit: int = Query(default=100, lte=100),
        offset: int = Query(default=0),
        namespace_service: ABCNamespaceService = Depends(namespace_service_dep)
):
    namespace_list = await namespace_service.get_list(
        user_id=user.id
    )
    return [NamespaceResponse(**namespace.dict()) for namespace in namespace_list]

@router.post(
    '/',
    response_model=NamespaceResponse
)
async def create(
        namespace_request: NamespaceRequest,
        user: UserInfoDto = Depends(current_user_dep),
        namespace_service: ABCNamespaceService = Depends(namespace_service_dep)
):
    namespace_dto = NamespaceDTO(
        name=namespace_request.name
    )
    namespace = await namespace_service.create(namespace_dto, user.id, 'owner')
    return NamespaceResponse(**namespace.dict())
