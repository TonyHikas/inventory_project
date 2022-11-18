from fastapi import FastAPI, APIRouter

from app.auth.communication import auth_api
from app.user.communication import user_api
from core.db import database

app = FastAPI(title='Api for an appointment in a hairdressing salon chain.')

allow_any_router = APIRouter()
is_authenticated_router = APIRouter()  # todo add auth depend

# add modules routers here
is_authenticated_router.include_router(user_api.router, prefix='/users', tags=['users'])
allow_any_router.include_router(auth_api.router, prefix='/auth', tags=['auth'])

app.include_router(allow_any_router)
app.include_router(is_authenticated_router)

@app.get('/')
async def root():
    return {'message': 'Wellcome to api!'}

@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
