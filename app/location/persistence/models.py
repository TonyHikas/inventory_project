from sqlalchemy import Column, String, Integer, ForeignKey

from framework.persistence.mixins import CommonMixin
from framework.persistence.models import Base


class Location(Base, CommonMixin):
    __tablename__ = 'location'

    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    description = Column(String, nullable=False)
    namespace_id = Column(
        Integer,
        ForeignKey('namespace.id', ondelete='CASCADE'),
        nullable=False
    )
