from fastapi import APIRouter, status, Depends

from app.namespace.communication.schema import NamespaceResponse, NamespaceRequest, NamespaceEditRoleRequest, \
    RoleResponse
from app.namespace.dependencies import namespace_service_dep
from app.namespace.dto.namespace import NamespaceDTO
from app.namespace.persistence.models import RightEnum
from app.namespace.services.namespace_service import ABCNamespaceService
from app.user.dependencies.user import current_user_dep
from app.user.dto.user import UserInfoDto

router = APIRouter(prefix='/namespace', tags=['namespace'])

@router.get(
    '/get_all_roles',
    response_model=list[RoleResponse],
    responses={status.HTTP_404_NOT_FOUND: {}}
)
async def get_all_roles(
        user: UserInfoDto = Depends(current_user_dep),
        namespace_service: ABCNamespaceService = Depends(namespace_service_dep)
):
    roles_dto_list = await namespace_service.get_all_roles()
    return [
        RoleResponse.parse_obj(role) for role in roles_dto_list
    ]


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
        namespace_service: ABCNamespaceService = Depends(namespace_service_dep)
):
    namespace_list = await namespace_service.get_list(
        user_id=user.id,
        rights=[RightEnum.VIEW]
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


@router.put(
    '/{namespace_id}',
    response_model=NamespaceResponse
)
async def update(
        namespace_id: int,
        namespace_request: NamespaceRequest,
        user: UserInfoDto = Depends(current_user_dep),
        namespace_service: ABCNamespaceService = Depends(namespace_service_dep)
):
    namespace_dto = NamespaceDTO(
        id=namespace_id,
        name=namespace_request.name
    )
    namespace = await namespace_service.update(namespace_dto, user.id)
    return NamespaceResponse(**namespace.dict())


@router.delete(
    '/{namespace_id}',
    response_model=NamespaceResponse
)
async def delete(
        namespace_id: int,
        user: UserInfoDto = Depends(current_user_dep),
        namespace_service: ABCNamespaceService = Depends(namespace_service_dep)
):
    namespace = await namespace_service.delete(namespace_id, user.id)
    return NamespaceResponse(**namespace.dict())


@router.post(
    '/{namespace_id}/add_user_role',
    response_model={},
    responses={status.HTTP_404_NOT_FOUND: {}}
)
async def add_user_role(
        namespace_id: int,
        edit_role_request: NamespaceEditRoleRequest,
        user: UserInfoDto = Depends(current_user_dep),
        namespace_service: ABCNamespaceService = Depends(namespace_service_dep)
):
    await namespace_service.add_user_role(
        user.id,
        edit_role_request.user_id,
        namespace_id,
        edit_role_request.role_id
    )
    return {}

@router.delete(
    '/{namespace_id}/remove_user_role',
    response_model={},
    responses={status.HTTP_404_NOT_FOUND: {}}
)
async def remove_user_role(
        namespace_id: int,
        edit_role_request: NamespaceEditRoleRequest,
        user: UserInfoDto = Depends(current_user_dep),
        namespace_service: ABCNamespaceService = Depends(namespace_service_dep)
):
    await namespace_service.remove_user_role(
        user.id,
        edit_role_request.user_id,
        namespace_id,
        edit_role_request.role_id
    )
    return {}

