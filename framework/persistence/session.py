from contextlib import asynccontextmanager
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


@asynccontextmanager
async def get_context_session(session: sessionmaker):
    """Auto commit on success and rollback on error"""
    try:
        async with session:
            async with session.begin():
                yield session
    except Exception as ex:
        await session.rollback()
        raise ex
    finally:
        await session.commit()


@lru_cache
def get_sessionmaker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(
        engine.execution_options(),
        expire_on_commit=False,
        class_=AsyncSession
    )


def get_async_engine(dns: str):
    return create_async_engine(dns=dns)
