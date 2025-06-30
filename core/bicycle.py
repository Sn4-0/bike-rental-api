from typing import List, Optional, Annotated

from fastapi import Depends, HTTPException, status

from crud.bicycle import BicycleRepository
from crud.location import LocationRepository
from schemas.bicycle import BicycleCreate, BicycleUpdate, Bicycle as BicycleDto


class BicycleService:
    def __init__(
            self,
            bicycle_repository: BicycleRepository = Depends(BicycleRepository),
            location_repository: LocationRepository = Depends(LocationRepository)
    ):
        self.bicycle_repository = bicycle_repository
        self.location_repository = location_repository

    def get_all(self) -> List[BicycleDto]:
        bicycles = self.bicycle_repository.get_bicycles()
        return [BicycleDto.model_validate(b) for b in bicycles]

    def get_by_id(self, bicycle_id: int) -> BicycleDto:
        bicycle = self.bicycle_repository.get_bicycle(bicycle_id=bicycle_id)
        if bicycle is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Велосипед з ID {bicycle_id} не знайдено")
        return BicycleDto.model_validate(bicycle)

    def create(self, bicycle_data: BicycleCreate) -> BicycleDto:
        if bicycle_data.current_location_id is not None:
            location = self.location_repository.get_location(location_id=bicycle_data.current_location_id)
            if not location:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Локацію не знайдено")

        try:
            created_bicycle = self.bicycle_repository.create_bicycle(bicycle=bicycle_data)
            return BicycleDto.model_validate(created_bicycle)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


    def update(self, bicycle_id: int, bicycle_update_data: BicycleUpdate) -> BicycleDto:
        db_bicycle = self.bicycle_repository.get_bicycle(bicycle_id=bicycle_id)
        if not db_bicycle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Велосипед з ID {bicycle_id} не знайдено")

        if bicycle_update_data.current_location_id is not None and \
                bicycle_update_data.current_location_id != db_bicycle.current_location_id:
            location = self.location_repository.get_location(location_id=bicycle_update_data.current_location_id)
            if not location:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Локацію не знайдено для оновлення")

        try:
            updated_bicycle = self.bicycle_repository.update_bicycle(bicycle_id=bicycle_id, bicycle_update=bicycle_update_data)
            if updated_bicycle is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Помилка при оновленні велосипеда")
            return BicycleDto.model_validate(updated_bicycle)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def delete(self, bicycle_id: int) -> dict:
        if not self.bicycle_repository.delete_bicycle(bicycle_id=bicycle_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Велосипед з ID {bicycle_id} не знайдено")
        return {"message": f"Велосипед з ID {bicycle_id} видалено"}

    def get_available_bicycles_in_location(self, location_id: int) -> List[BicycleDto]:
        bicycles = self.bicycle_repository.get_bicycles_by_location(location_id=location_id)
        return [BicycleDto.model_validate(b) for b in bicycles] # Виправлено: bicycle -> bicycles

    def get_most_rented_bicycle(self) -> Optional[BicycleDto]:
        bicycle = self.bicycle_repository.get_most_rented_bicycle()
        if bicycle:
            return BicycleDto.model_validate(bicycle)
        return None

BicycleServiceDependency = Annotated[BicycleService, Depends]