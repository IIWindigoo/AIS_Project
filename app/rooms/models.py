from sqlalchemy.orm import Mapped, relationship
from app.dao.database import Base


class Room(Base):
    __tablename__ = "rooms"
    
    title: Mapped[str]
    capacity: Mapped[int]
    
    trainings: Mapped[list["Training"]] = relationship(back_populates="room", cascade="all, delete-orphan") # type: ignore

    def __repr__(self):
        return (f"{self.__class__.__name__}(id={self.id}, title={self.title}, capacity={self.capacity})")