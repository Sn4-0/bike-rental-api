from pydantic import BaseModel, Field
from typing import Optional

class BicycleBase(BaseModel):
    brand: str = Field(..., description="Марка велосипеда")
    model: str = Field(..., description="Модель велосипеда")
    type: str = Field(..., description="Тип велосипеда")
    price_per_hour: float = Field(..., gt=0, description="Ціна за годину прокату")
    current_location_id: Optional[int] = Field(None, description="ID поточної локації велосипеда")
    status: str = Field("доступний", description="Статус велосипеда (доступний, в прокаті, на ремонті)")


class BicycleCreate(BicycleBase):
    pass

class BicycleUpdate(BaseModel):
    brand: Optional[str] = Field(None, description="Марка велосипеда")
    model: Optional[str] = Field(None, description="Модель велосипеда")
    type: Optional[str] = Field(None, description="Тип велосипеда")
    price_per_hour: Optional[float] = Field(None, gt=0, description="Ціна за годину прокату")
    current_location_id: Optional[int] = Field(None, description="ID поточної локації велосипеда")
    status: Optional[str] = Field(None, description="Статус велосипеда")

class Bicycle(BicycleBase):
    id: int = Field(..., description="Унікальний ідентифікатор велосипеда")

    class Config:
        from_attributes = True