from pydantic import BaseModel, ConfigDict, Field


class SRoomInfo(BaseModel):
    title: str = Field(min_length=2, max_length=30, description="Название помещения, от 2 до 30 символов")
    capacity: int = Field(description="Вместимость помещения")

class SRoomFilter(BaseModel):
    id: int = Field(description="ID помещения")

class SRoomUpd(BaseModel):
    title: str | None = None
    capacity: int | None = None