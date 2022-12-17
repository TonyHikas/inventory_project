from datetime import datetime

from pydantic import BaseModel

from app.item.dto.item import ItemTypeEnum, ItemUnitEnum


class ItemImageRequest(BaseModel):
    id: int | None
    url: str


class ItemRequest(BaseModel):
    name: str
    description: str
    type: ItemTypeEnum
    count: float
    unit: ItemUnitEnum
    namespace_id: int
    parent_id: int | None
    images: list[ItemImageRequest]


class ItemImageResponse(BaseModel):
    id: int
    url: str
    created_at: datetime
    updated_at: datetime


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    type: ItemTypeEnum
    count: float
    unit: ItemUnitEnum
    namespace_id: int
    parent_id: int | None
    created_at: datetime
    updated_at: datetime
    images: list[ItemImageResponse]
