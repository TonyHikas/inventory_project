import abc

from app.namespace.dto.namespace import NamespaceDTO, UserNamespaceWithRoleDTO, RoleDTO
from app.namespace.exceptions import NamespacePermissionDeniedException
from app.namespace.persistence.models import RightEnum
from app.namespace.persistence.namespace_repository import ABCNamespaceRepository
from framework.services.base_service import BaseService


class ABCNamespaceService(BaseService):

    @abc.abstractmethod
    def __init__(self, namespace_repository: ABCNamespaceRepository) -> None:
        pass

    @abc.abstractmethod
    async def get_one(self, namespace_id: int, user_id: int) -> NamespaceDTO:
        pass

    @abc.abstractmethod
    async def get_list(
            self,
            user_id: int,
            rights: list[RightEnum]
    ) -> list[NamespaceDTO]:
        pass

    @abc.abstractmethod
    async def create(
            self,
            namespace: NamespaceDTO,
            user_id: int,
            role_slug: str
    ) -> NamespaceDTO:
        pass

    @abc.abstractmethod
    async def update(self, namespace: NamespaceDTO, user_id: int) -> NamespaceDTO:
        pass

    @abc.abstractmethod
    async def delete(self, namespace_id: int, user_id: int) -> NamespaceDTO:
        pass

    @abc.abstractmethod
    async def check_rights(
            self,
            user_id: int,
            namespace_id: int,
            rights: list[RightEnum]
    ) -> bool:
        pass

class NamespaceService(ABCNamespaceService):

    def __init__(self, namespace_repository: ABCNamespaceRepository) -> None:
        self.namespace_repository = namespace_repository

    async def get_one(self, namespace_id: int, user_id: int) -> NamespaceDTO:
        return await self.namespace_repository.get_one(namespace_id, user_id)

    async def get_list(
        self,
        user_id: int,
        rights: list[RightEnum]
    ) -> list[NamespaceDTO]:
        user_namespaces = await self.namespace_repository.get_list(user_id, rights)
        return await self.__map_user_namespaces_to_namespace(user_namespaces)

    async def create(
            self,
            namespace: NamespaceDTO,
            user_id: int,
            role_slug: str
    ) -> NamespaceDTO:
        namespace_id = await self.namespace_repository.create(namespace, user_id, role_slug)
        namespace_dto = await self.get_one(namespace_id, user_id)
        return namespace_dto

    async def update(self, namespace: NamespaceDTO, user_id: int) -> NamespaceDTO:
        can_update = await self.namespace_repository.check_rights(
            user_id=user_id,
            namespace_id=namespace.id,
            rights=[RightEnum.EDIT_NAMESPACE]
        )
        if not can_update:
            raise NamespacePermissionDeniedException
        await self.namespace_repository.update(namespace)
        return await self.namespace_repository.get_one(namespace.id, user_id)

    async def delete(self, namespace_id: int, user_id: int) -> NamespaceDTO:
        can_update = await self.namespace_repository.check_rights(
            user_id=user_id,
            namespace_id=namespace_id,
            rights=[RightEnum.EDIT_NAMESPACE]
        )
        if not can_update:
            raise NamespacePermissionDeniedException
        namespace_dto = await self.namespace_repository.get_one(namespace_id, user_id)
        await self.namespace_repository.delete(namespace_id)
        return namespace_dto

    async def check_rights(
            self,
            user_id: int,
            namespace_id: int,
            rights: list[RightEnum]
    ) -> bool:
        return await self.namespace_repository.check_rights(user_id, namespace_id, rights)

    @staticmethod
    async def __map_user_namespaces_to_namespace(
            user_namespaces: list[UserNamespaceWithRoleDTO]
    ) -> list[NamespaceDTO]:
        namespaces_dict: dict[int, NamespaceDTO] = {}
        for user_namespace in user_namespaces:
            if not namespaces_dict.get(user_namespace.namespace_id):
                namespaces_dict[user_namespace.namespace_id] = NamespaceDTO(
                    id=user_namespace.namespace_id,
                    name=user_namespace.namespace_name,
                    created_at=user_namespace.namespace_created_at,
                    updated_at=user_namespace.namespace_updated_at,
                    roles=[]
                )
            namespaces_dict[user_namespace.namespace_id].roles.append(
                RoleDTO(
                    id=user_namespace.role_id,
                    name=user_namespace.role_name,
                    rights=user_namespace.role_rights
                )
            )

        return [*namespaces_dict.values()]
