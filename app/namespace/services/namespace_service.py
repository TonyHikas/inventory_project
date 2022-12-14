import abc

from app.namespace.dto.namespace import NamespaceDTO
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
            user_id: int
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
    async def update(self, namespace: NamespaceDTO) -> NamespaceDTO:
        pass

    @abc.abstractmethod
    async def delete(self, namespace_id: int) -> NamespaceDTO:
        pass


class NamespaceService(ABCNamespaceService):

    def __init__(self, namespace_repository: ABCNamespaceRepository) -> None:
        self.namespace_repository = namespace_repository

    async def get_one(self, namespace_id: int, user_id: int) -> NamespaceDTO:
        return await self.namespace_repository.get_one(namespace_id, user_id)

    async def get_list(self, user_id: int, limit: int, offset: int) -> list[NamespaceDTO]:
        return await self.namespace_repository.get_list(user_id, limit, offset)

    async def create(
            self,
            namespace: NamespaceDTO,
            user_id: int,
            role_slug: str
    ) -> NamespaceDTO:
        return await self.namespace_repository.create(namespace, user_id, role_slug)

    async def update(self, namespace: NamespaceDTO) -> NamespaceDTO:
        return await self.namespace_repository.update(namespace)

    async def delete(self, namespace_id: int) -> NamespaceDTO:
        return await self.namespace_repository.delete(namespace_id)
