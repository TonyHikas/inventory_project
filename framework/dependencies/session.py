from core.settings import settings
from framework.persistence.session import get_async_engine


async def rw_engine_dep():
    return get_async_engine(settings.postgres_full_rw_dns())

async def ro_engine_dep():
    return get_async_engine(settings.postgres_full_ro_dns())
