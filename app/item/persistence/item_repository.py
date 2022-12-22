import abc

from sqlalchemy import select, insert, func, delete, update

from app.item.dto.item import ItemDTO, ItemImageDTO
from app.item.exceptions import ItemNotFoundException
from app.item.persistence.models import Item, ItemImage
from app.movement.persistence.models import ItemMovement
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
            namespace_id: int,
            limit: int | None = None,
            offset: int | None = None
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
        async with self.session() as session:
            item_stmt = select(
                Item.id,
                Item.name,
                Item.description,
                Item.type,
                Item.count,
                Item.unit,
                Item.namespace_id,
                Item.parent_id,
                Item.created_at,
                Item.updated_at
            ).where(
                Item.id == item_id
            )
            item_result = await session.execute(item_stmt)
            item_row = item_result.first()
            images_stmt = select(
                ItemImage.id,
                ItemImage.url,
                ItemImage.created_at,
                ItemImage.updated_at
            ).where(
                ItemImage.item_id == item_id
            )
            images_result = await session.execute(images_stmt)

        if item_row is None:
            raise ItemNotFoundException

        item_dto = ItemDTO.parse_obj(item_row)
        item_dto.images = []
        for image_row in images_result:
            item_dto.images.append(
                ItemImageDTO.parse_obj(image_row)
            )

        return item_dto

    async def get_list(
            self,
            namespace_id: int,
            limit: int | None = None,
            offset: int | None = None
    ) -> list[ItemDTO]:
        result_dict: dict[int, ItemDTO] = {}
        item_ids: list[int] = []
        async with self.ro_session() as session:
            items_stmt = select(
                Item.id,
                Item.name,
                Item.description,
                Item.type,
                Item.count,
                Item.unit,
                Item.namespace_id,
                Item.parent_id,
                Item.created_at,
                Item.updated_at
            ).where(
                Item.namespace_id == namespace_id
            )

            if limit is not None:
                items_stmt = items_stmt.limit(limit)
            if offset is not None:
                items_stmt = items_stmt.offset(offset)

            items_result = await session.execute(items_stmt)

            for item_row in items_result:
                result_dict[item_row.id] = ItemDTO.parse_obj(item_row)
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

            if item.parent_id is not None:
                item_stmt = insert(
                    ItemMovement
                ).values(
                    item_id=func.currval('item_id_seq'),
                    from_item_id=None,
                    to_item_id=item.parent_id
                )
                await session.execute(item_stmt)

        return item_result.first().id

    async def update(self, item: ItemDTO) -> None:
        item_before = await self.get_one(item.id)
        async with self.session() as session:
            existing_images_ids: list[int] = []
            updated_images_ids: list[int] = []
            images_stmt = select(
                ItemImage.id,
                ItemImage.url,
                ItemImage.created_at,
                ItemImage.updated_at
            ).where(
                ItemImage.item_id == item.id
            )
            images_result = await session.execute(images_stmt)
            for image_row in images_result:
                existing_images_ids.append(image_row.id)

            item_stmt = update(
                Item
            ).where(
                Item.id == item.id
            ).values(
                name=item.name,
                description=item.description,
                type=item.type,
                count=item.count,
                unit=item.unit,
                parent_id=item.parent_id
            )
            item_result = await session.execute(item_stmt)

            for image_dto in (item.images or []):
                if image_dto.id is None:
                    insert_image_stmt = insert(
                        ItemImage
                    ).values(
                        item_id=item.id,
                        url=image_dto.url
                    )
                    await session.execute(insert_image_stmt)
                else:
                    updated_images_ids.append(image_dto.id)
                    update_image_stmt = update(
                        ItemImage
                    ).where(
                        ItemImage.item_id == item.id,
                        ItemImage.id == image_dto.id
                    ).values(
                        url=image_dto.url
                    )
                    await session.execute(update_image_stmt)

            for existing_image_id in existing_images_ids:
                if existing_image_id not in updated_images_ids:
                    delete_image_stmt = delete(
                        ItemImage
                    ).where(
                        ItemImage.item_id == item.id,
                        ItemImage.id == existing_image_id
                    )
                    await session.execute(delete_image_stmt)

            if item.parent_id != item_before.parent_id:
                item_stmt = insert(
                    ItemMovement
                ).values(
                    item_id=item.id,
                    from_item_id=item_before.parent_id,
                    to_item_id=item.parent_id
                )
                await session.execute(item_stmt)

    async def delete(self, item_id: int) -> None:
        async with self.session() as session:
            stmt = delete(
                Item
            ).where(
                Item.id == item_id
            )
            await session.execute(stmt)
