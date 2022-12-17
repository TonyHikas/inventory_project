import abc

from sqlalchemy import select, insert

from app.movement.dto.movement import MovementDTO
from app.movement.persistence.models import ItemMovement
from framework.persistence.base_repository import BaseRepository, ABCBaseRepository


class ABCMovementRepository(ABCBaseRepository, abc.ABC):

    @abc.abstractmethod
    async def get_list(
            self,
            item_id: int
    ) -> list[MovementDTO]:
        pass

    @abc.abstractmethod
    async def create(
            self,
            movement: MovementDTO
    ) -> int:
        pass


class MovementRepository(ABCMovementRepository, BaseRepository):

    async def get_list(
            self,
            item_id: int
    ) -> list[MovementDTO]:
        async with self.ro_session() as session:
            movement_stmt = select(
                ItemMovement.id,
                ItemMovement.item_id,
                ItemMovement.from_item_id,
                ItemMovement.to_item_id,
                ItemMovement.created_at,
                ItemMovement.updated_at
            ).where(
                ItemMovement.item_id == item_id
            )
            result = await session.execute(movement_stmt)

        return [MovementDTO.parse_obj(row) for row in result]

    async def create(
            self,
            movement: MovementDTO
    ) -> int:
        async with self.session() as session:
            item_stmt = insert(
                ItemMovement
            ).values(
                from_item_id=movement.from_item_id,
                to_item_id=movement.to_item_id
            ).returning(
                ItemMovement.id
            )
            result = await session.execute(item_stmt)

        return result.first().id
