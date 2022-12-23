from sqlalchemy import Column, TIMESTAMP, func, Integer


class IdMixin:
    id = Column(Integer, primary_key=True)


class CreatedAtMixin:
    created_at = Column(TIMESTAMP(timezone=True), default=func.now(), nullable=True)


class UpdatedAtMixin:
    updated_at = Column(TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now(), nullable=True)


class CreateUpdateMixin(CreatedAtMixin, UpdatedAtMixin):
    pass


class CommonMixin(IdMixin, CreateUpdateMixin):
    pass
