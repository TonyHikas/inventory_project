import abc

from sqlalchemy.ext.asyncio import AsyncEngine

from framework.persistence.session import get_context_session, get_sessionmaker


class ABCBaseRepository(abc.ABC):

    @abc.abstractmethod
    def __init__(self, rw_engine: AsyncEngine, ro_engine: AsyncEngine) -> None:
        pass

    @abc.abstractmethod
    def session(self):
        pass

    @abc.abstractmethod
    def ro_session(self):
        pass

class BaseRepository(ABCBaseRepository):
    def __init__(self, rw_engine: AsyncEngine, ro_engine: AsyncEngine) -> None:
        self.rw_engine = rw_engine
        self.ro_engine = ro_engine

    def session(self):
        return get_context_session(get_sessionmaker(self.rw_engine)())

    def ro_session(self):
        return get_context_session(get_sessionmaker(self.ro_engine)())
