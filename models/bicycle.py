from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.database import Base

class Bicycle(Base):
    __tablename__ = "bicycles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    price_per_hour: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String, default="доступний", nullable=False)

    current_location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id"), nullable=True)

    # Використання relationship
    current_location: Mapped["Location"] = relationship("Location", back_populates="bicycles")
    rentals: Mapped[list["Rental"]] = relationship("Rental", back_populates="bicycle")

    def __repr__(self):
        return f"<Bicycle(id={self.id}, brand='{self.brand}', model='{self.model}')>"