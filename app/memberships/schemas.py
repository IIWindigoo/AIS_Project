from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date
from app.users.schemas import SUserShort
from app.subscriptions.schemas import SSubInfo
from enum import Enum


class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class MembershipStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"

class SSubReqCreate(BaseModel):
    subscription_id: int = Field(description="ID абонемента")

class SSubReqAdd(SSubReqCreate):
    user_id: int = Field(description="ID клиента")

class SSubReqUpdate(BaseModel):
    status: RequestStatus = Field(description="Статус заявки")

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
    start_date: date | None = Field(default=None, description="Дата начала действия абонемента")
    end_date: date | None = Field(default=None, description="Дата окончания действия абонемента")
    status: str | None = Field(default=None, description="Статус абонемента. Активен или нет")

class SMembershipCreate(MembershipBase):
    user_id: int = Field(description="ID клиента")
    subscription_id: int = Field(description="ID абонемента")

class SMembershipInfo(MembershipBase):
    id: int = Field(description="ID")
    subscription_id: int = Field(description="ID абонемента")

    model_config = ConfigDict(from_attributes=True)

class SMembershipUpd(BaseModel):
    status: MembershipStatus | None = Field(default=None, description="Статус абонемента. Активен или нет")

class SMembershipFilter(BaseModel):
    user_id: int = Field(description="ID клиента")

class SMembershipInfoFull(MembershipBase):
    id: int = Field(description="ID абонемента")
    user: SUserShort = Field(description="Информация о клиенте")
    subscription: SSubInfo = Field(description="Информация об абонементе")
    created_at: datetime = Field(description="Дата создания записи")

    model_config = ConfigDict(from_attributes=True)

class SFilter(BaseModel):
    user_id: int = Field(description="ID клиента")
    status: str = Field(description="Статус заявки/абонемента")
