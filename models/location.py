from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.database import Base

class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=True)

    # Зв'язок з велосипедами: одна локація може мати багато велосипедів
    bicycles: Mapped[list["Bicycle"]] = relationship("Bicycle", back_populates="current_location")

    def __repr__(self):
        return f"<Location(id={self.id}, name='{self.name}')>"