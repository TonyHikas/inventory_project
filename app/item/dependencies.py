from fastapi import Depends

from app.item.persistence.item_repository import ItemRepository
from app.item.services.item_service import ItemService
from app.namespace.dependencies import namespace_service_dep
from framework.dependencies.session import rw_engine_dep, ro_engine_dep


async def item_repository_dep(
        rw_engine=Depends(rw_engine_dep),
        ro_engine=Depends(ro_engine_dep)
):
    return ItemRepository(rw_engine, ro_engine)


async def item_service_dep(
        item_repository=Depends(item_repository_dep),
        namespace_service=Depends(namespace_service_dep)
):
    return ItemService(
        item_repository=item_repository,
        namespace_service=namespace_service
    )
