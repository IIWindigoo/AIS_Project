from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.dao.database import Base


class Membership(Base):
    __tablename__ = "memberships"

    start_date: Mapped[date]
    end_date: Mapped[date]
    status: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="membership") # type: ignore
    subscription: Mapped["Subscription"] = relationship(back_populates="memberships") # type: ignore
    
    def __repr__(self):
        return (f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id}, start_date={self.start_date}, "
                f"end_date={self.end_date}, status={self.status}, subscription_id={self.subscription_id})")
    
class SubRequest(Base):
    __tablename__ = "sub_requests"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    subscription_id: Mapped[int] = mapped_column(ForeignKey("subscriptions.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(default="pending", server_default=text("'pending'"))

    user: Mapped["User"] = relationship(back_populates="sub_requests") # type: ignore
    subscription: Mapped["Subscription"] = relationship(back_populates="sub_requests") # type: ignore