from sqlalchemy import Column, String, Integer, ForeignKey, Numeric

from framework.persistence.mixins import CommonMixin
from framework.persistence.models import Base


class Item(Base, CommonMixin):
    __tablename__ = 'item'

    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    type = Column(String, nullable=False)  # todo enum
    count = Column(Numeric(10, 4))
    unit = Column(String, nullable=False)  # todo enum единица измерения
    namespace_id = Column(
        Integer,
        ForeignKey('namespace.id', ondelete='CASCADE'),
        nullable=False
    )
    location_id = Column(
        Integer,
        ForeignKey('location.id', ondelete='CASCADE'),
        nullable=True
    )


class ItemImage(Base, CommonMixin):
    __tablename__ = 'item_image'

    item_id = Column(
        Integer,
        ForeignKey('item.id', ondelete='CASCADE'),
        nullable=False
    )
    url = Column(String, nullable=False)
