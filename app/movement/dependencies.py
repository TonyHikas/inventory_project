from fastapi import Depends

from app.movement.persistence.movement_repository import MovementRepository
from app.movement.services.movement_service import MovementService
from framework.dependencies.session import rw_engine_dep, ro_engine_dep


async def movement_repository_dep(
        rw_engine=Depends(rw_engine_dep),
        ro_engine=Depends(ro_engine_dep)
):
    return MovementRepository(rw_engine, ro_engine)


async def movement_service_dep(
        movement_repository=Depends(movement_repository_dep),
):
    return MovementService(
        movement_repository=movement_repository
    )
