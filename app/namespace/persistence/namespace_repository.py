import abc

from sqlalchemy import select, exists, insert, func, update, delete

from app.namespace.dto.namespace import NamespaceDTO, RoleDTO, UserNamespaceWithRoleDTO
from app.namespace.exceptions import NamespaceNotFoundException, NamespacePermissionDeniedException, \
    RoleNotFoundException
from app.namespace.persistence.models import Namespace, RightEnum, UserNamespace, Role
from framework.persistence.base_repository import BaseRepository, ABCBaseRepository


class ABCNamespaceRepository(ABCBaseRepository, abc.ABC):

    @abc.abstractmethod
    async def get_one(self, namespace_id: int, user_id: int) -> NamespaceDTO:
        pass

    @abc.abstractmethod
    async def get_list(
            self,
            user_id: int,
            rights: list[RightEnum]
    ) -> list[UserNamespaceWithRoleDTO]:
        pass

    @abc.abstractmethod
    async def create(
            self,
            namespace: NamespaceDTO,
            user_id: int,
            role_slug: str
    ) -> int:
        pass

    @abc.abstractmethod
    async def update(self, namespace: NamespaceDTO) -> None:
        pass

    @abc.abstractmethod
    async def delete(self, namespace_id: int) -> None:
        pass

    @abc.abstractmethod
    async def check_rights(
            self,
            user_id: int,
            namespace_id: int,
            rights: list[RightEnum]
    ) -> bool:
        pass

    @abc.abstractmethod
    async def get_roles(
            self,
            user_id: int,
            namespace_id: int
    ) -> list[RoleDTO]:
        pass

    @abc.abstractmethod
    async def add_user_role(
            self,
            user_id: int,
            namespace_id: int,
            role_id: int
    ):
        pass

    @abc.abstractmethod
    async def remove_user_role(
            self,
            user_id: int,
            namespace_id: int,
            role_id: int
    ):
        pass

    @abc.abstractmethod
    async def get_all_roles(self) -> list[RoleDTO]:
        pass


class NamespaceRepository(ABCNamespaceRepository, BaseRepository):

    async def get_one(self, namespace_id: int, user_id: int) -> NamespaceDTO:
        async with self.ro_session() as session:
            stmt = select(
                Namespace.id,
                Namespace.name,
                Namespace.created_at,
                Namespace.updated_at
            ).where(
                Namespace.id == namespace_id
            )
            result = await session.execute(stmt)
            row = result.first()
        if row is None:
            raise NamespaceNotFoundException
        namespace_dto = NamespaceDTO.parse_obj(row)
        roles = await self.get_roles(user_id, namespace_id)
        namespace_dto.roles = roles

        if not namespace_dto.check_rights([RightEnum.VIEW]):
            raise NamespacePermissionDeniedException

        return namespace_dto

    async def get_list(
            self,
            user_id: int,
            rights: list[RightEnum]
    ) -> list[UserNamespaceWithRoleDTO]:
        async with self.ro_session() as session:
            stmt = select(
                Namespace.id.label('namespace_id'),
                Namespace.name.label('namespace_name'),
                Namespace.created_at.label('namespace_created_at'),
                Namespace.updated_at.label('namespace_updated_at'),
                Role.id.label('role_id'),
                Role.name.label('role_name'),
                Role.rights.label('role_rights')
            ).select_from(
                UserNamespace.__table__.join(Namespace).join(Role)
            ).where(
                UserNamespace.user_id == user_id,
                Role.rights.comparator.contains(rights)
            )

            result = await session.execute(stmt)
        return [
            UserNamespaceWithRoleDTO.parse_obj(row) for row in result
        ]

    async def create(
            self,
            namespace: NamespaceDTO,
            user_id: int,
            role_slug: str
    ) -> int:
        """Create Namespace and UserNamespace with role. Returning namespace id."""
        async with self.ro_session() as session:
            stmt = select(
                Role.id,
            ).where(
                Role.slug == role_slug
            )
            result = await session.execute(stmt)
            role_row = result.first()
        if role_row is None:
            raise RoleNotFoundException

        async with self.session() as session:
            stmt = insert(
                Namespace
            ).values(
                name=namespace.name
            ).returning(
                Namespace.id
            )
            namespace_result = await session.execute(stmt)

            stmt = insert(
                UserNamespace
            ).values(
                namespace_id=func.currval('namespace_id_seq'),
                user_id=user_id,
                role_id=role_row.id
            )
            await session.execute(stmt)

        return namespace_result.first().id

    async def update(self, namespace: NamespaceDTO) -> None:
        async with self.session() as session:
            stmt = update(
                Namespace
            ).where(
                Namespace.id == namespace.id
            ).values(
                name=namespace.name
            )
            await session.execute(stmt)

    async def delete(self, namespace_id: int) -> None:
        async with self.session() as session:
            stmt = delete(
                Namespace
            ).where(
                Namespace.id == namespace_id
            )
            await session.execute(stmt)

    async def check_rights(
            self,
            user_id: int,
            namespace_id: int,
            rights: list[RightEnum]
    ) -> bool:
        async with self.ro_session() as session:
            stmt = exists(
                UserNamespace
            ).select_from(
                UserNamespace.__table__.join(Role)
            ).where(
                UserNamespace.user_id == user_id,
                UserNamespace.namespace_id == namespace_id,
                Role.rights.comparator.contains(rights)
            ).select()
            result = await session.execute(stmt)
        return result.scalars().first()

    async def get_roles(
            self,
            user_id: int,
            namespace_id: int
    ) -> list[RoleDTO]:
        async with self.ro_session() as session:
            stmt = select(
                Role.id,
                Role.name,
                Role.rights
            ).select_from(
                UserNamespace.__table__.join(Role)
            ).where(
                UserNamespace.user_id == user_id,
                UserNamespace.namespace_id == namespace_id,
            )
            result = await session.execute(stmt)
        return [
            RoleDTO.parse_obj(row) for row in result
        ]

    async def add_user_role(
            self,
            user_id: int,
            namespace_id: int,
            role_id: int
    ):
        async with self.session() as session:
            stmt = insert(
                UserNamespace
            ).values(
                namespace_id=namespace_id,
                user_id=user_id,
                role_id=role_id
            )
            await session.execute(stmt)

    async def remove_user_role(
            self,
            user_id: int,
            namespace_id: int,
            role_id: int
    ):
        async with self.session() as session:
            stmt = delete(
                UserNamespace
            ).where(
                UserNamespace.namespace_id == namespace_id,
                UserNamespace.user_id == user_id,
                UserNamespace.role_id == role_id
            )
            await session.execute(stmt)

    async def get_all_roles(self) -> list[RoleDTO]:
        async with self.ro_session() as session:
            stmt = select(
                Role.id,
                Role.name,
                Role.rights
            )
            result = await session.execute(stmt)
        return [
            RoleDTO.parse_obj(row) for row in result
        ]

