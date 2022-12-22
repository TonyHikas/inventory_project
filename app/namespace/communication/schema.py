from datetime import datetime

from pydantic import BaseModel


class NamespaceRequest(BaseModel):
    name: str

class RoleResponse(BaseModel):
    id: int
    name: str
    rights: list[str]

class NamespaceResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    roles: list[RoleResponse]

class NamespaceEditRoleRequest(BaseModel):
    user_id: int
    role_id: int
