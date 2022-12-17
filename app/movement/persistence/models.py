from sqlalchemy import Column, Integer, ForeignKey

from framework.persistence.mixins import CommonMixin
from framework.persistence.models import Base


class ItemMovement(Base, CommonMixin):
    __tablename__ = 'item_movement'

    item_id = Column(
        Integer,
        ForeignKey('item.id', ondelete='CASCADE'),
        nullable=False
    )
    from_item_id = Column(
        Integer,
        ForeignKey('item.id', ondelete='CASCADE'),
        nullable=True
    )
    to_item_id = Column(
        Integer,
        ForeignKey('item.id', ondelete='CASCADE'),
        nullable=True
    )
