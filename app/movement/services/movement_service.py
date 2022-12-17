import abc

from app.movement.dto.movement import MovementDTO
from app.movement.persistence.movement_repository import ABCMovementRepository
from framework.services.base_service import BaseService


class ABCMovementService(BaseService):

    @abc.abstractmethod
    def __init__(
            self,
            movement_repository: ABCMovementRepository
    ) -> None:
        self.movement_repository = None

    @abc.abstractmethod
    async def get_list(
            self,
            item_id: int
    ) -> list[MovementDTO]:
        """!!! BEFORE USE CHECK RIGHTS. !!!"""
        pass


class MovementService(ABCMovementService):

    def __init__(
            self,
            movement_repository: ABCMovementRepository
    ) -> None:
        self.movement_repository = movement_repository

    async def get_list(
            self,
            item_id: int
    ) -> list[MovementDTO]:
        return await self.movement_repository.get_list(item_id)
