from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class RentalBase(BaseModel):
    user_id: int
    bicycle_id: int
    rental_start_time: datetime
    rental_end_time: datetime
    actual_return_time: Optional[datetime] = None
    total_price: float
    discount_id: Optional[int] = None

class RentalCreate(RentalBase):
    pass

class RentalUpdate(BaseModel):
    user_id: Optional[int] = None
    bicycle_id: Optional[int] = None
    rental_start_time: Optional[datetime] = None
    rental_end_time: Optional[datetime] = None
    actual_return_time: Optional[datetime] = None
    total_price: Optional[float] = None
    discount_id: Optional[int] = None

class Rental(RentalBase):
    id: int

    model_config = ConfigDict(from_attributes=True)