from pydantic import BaseModel, Field, ConfigDict
from datetime import time, date as dt

from app.users.schemas import SUserShort


class TrainingBase(BaseModel):
    title: str = Field(min_length=2, max_length=50, description="Название тренировки, от 2 до 50 символов")
    description: str = Field(min_length=5, max_length=256, description="Описание тренировки, от 5 до 256 символов")
    date: dt = Field(description="Дата проведения тренировки")
    start_time: time = Field(description="Время начала тренировки")
    end_time: time = Field(description="Время окончания тренировки")

    model_config = ConfigDict(from_attributes=True)

class STrainingAdd(TrainingBase):
    trainer_id: int = Field(description="ID тренера")
    room_id: int = Field(description="ID помещения")

class STrainingInfo(TrainingBase):
    id: int = Field(description="ID тренировки")
    trainer_id: int = Field(description="ID тренера")
    room_id: int = Field(description="ID помещения")

class STrainingFilter(BaseModel):
    id: int = Field(description="ID тренировки")

class STrainingUpd(BaseModel):
    title: str | None = None
    description: str | None = None
    date: dt | None = None 
    start_time: time | None = None
    end_time: time | None = None

    model_config = ConfigDict(from_attributes=True)

class STrainingShort(BaseModel):
    id: int = Field(description="ID тренировки")
    title: str = Field(min_length=2, max_length=50, description="Название тренировки, от 2 до 50 символов")
    date: dt = Field(description="Дата проведения тренировки")
    start_time: time = Field(description="Время начала тренировки")
    end_time: time = Field(description="Время окончания тренировки")

    model_config = ConfigDict(from_attributes=True)

class SBookingWithUser(BaseModel):
    id: int = Field(description="ID бронирования")
    user: SUserShort = Field(description="Клиент")
    
    model_config = ConfigDict(from_attributes=True)

class STrainingWithBookings(STrainingShort):
    bookings: list[SBookingWithUser] = Field(default=[], description="Список бронирований")
