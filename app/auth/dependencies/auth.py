from app.auth.services.auth_service import AuthService


async def auth_service_dep():
    return AuthService()
