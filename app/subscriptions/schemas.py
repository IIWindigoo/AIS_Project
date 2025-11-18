from pydantic import BaseModel, Field, ConfigDict


class SSubAdd(BaseModel):
    title: str = Field(min_length=2, max_length=30, description="Название абонемента, от 2 до 30 символов")
    price: int = Field(description="Цена абонемента в рублях, целые числа")
    duration_days: int = Field(description="Длительность абонемента в днях")

    model_config = ConfigDict(from_attributes=True)

class SSubInfo(SSubAdd):
    id: int = Field(description="ID абонемента")
    
class SSubFilter(BaseModel):
    id: int = Field(description="ID абонемента")

class SSubUpd(BaseModel):
    title: str | None = None
    price: int | None = None
    duration_days: int | None = None