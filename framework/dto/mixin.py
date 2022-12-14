from datetime import datetime


class IdDTOMixin:
    id: int | None = None


class CreatedAtDTOMixin:
    created_at: datetime | None = None


class UpdatedAtDTOMixin:
    updated_at: datetime | None = None


class CreateUpdateDTOMixin(CreatedAtDTOMixin, UpdatedAtDTOMixin):
    pass


class CommonDTOMixin(IdDTOMixin, CreateUpdateDTOMixin):
    pass
