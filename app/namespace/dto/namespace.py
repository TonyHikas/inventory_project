from functools import reduce

from pydantic import BaseModel

from app.namespace.persistence.models import RightEnum
from framework.dto.mixin import CommonDTOMixin, IdDTOMixin


class RoleDTO(BaseModel, IdDTOMixin):
    name: str | None = None
    rights: list[RightEnum] | None = None

class NamespaceDTO(BaseModel, CommonDTOMixin):
    name: str | None = None
    roles: list[RoleDTO] | None = None

    def get_rights(self) -> list[RightEnum]:
        """Return unique names of all rights."""
        rights = reduce(lambda x, y: x.append(y), [role.rights for role in self.roles])
        return list(set(rights))

    def check_rights(self, rights: list[RightEnum]) -> bool:
        """Check containing all rights."""
        return set(rights).issubset(self.get_rights())


class UserNamespaceWithRoleDTO(BaseModel, CommonDTOMixin):  # todo
    namespace_name: str
    role_name: str
