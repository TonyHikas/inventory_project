from pydantic import BaseModel

from framework.dto.mixin import CommonDTOMixin

class MovementDTO(CommonDTOMixin, BaseModel):
    item_id: int | None = None
    from_item_id: int | None = None
    to_item_id: int | None = None
