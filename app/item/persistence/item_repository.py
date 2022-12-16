import abc

from sqlalchemy import select, insert, func, update, delete

from app.item.dto.item import ItemDTO, ItemImageDTO
from app.item.persistence.models import Item, ItemImage
from app.namespace.dto.namespace import NamespaceDTO
from app.namespace.exceptions import NamespaceNotFoundException, RoleNotFoundException
from app.namespace.persistence.models import Namespace, UserNamespace, Role
from framework.persistence.base_repository import BaseRepository, ABCBaseRepository


class ABCItemRepository(ABCBaseRepository, abc.ABC):

    @abc.abstractmethod
    async def get_one(
            self,
            item_id: int
    ) -> ItemDTO:
        pass

    @abc.abstractmethod
    async def get_list(
            self,
            namespace_id: int
    ) -> list[ItemDTO]:
        pass

    @abc.abstractmethod
    async def create(
            self,
            item: ItemDTO
    ) -> int:
        pass

    @abc.abstractmethod
    async def update(self, item: ItemDTO) -> None:
        pass

    @abc.abstractmethod
    async def delete(self, item_id: int) -> None:
        pass


class ItemRepository(ABCItemRepository, BaseRepository):

    async def get_one(
            self,
            item_id: int
    ) -> ItemDTO:
        async with self.ro_session() as session:
            stmt = select(
                Item.id,
                Item.name,
                # todo
                Item.created_at,
                Item.updated_at
            ).where(
                Item.id == item_id
            )
            item_result = await session.execute(stmt)
            item_row = item_result.first()
            stmt = select(
                ItemImage.id,
                ItemImage.url,
                ItemImage.created_at,
                ItemImage.updated_at
            ).where(
                ItemImage.item_id == item_id
            )
            images_result = await session.execute(stmt)

        if item_row is None:
            raise NamespaceNotFoundException

        item_dto = ItemDTO.parse_obj(item_row)
        item_dto.images = []
        for image_row in images_result:
            item_dto.images.append(
                ItemImageDTO.parse_obj(image_row)
            )

        return item_dto

    async def get_list(
            self,
            namespace_id: int
    ) -> list[ItemDTO]:
        result_dict: dict[int, ItemDTO] = {}
        item_ids: list[int] = []
        async with self.ro_session() as session:
            items_stmt = select(
                Item.id,
                Item.name,
                # todo
                Item.created_at,
                Item.updated_at
            ).where(
                Item.namespace_id == namespace_id
            )
            items_result = await session.execute(items_stmt)

            for item_row in items_result:
                result_dict[item_row.id] = ItemDTO.parse_obj(**item_row)
                result_dict[item_row.id].images = []
                item_ids.append(item_row.id)

            images_stmt = select(
                ItemImage.id,
                ItemImage.url,
                ItemImage.created_at,
                ItemImage.updated_at
            ).where(
                ItemImage.item_id.in_(item_ids)
            )
            images_result = await session.execute(images_stmt)
            for image_row in images_result:
                result_dict[image_row.id].images.append(
                    ItemImageDTO.parse_obj(image_row)
                )

        return list(result_dict.values())

    async def create(
            self,
            item: ItemDTO
    ) -> int:
        async with self.session() as session:
            item_stmt = insert(
                Item
            ).values(
                name=item.name,
                description=item.description,
                type=item.type,
                count=item.count,
                unit=item.unit,
                namespace_id=item.namespace_id,
                parent_id=item.parent_id
            ).returning(
                Item.id
            )
            item_result = await session.execute(item_stmt)

            for image_dto in (item.images or []):
                image_stmt = insert(
                    ItemImage
                ).values(
                    item_id=func.currval('item_id_seq'),
                    url=image_dto.url
                )
                await session.execute(image_stmt)

        return item_result.first().id

    async def update(self, item: ItemDTO) -> None:
        pass

    async def delete(self, item_id: int) -> None:
        async with self.session() as session:
            stmt = delete(
                Item
            ).where(
                Item.id == item_id
            )
            await session.execute(stmt)

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
