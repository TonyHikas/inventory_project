from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Enum

from app.item.dto.item import ItemUnitEnum, ItemTypeEnum
from framework.persistence.mixins import CommonMixin
from framework.persistence.models import Base


class Item(Base, CommonMixin):
    __tablename__ = 'item'

    name = Column(String(511), nullable=False)
    description = Column(String(3000), nullable=False)
    type = Column(Enum(ItemTypeEnum), nullable=False)
    count = Column(Numeric(10, 4))
    unit = Column(Enum(ItemUnitEnum), nullable=False)
    namespace_id = Column(
        Integer,
        ForeignKey('namespace.id', ondelete='CASCADE'),
        nullable=False
    )
    parent_id = Column(
        Integer,
        ForeignKey('item.id', ondelete='CASCADE'),
        nullable=True
    )


class ItemImage(Base, CommonMixin):
    __tablename__ = 'item_image'

    item_id = Column(
        Integer,
        ForeignKey('item.id', ondelete='CASCADE'),
        nullable=False
    )
    url = Column(String(3000), nullable=False)
