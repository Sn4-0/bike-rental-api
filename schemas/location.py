from pydantic import BaseModel, Field
from typing import Optional

class LocationBase(BaseModel):
    name: str = Field(..., description="Назва локації прокату")
    address: Optional[str] = Field(None, description="Адреса локації")

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Назва локації прокату")
    address: Optional[str] = Field(None, description="Адреса локації")

class Location(LocationBase):
    id: int = Field(..., description="Унікальний ідентифікатор локації")

    class Config:
        from_attributes = True