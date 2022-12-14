from sqlalchemy import Column, String

from framework.persistence.mixins import CommonMixin
from framework.persistence.models import Base


class User(Base, CommonMixin):
    __tablename__ = 'user'

    email = Column(String(255), nullable=False, unique=True)
    password = Column(String, nullable=False)
