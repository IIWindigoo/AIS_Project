from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import time, date
from app.dao.database import Base


class Training(Base):
    __tablename__ = "trainings"

    title: Mapped[str]
    description: Mapped[str] = mapped_column(Text)
    date: Mapped[date]
    start_time: Mapped[time]
    end_time: Mapped[time]
    trainer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"))
    
    room: Mapped["Room"] = relationship(back_populates="trainings") # type: ignore
    trainer: Mapped["User"] = relationship(back_populates="trainings") # type: ignore
    bookings: Mapped[list["Booking"]] = relationship(back_populates="training", cascade="all, delete-orphan") # type: ignore

    def __repr__(self):
        return (f"{self.__class__.__name__}(id={self.id}, title={self.title}, description={self.description}, "
                f"date={self.date}, start_time={self.start_time}, end_time={self.end_time})")