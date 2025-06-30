from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Annotated
from datetime import datetime, timezone
from fastapi import Depends

from db.database import get_db

from models.discount import Discount
from schemas.discount import DiscountCreate, DiscountUpdate


class DiscountRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_discount(self, discount_id: int) -> Optional[Discount]:
        return self.db.query(Discount).filter(Discount.id == discount_id).first()

    def get_discount_by_name(self, name: str) -> Optional[Discount]:
        return self.db.query(Discount).filter(Discount.name == name).first()

    def get_discounts(self) -> List[Discount]:
        return self.db.query(Discount).all()

    def get_active_discounts(self, current_time: Optional[datetime] = None) -> List[Discount]:
        if current_time is None:
            current_time = datetime.utcnow()
        return self.db.query(Discount).filter(
            Discount.is_active == True,
            Discount.valid_from <= current_time,
            Discount.valid_to >= current_time
        ).all()

    def create_discount(self, discount: DiscountCreate) -> Discount:
        db_discount = Discount(**discount.model_dump())
        self.db.add(db_discount)
        self.db.commit()
        self.db.refresh(db_discount)
        return db_discount

    def update_discount(self, discount_id: int, discount_update: DiscountUpdate) -> Optional[Discount]:
        db_discount = self.get_discount(discount_id)
        if db_discount:
            update_data = discount_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_discount, key, value)
            self.db.add(db_discount)
            self.db.commit()
            self.db.refresh(db_discount)
            return db_discount
        return None

    def delete_discount(self, discount_id: int) -> bool:
        db_discount = self.get_discount(discount_id)
        if db_discount:
            self.db.delete(db_discount)
            self.db.commit()
            return True
        return False

DiscountRepositoryDependency = Annotated[DiscountRepository, Depends]