from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import time, date
from app.dao.database import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    title: Mapped[str]
    price: Mapped[int]
    duration_days: Mapped[int]

    memberships: Mapped[list["Membership"]] = relationship(back_populates="subscription", cascade="all, delete-orphan") # type: ignore
    sub_requests: Mapped[list["SubRequest"]] = relationship(back_populates="subscription", cascade="all, delete-orphan") # type: ignore

    def __repr__(self):
        return (f"{self.__class__.__name__}(id={self.id}, title={self.title}, price={self.price}, "
                f"duration_days={self.duration_days})")