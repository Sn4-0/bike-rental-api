from typing import List, Optional, Annotated
from datetime import datetime
from fastapi import Depends, HTTPException
from starlette import status

from crud.location import LocationRepository
from schemas.location import LocationCreate, LocationUpdate, Location as LocationDto


class LocationService:
    def __init__(self, location_repository: LocationRepository = Depends(LocationRepository)): # <--- ЗМІНА ТУТ
        self.location_repository = location_repository

    def get_all(self) -> List[LocationDto]:
        locations = self.location_repository.get_locations()
        return [LocationDto.model_validate(l) for l in locations]

    def get_by_id(self, location_id: int) -> LocationDto:
        location = self.location_repository.get_location(location_id=location_id)
        if location is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Локацію з ID {location_id} не знайдено")
        return LocationDto.model_validate(location)

    def create(self, location_data: LocationCreate) -> LocationDto:
        created_location = self.location_repository.create_location(location=location_data)
        return LocationDto.model_validate(created_location)

    def update(self, location_id: int, location_update_data: LocationUpdate) -> LocationDto:
        updated_location = self.location_repository.update_location(location_id=location_id, location_update=location_update_data)
        if updated_location is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Локацію з ID {location_id} не знайдено")
        return LocationDto.model_validate(updated_location)

    def delete(self, location_id: int) -> dict:
        if not self.location_repository.delete_location(location_id=location_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Локацію з ID {location_id} не знайдено")
        return {"message": f"Локацію з ID {location_id} видалено"}

    def get_top_locations_by_rentals(self, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, limit: int = 5) -> List[LocationDto]:
        locations = self.location_repository.get_top_performing_locations(start_date=start_date, end_date=end_date, limit=limit)
        return [LocationDto.model_validate(l) for l in locations]

LocationServiceDependency = Annotated[LocationService, Depends]
