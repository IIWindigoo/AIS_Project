from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from app.users.schemas import SUserShort
from app.subscriptions.schemas import SSubInfo


class SSubReqCreate(BaseModel):
    subscription_id: int = Field(description="ID абонемента")

class SSubReqUpdate(BaseModel):
    status: str = Field(description="Статус заявки")

class SSubReqInfo(BaseModel):
    id: int = Field(description="ID заявки")
    user_id: int = Field(description="ID клиента")
    subscription_id: int = Field(description="ID абонемента")
    status: str = Field(description="Статус заявки")
    created_at: datetime = Field(description="Дата создания заявки")

    model_config = ConfigDict(from_attributes=True)

class SSubReqInfoFull(BaseModel):
    id: int = Field(description="ID заявки")
    status: str = Field(description="Статус заявки")
    user: SUserShort = Field(description="Информация о клиенте")
    subscription: SSubInfo = Field(description="Информация об абонементе")
    created_at: datetime = Field(description="Дата создания заявки")

    model_config = ConfigDict(from_attributes=True)

class SSubReqFilter(BaseModel):
    id: int = Field(description="ID заявки")

class MembershipBase(BaseModel):
    user_id: int | None = Field(default=None, description="ID клиента")
    subscription_id: int | None = Field(default=None, description="ID абонемента")
    start_date: date | None = Field(default=None, description="Дата начала действия абонемента")
    end_date: date | None = Field(default=None, description="Дата окончания действия абонемента")
    status: str | None = Field(default=None, description="Статус абонемента. Активен или нет")

class SMembershipCreate(MembershipBase):
    user_id: int = Field(description="ID клиента")
    subscription_id: int = Field(description="ID абонемента")

class SMembershipInfo(MembershipBase):
    id: int = Field(description="ID")

    model_config = ConfigDict(from_attributes=True)

class SFilter(BaseModel):
    user_id: int = Field(description="ID клиента")
    status: str = Field(description="Статус заявки/абонемента")
