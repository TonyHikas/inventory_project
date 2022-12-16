from fastapi import FastAPI, APIRouter

from app.auth.communication import auth_api
from app.user.communication import user_api
from app.namespace.communication import namespace_api
from app.item.communication import item_api

app = FastAPI(title='Api for inventory project by Anton.')

main_router = APIRouter(prefix='/api')
allow_any_router = APIRouter()
is_authenticated_router = APIRouter()  # todo add auth depend

# add modules routers here
is_authenticated_router.include_router(user_api.router)
is_authenticated_router.include_router(namespace_api.router)
is_authenticated_router.include_router(item_api.router)

allow_any_router.include_router(auth_api.router)

main_router.include_router(allow_any_router)
main_router.include_router(is_authenticated_router)

app.include_router(main_router)


@app.get('/')
async def root():
    return {'message': 'Wellcome to api!'}
