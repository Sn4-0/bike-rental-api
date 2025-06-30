from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Annotated
from datetime import datetime
from fastapi import Depends

from db.database import get_db

from models.rental import Rental as DBRental
from schemas.rental import RentalCreate, RentalUpdate, Rental


class RentalRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_rental(self, rental_id: int) -> Optional[DBRental]:
        return self.db.query(DBRental).filter(DBRental.id == rental_id).first()

    def get_rentals(self) -> List[DBRental]:
        return self.db.query(DBRental).all()

    def get_rentals_by_user_id(self, user_id: int) -> List[DBRental]:
        return self.db.query(DBRental).filter(DBRental.user_id == user_id).all()

    def get_rentals_by_bicycle_id(self, bicycle_id: int) -> List[DBRental]:
        return self.db.query(DBRental).filter(DBRental.bicycle_id == bicycle_id).all()

    def get_rentals_by_time_range(self, start_time: datetime, end_time: datetime) -> List[DBRental]:
        return self.db.query(DBRental).filter(
            DBRental.rental_start_time >= start_time,
            DBRental.rental_end_time <= end_time
        ).all()

    def get_total_revenue_by_time_range(self, start_time: datetime, end_time: datetime) -> float:
        result = self.db.query(func.sum(DBRental.total_price)).filter(
            DBRental.rental_start_time >= start_time,
            DBRental.rental_end_time <= end_time
        ).scalar()
        return float(result) if result is not None else 0.0

    def create_rental(self, rental: RentalCreate) -> DBRental:
        db_rental = DBRental(
            user_id=rental.user_id,
            bicycle_id=rental.bicycle_id,
            rental_start_time=rental.rental_start_time,
            rental_end_time=rental.rental_end_time,
            actual_return_time=rental.actual_return_time,
            total_price=rental.total_price,
            discount_id=rental.discount_id
        )
        self.db.add(db_rental)
        self.db.commit()
        self.db.refresh(db_rental)
        return db_rental

    def update_rental(self, rental_id: int, rental_update: RentalUpdate) -> Optional[DBRental]:
        db_rental = self.get_rental(rental_id)
        if db_rental:
            update_data = rental_update.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(db_rental, field, value)

            self.db.add(db_rental)
            self.db.commit()
            self.db.refresh(db_rental)
        return db_rental

    def delete_rental(self, rental_id: int) -> bool:
        db_rental = self.get_rental(rental_id)
        if db_rental:
            self.db.delete(db_rental)
            self.db.commit()
            return True
        return False

RentalRepositoryDependency = Annotated[RentalRepository, Depends]
