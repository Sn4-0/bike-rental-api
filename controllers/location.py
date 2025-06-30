from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Annotated
from datetime import datetime
from core.location import LocationService

from schemas.location import LocationCreate, LocationUpdate, Location as LocationDto


router = APIRouter(
    prefix="/locations",
    tags=["locations"],
    responses={404: {"description": "Локацію не знайдено"}},
)


@router.post("/", response_model=LocationDto, status_code=status.HTTP_201_CREATED)
def create_location_route(
    location: LocationCreate,
    location_service: LocationService = Depends(LocationService)
) -> LocationDto:
    return location_service.create(location_data=location)


@router.get("/", response_model=List[LocationDto])
def read_locations_route(
    location_service: LocationService = Depends(LocationService)
) -> List[LocationDto]:
    return location_service.get_all()


@router.get("/{location_id}", response_model=LocationDto)
def read_location_route(
    location_id: int,
    location_service: LocationService = Depends(LocationService)
) -> LocationDto:
    return location_service.get_by_id(location_id=location_id)


@router.put("/{location_id}", response_model=LocationDto)
def update_location_route(
    location_id: int,
    location_update_data: LocationUpdate,
    location_service: LocationService = Depends(LocationService)
) -> LocationDto:
    return location_service.update(location_id=location_id, location_update_data=location_update_data)


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location_route(
    location_id: int,
    location_service: LocationService = Depends(LocationService)
):
    location_service.delete(location_id=location_id)
    return None


@router.get("/top-rentals/", response_model=List[LocationDto])
def get_top_locations_by_rentals_route(
    location_service: LocationService = Depends(LocationService),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(5)
) -> List[LocationDto]:
    return location_service.get_top_locations_by_rentals(start_date=start_date, end_date=end_date, limit=limit)