from sqlalchemy import Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.database import Base
from datetime import datetime

class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    bicycle_id: Mapped[int] = mapped_column(Integer, ForeignKey("bicycles.id"), nullable=False)
    rental_start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    rental_end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    actual_return_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    discount_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("discounts.id"), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="rentals")
    bicycle: Mapped["Bicycle"] = relationship("Bicycle", back_populates="rentals")
    discount: Mapped["Discount"] = relationship("Discount", back_populates="rentals")

    def __repr__(self):
        return f"<Rental(id={self.id}, user_id={self.user_id}, bicycle_id={self.bicycle_id})>"