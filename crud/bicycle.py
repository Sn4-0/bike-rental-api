from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Annotated
from fastapi import Depends

from db.database import get_db
from models.bicycle import Bicycle
from models.location import Location
from schemas.bicycle import BicycleCreate, BicycleUpdate

class BicycleRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_bicycle(self, bicycle_id: int) -> Optional[Bicycle]:
        return self.db.query(Bicycle).filter(Bicycle.id == bicycle_id).first()

    def get_bicycles(self) -> List[Bicycle]:
        return self.db.query(Bicycle).all()

    def get_bicycles_by_location(self, location_id: int) -> List[Bicycle]:
        return self.db.query(Bicycle).filter(Bicycle.current_location_id == location_id).all()

    def get_bicycles_by_status(self, status: str) -> List[Bicycle]:
        return self.db.query(Bicycle).filter(Bicycle.status == status).all()

    def create_bicycle(self, bicycle: BicycleCreate) -> Bicycle:
        if bicycle.current_location_id is not None:
            location = self.db.query(Location).filter(Location.id == bicycle.current_location_id).first()
            if not location:
                raise ValueError(f"Location with ID {bicycle.current_location_id} does not exist.")

        db_bicycle = Bicycle(**bicycle.model_dump())
        self.db.add(db_bicycle)
        self.db.commit()
        self.db.refresh(db_bicycle)
        return db_bicycle

    def update_bicycle(self, bicycle_id: int, bicycle_update: BicycleUpdate) -> Optional[Bicycle]:
        db_bicycle = self.get_bicycle(bicycle_id)
        if db_bicycle:
            update_data = bicycle_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                if key == "current_location_id" and value is not None:
                    location = self.db.query(Location).filter(Location.id == value).first()
                    if not location:
                        raise ValueError(f"Location with ID {value} does not exist for update.")
                setattr(db_bicycle, key, value)
            self.db.add(db_bicycle)
            self.db.commit()
            self.db.refresh(db_bicycle)
            return db_bicycle
        return None

    def delete_bicycle(self, bicycle_id: int) -> bool:
        db_bicycle = self.get_bicycle(bicycle_id)
        if db_bicycle:
            self.db.delete(db_bicycle)
            self.db.commit()
            return True
        return False

    def get_most_rented_bicycle(self) -> Optional[Bicycle]:
        from models.rental import Rental
        result = self.db.query(Bicycle, func.count(Rental.id).label("rental_count")).join(Rental).group_by(Bicycle.id).order_by(func.count(Rental.id).desc()).first()

        if result:
            return result.Bicycle
        return None

BicycleRepositoryDependency = Annotated[BicycleRepository, Depends]