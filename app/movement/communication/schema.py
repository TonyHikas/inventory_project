from datetime import datetime

from pydantic import BaseModel


class MovementResponse(BaseModel):
    id: int
    item_id: int
    from_item_id: int | None = None
    to_item_id: int | None = None
    created_at: datetime
    updated_at: datetime
