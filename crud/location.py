from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Annotated
from fastapi import Depends

from db.database import get_db
from models.location import Location
from models.rental import Rental
from models.bicycle import Bicycle
from schemas.location import LocationCreate, LocationUpdate


class LocationRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_location(self, location_id: int) -> Optional[Location]:
        return self.db.query(Location).filter(Location.id == location_id).first()

    def get_locations(self) -> List[Location]:
        return self.db.query(Location).all()

    def create_location(self, location: LocationCreate) -> Location:
        db_location = Location(**location.model_dump())
        self.db.add(db_location)
        self.db.commit()
        self.db.refresh(db_location)
        return db_location

    def update_location(self, location_id: int, location_update: LocationUpdate) -> Optional[Location]:
        db_location = self.get_location(location_id)
        if db_location:
            update_data = location_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_location, key, value)
            self.db.add(db_location)
            self.db.commit()
            self.db.refresh(db_location)
            return db_location
        return None

    def delete_location(self, location_id: int) -> bool:
        db_location = self.get_location(location_id)
        if db_location:
            self.db.delete(db_location)
            self.db.commit()
            return True
        return False

    def get_top_performing_locations(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, limit: int = 5) -> List[Location]:
        query = self.db.query(
            Location,
            func.count(Rental.id).label("rental_count")
        ).join(Bicycle, Location.id == Bicycle.current_location_id)\
        .join(Rental, Bicycle.id == Rental.bicycle_id)

        if start_date:
            query = query.filter(Rental.rental_start_time >= start_date)
        if end_date:
            query = query.filter(Rental.rental_start_time <= end_date)

        results = query.group_by(Location.id).order_by(func.count(Rental.id).desc()).limit(limit).all()
        return [result.Location for result in results]

LocationRepositoryDependency = Annotated[LocationRepository, Depends]