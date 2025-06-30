from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DiscountBase(BaseModel):
    name: str = Field(..., description="Назва знижки")
    percentage_amount: float = Field(..., ge=0, le=100, description="Розмір знижки у відсотках (0-100)")
    valid_from: datetime = Field(..., description="Дата початку дії знижки")
    valid_to: datetime = Field(..., description="Дата закінчення дії знижки")
    is_active: Optional[bool] = Field(True, description="Чи активна знижка на даний момент")

class DiscountCreate(DiscountBase):
    pass

class DiscountUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Назва знижки")
    percentage_amount: Optional[float] = Field(None, ge=0, le=100, description="Розмір знижки у відсотках")
    valid_from: Optional[datetime] = Field(None, description="Дата початку дії знижки")
    valid_to: Optional[datetime] = Field(None, description="Дата закінчення дії знижки")
    is_active: Optional[bool] = Field(None, description="Чи активна знижка")

class Discount(DiscountBase):
    id: int = Field(..., description="Унікальний ідентифікатор знижки")

    class Config:
        from_attributes = True