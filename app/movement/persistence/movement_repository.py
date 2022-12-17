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
