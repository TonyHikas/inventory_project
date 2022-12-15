from datetime import datetime
from functools import reduce

from pydantic import BaseModel

from app.namespace.persistence.models import RightEnum
from framework.dto.mixin import CommonDTOMixin, IdDTOMixin


class RoleDTO(IdDTOMixin, BaseModel):
    name: str | None = None
    rights: list[RightEnum] | None = None

class NamespaceDTO(CommonDTOMixin, BaseModel):
    name: str | None = None
    roles: list[RoleDTO] | None = None

    def get_rights(self) -> list[RightEnum]:
        """Return unique names of all rights."""
        if self.roles is None or len(self.roles) == 0:
            return []
        rights = reduce(lambda x, y: x.append(y), [role.rights for role in self.roles])
        return list(set(rights))

    def check_rights(self, rights: list[RightEnum]) -> bool:
        """Check containing all rights."""
        return set(rights).issubset(self.get_rights())


class UserNamespaceWithRoleDTO(BaseModel):
    namespace_id: int | None = None
    namespace_name: str | None = None
    namespace_created_at: datetime | None = None
    namespace_updated_at: datetime | None = None
    role_id: int | None = None
    role_name: str | None = None
    role_rights: list[RightEnum] | None = None
