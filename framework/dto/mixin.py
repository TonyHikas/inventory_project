from datetime import datetime

from pydantic import BaseModel


class IdDTOMixin(BaseModel):
    id: int | None = None


class CreatedAtDTOMixin(BaseModel):
    created_at: datetime | None = None


class UpdatedAtDTOMixin(BaseModel):
    updated_at: datetime | None = None


class CreateUpdateDTOMixin(CreatedAtDTOMixin, UpdatedAtDTOMixin, BaseModel):
    pass


class CommonDTOMixin(IdDTOMixin, CreateUpdateDTOMixin, BaseModel):
    pass
