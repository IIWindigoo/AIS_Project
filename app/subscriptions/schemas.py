from pydantic import BaseModel, Field


class SSubInfo(BaseModel):
    title: str = Field(min_length=2, max_length=30, description="Название абонемента, от 2 до 30 символов")
    price: int = Field(description="Цена абонемента в рублях, целые числа")
    duration_days: int = Field(description="Длительность абонемента в днях")

class SSubFilter(BaseModel):
    id: int = Field(description="ID помещения")

class SSubUpd(BaseModel):
    title: str | None = None
    price: int | None = None
    duration_days: int | None = None