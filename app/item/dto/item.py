import enum

from pydantic import BaseModel

from framework.dto.mixin import CommonDTOMixin


class ItemTypeEnum(str, enum.Enum):
    OBJECT = 'OBJECT'
    STORAGE = 'STORAGE'

class ItemUnitEnum(str, enum.Enum):
    PCS = 'PCS'
    KGS = 'KGS'

class ItemImageDTO(CommonDTOMixin, BaseModel):
    url: str | None = None

class ItemDTO(CommonDTOMixin, BaseModel):
    name: str | None = None
    description: str | None = None
    type: str | None = None
    count: float | None = None
    unit: ItemUnitEnum | None = None
    namespace_id: int | None = None
    parent_id: int | None = None
    images: list[ItemImageDTO] | None = None
