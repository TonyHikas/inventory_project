import abc

from app.item.dto.item import ItemDTO
from app.item.exceptions import ChangeNamespaceException
from app.item.persistence.item_repository import ABCItemRepository
from app.movement.dto.movement import MovementDTO
from app.movement.services.movement_service import ABCMovementService
from app.namespace.dto.namespace import NamespaceDTO
from app.namespace.exceptions import NamespacePermissionDeniedException
from app.namespace.persistence.models import RightEnum
from app.namespace.services.namespace_service import ABCNamespaceService
from framework.services.base_service import BaseService


class ABCItemService(BaseService):

    @abc.abstractmethod
    def __init__(
            self,
            item_repository: ABCItemRepository,
            namespace_service: ABCNamespaceService
    ) -> None:
        pass

    @abc.abstractmethod
    async def get_one(self, item_id: int, user_id: int) -> ItemDTO:
        pass

    @abc.abstractmethod
    async def get_one_min(self, item_id: int, user_id: int) -> ItemDTO:
        pass

    @abc.abstractmethod
    async def get_list(
            self,
            namespace_id: int,
            user_id: int,
            limit: int | None = None,
            offset: int | None = None
    ) -> list[ItemDTO]:
        pass

    @abc.abstractmethod
    async def create(
            self,
            item: ItemDTO,
            user_id: int
    ) -> ItemDTO:
        pass

    @abc.abstractmethod
    async def update(self, item: ItemDTO, user_id: int) -> ItemDTO:
        pass

    @abc.abstractmethod
    async def delete(self, item_id: int, user_id: int) -> ItemDTO:
        pass


class ItemService(ABCItemService):

    def __init__(
            self,
            item_repository: ABCItemRepository,
            namespace_service: ABCNamespaceService
    ) -> None:
        self.item_repository = item_repository
        self.namespace_service = namespace_service

    async def get_one(self, item_id: int, user_id: int) -> ItemDTO:
        item_dto = await self.item_repository.get_one(item_id)

        if not await self.namespace_service.check_rights(user_id, item_dto.namespace_id, [RightEnum.VIEW]):
            raise NamespacePermissionDeniedException

        return item_dto

    async def get_one_min(self, item_id: int, user_id: int) -> ItemDTO:
        item_dto = await self.item_repository.get_one_min(item_id)

        if not await self.namespace_service.check_rights(user_id, item_dto.namespace_id, [RightEnum.VIEW]):
            raise NamespacePermissionDeniedException

        return item_dto

    async def get_list(
            self,
            namespace_id: int,
            user_id: int,
            limit: int | None = None,
            offset: int | None = None
    ) -> list[ItemDTO]:
        if not await self.namespace_service.check_rights(user_id, namespace_id, [RightEnum.VIEW]):
            raise NamespacePermissionDeniedException

        return await self.item_repository.get_list(namespace_id, limit, offset)

    async def create(
            self,
            item: ItemDTO,
            user_id: int
    ) -> ItemDTO:
        if not await self.namespace_service.check_rights(user_id, item.namespace_id, [RightEnum.EDIT_ITEMS]):
            raise NamespacePermissionDeniedException
        item_id = await self.item_repository.create(item)
        item_dto = await self.item_repository.get_one(item_id)
        return item_dto

    async def update(self, item: ItemDTO, user_id: int) -> ItemDTO:
        item_before = await self.item_repository.get_one(item.id)
        if item_before.namespace_id != item.namespace_id:
            raise ChangeNamespaceException
        if not await self.namespace_service.check_rights(user_id, item.namespace_id, [RightEnum.EDIT_ITEMS]):
            raise NamespacePermissionDeniedException
        await self.item_repository.update(item)
        item_dto = await self.item_repository.get_one(item.id)
        return item_dto

    async def delete(self, item_id: int, user_id: int) -> ItemDTO:
        item_dto = await self.item_repository.get_one(item_id)
        if not await self.namespace_service.check_rights(user_id, item_dto.namespace_id, [RightEnum.EDIT_ITEMS]):
            raise NamespacePermissionDeniedException
        await self.item_repository.delete(item_id)
        return item_dto
