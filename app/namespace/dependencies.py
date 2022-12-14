from fastapi import Depends

from app.namespace.persistence.namespace_repository import NamespaceRepository
from app.namespace.services.namespace_service import NamespaceService
from framework.dependencies.session import rw_engine_dep, ro_engine_dep


async def namespace_repository_dep(
        rw_engine=Depends(rw_engine_dep),
        ro_engine=Depends(ro_engine_dep)
):
    return NamespaceRepository(rw_engine, ro_engine)


async def namespace_service_dep(
        namespace_repository=Depends(namespace_repository_dep)
):
    return NamespaceService(namespace_repository)
