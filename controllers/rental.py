from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Annotated
from datetime import datetime

from core.rental import RentalService
from core.bicycle import BicycleService
from schemas.rental import RentalCreate, RentalUpdate, Rental as RentalDto


router = APIRouter(
    prefix="/rentals",
    tags=["Rentals"],
    responses={404: {"description": "Запис про прокат не знайдено"}},
)


@router.post("/", response_model=RentalDto, status_code=status.HTTP_201_CREATED)
def create_rental_route(
    rental: RentalCreate,
    rental_service: RentalService = Depends(RentalService)
) -> RentalDto:
    return rental_service.create(rental_data=rental)


@router.get("/", response_model=List[RentalDto])
def read_rentals_route(
    rental_service: RentalService = Depends(RentalService),
    start_date: Optional[datetime] = Query(None, description="Початкова дата фільтрації (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="Кінцева дата фільтрації (YYYY-MM-DD)"),
) -> List[RentalDto]:
    if start_date and end_date:
        rentals = rental_service.get_rentals_in_time_range(start_date=start_date, end_date=end_date)
    else:
        rentals = rental_service.get_all()
    return rentals


@router.get("/{rental_id}", response_model=RentalDto)
def read_rental_route(
    rental_id: int,
    rental_service: RentalService = Depends(RentalService)
) -> RentalDto:
    return rental_service.get_by_id(rental_id=rental_id)


@router.put("/{rental_id}", response_model=RentalDto)
def update_rental_route(
    rental_id: int,
    rental_update_data: RentalUpdate,
    rental_service: RentalService = Depends(RentalService)
) -> RentalDto:
    return rental_service.update(rental_id=rental_id, rental_update_data=rental_update_data)


@router.delete("/{rental_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rental_route(
    rental_id: int,
    rental_service: RentalService = Depends(RentalService)
):
    rental_service.delete(rental_id=rental_id)
    return None


@router.get("/bicycle_history/{bicycle_id}", response_model=List[RentalDto])
def get_bicycle_rental_history_route(
    bicycle_id: int,
    rental_service: RentalService = Depends(RentalService),
    bicycle_service: BicycleService = Depends(BicycleService)
):
    bicycle = bicycle_service.get_by_id(bicycle_id=bicycle_id)
    history = rental_service.get_rental_history_for_bicycle(bicycle_id=bicycle_id)
    return history


@router.get("/revenue/", response_model=float)
def get_total_revenue_route(
    rental_service: RentalService = Depends(RentalService),
    start_date: datetime = Query(..., description="Початкова дата для розрахунку прибутку (YYYY-MM-DD)"),
    end_date: datetime = Query(..., description="Кінцева дата для розрахунку прибутку (YYYY-MM-DD)"),
):
    if start_date >= end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Кінцева дата повинна бути пізніше початкової дати.")

    revenue = rental_service.get_revenue_by_time_range(start_date=start_date, end_date=end_date)
    return revenue