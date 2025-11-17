from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.dao.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    training_id: Mapped[int] = mapped_column(ForeignKey("trainings.id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("user_id", "training_id", name="uq_user_training"),
    )

    user: Mapped["User"] = relationship(back_populates="bookings") # type: ignore
    training: Mapped["Training"] = relationship(back_populates="bookings") # type: ignore

    def __repr__(self):
        return (f"{self.__class__.__name__}(id={self.id}, training_id={self.training_id}, "
                f"user_id={self.user_id}")