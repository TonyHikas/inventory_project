import abc

from sqlalchemy import select, exists, insert

from app.namespace.dto.namespace import NamespaceDTO, RoleDTO
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
    ) -> list[NamespaceDTO]:
        pass

    @abc.abstractmethod
    async def create(
            self,
            namespace: NamespaceDTO,
            user_id: int,
            role_slug: str
    ) -> NamespaceDTO:
        pass

    # @abc.abstractmethod
    # async def update(self, namespace: NamespaceDTO) -> NamespaceDTO:
    #     pass
    #
    # @abc.abstractmethod
    # async def delete(self, namespace_id: int) -> NamespaceDTO:
    #     pass
    #
    # @abc.abstractmethod
    # async def check_rights(
    #         self,
    #         user_id: int,
    #         namespace_id: int,
    #         rights: list[RightEnum]
    # ) -> bool:
    #     """Return True if user has rights to namespace."""
    #     pass
    #
    # async def get_roles(
    #         self,
    #         user_id: int,
    #         namespace_id: int
    # ) -> list[RoleDTO]:
    #     pass
    #

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
    ) -> list[NamespaceDTO]:
        async with self.ro_session() as session:
            stmt = select(
                Namespace.id,
                Namespace.name,
                Namespace.created_at,
                Namespace.updated_at,
                Role.name,
                Role.rights
            ).select_from(
                UserNamespace.join(Namespace).join(Role)
            ).where(
                UserNamespace.user_id == user_id,
                Role.rights.comparator.contains(rights)  # todo check
            )

            result = await session.execute(stmt)
        return [
            NamespaceDTO.parse_obj(row) for row in result
        ]

    async def create(
            self,
            namespace: NamespaceDTO,
            user_id: int,
            role_slug: str
    ) -> NamespaceDTO:
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
            # todo transaction
            stmt = insert(
                Namespace
            ).values(
                name=namespace.name
            ).returning(
                Namespace.id,
                Namespace.name,
                Namespace.created_at,
                Namespace.updated_at
            )
            result = await session.execute(stmt)
            namespace_row = result.first()
            session.commit()

            stmt = insert(
                UserNamespace
            ).values(
                UserNamespace.namespace_id == namespace_row.id,
                UserNamespace.user_id == user_id,
                UserNamespace.role_id == role_row.id
            ).returning(
                Namespace.id,
                Namespace.name,
                Namespace.created_at,
                Namespace.updated_at
            )
            result = await session.execute(stmt)
            row = result.first()


        return [
            NamespaceDTO.parse_obj(row) for row in result
        ]


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
                UserNamespace.join(Role)
            ).where(
                UserNamespace.user_id == user_id,
                UserNamespace.namespace_id == namespace_id,
                Role.rights.comparator.contains(rights)  # todo check
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
                UserNamespace.join(Role)
            ).where(
                UserNamespace.user_id == user_id,
                UserNamespace.namespace_id == namespace_id,
            )
            result = await session.execute(stmt)
        return [
            Role.parse_obj(row) for row in result
        ]
