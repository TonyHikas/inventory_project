from sqlalchemy import Column, String, Integer, ForeignKey

from framework.persistence.mixins import CommonMixin
from framework.persistence.models import Base


class ItemMovement(Base, CommonMixin):
    __tablename__ = 'item_movement'

    item_id = Column(
        Integer,
        ForeignKey('item.id', ondelete='CASCADE'),
        nullable=False
    )
    location_from_id = Column(
        Integer,
        ForeignKey('location.id', ondelete='CASCADE'),
        nullable=False
    )
    location_to_id = Column(
        Integer,
        ForeignKey('location.id', ondelete='CASCADE'),
        nullable=False
    )
