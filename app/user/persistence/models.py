from sqlalchemy import Column, Integer, String

from framework.persistence.mixins import CommonMixin
from framework.persistence.models import Base


class User(Base, CommonMixin):
    __tablename__ = 'user'

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
