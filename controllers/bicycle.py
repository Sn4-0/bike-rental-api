from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from core.bicycle import BicycleService


from schemas.bicycle import BicycleCreate, BicycleUpdate, Bicycle as BicycleDto


router = APIRouter(
    prefix="/bicycles",
    tags=["Bicycles"],
    responses={404: {"description": "Велосипед не знайдено"}},
)

@router.post("/", response_model=BicycleDto, status_code=status.HTTP_201_CREATED)
def create_bicycle_route(
    bicycle: BicycleCreate,
    bicycle_service: BicycleService = Depends(BicycleService) # Виправлено: використовуємо Depends(ServiceClass)
) -> BicycleDto:
    return bicycle_service.create(bicycle_data=bicycle)

@router.get("/", response_model=List[BicycleDto])
def read_bicycles_route(
    bicycle_service: BicycleService = Depends(BicycleService), # Виправлено
    location_id: Optional[int] = Query(None, description="Фільтрувати за ID локації"),
    status: Optional[str] = Query(None, description="Фільтрувати за статусом (доступний, в прокаті, на ремонті)"),
    sort_by_price: Optional[bool] = Query(None, description="Сортувати за ціною за годину"),
) -> List[BicycleDto]:
    if location_id is not None:
        bicycles = bicycle_service.get_available_bicycles_in_location(location_id=location_id)
    elif status is not None:
        bicycles = bicycle_service.get_bicycles_by_status(status=status)
    else:
        bicycles = bicycle_service.get_all()
    if sort_by_price:
        bicycles.sort(key=lambda b: b.price_per_hour, reverse=False)
    return bicycles


@router.get("/{bicycle_id}", response_model=BicycleDto)
def read_bicycle_route(
    bicycle_id: int,
    bicycle_service: BicycleService = Depends(BicycleService)
) -> BicycleDto:
    return bicycle_service.get_by_id(bicycle_id=bicycle_id)


@router.put("/{bicycle_id}", response_model=BicycleDto)
def update_bicycle_route(
    bicycle_id: int,
    bicycle_update_data: BicycleUpdate,
    bicycle_service: BicycleService = Depends(BicycleService)
) -> BicycleDto:
    return bicycle_service.update(bicycle_id=bicycle_id, bicycle_update_data=bicycle_update_data)


@router.delete("/{bicycle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bicycle_route(
    bicycle_id: int,
    bicycle_service: BicycleService = Depends(BicycleService)
):
    bicycle_service.delete(bicycle_id=bicycle_id)
    return None


@router.get("/most_rented/", response_model=BicycleDto)
def get_most_rented_bicycle_route(
    bicycle_service: BicycleService = Depends(BicycleService)
) -> BicycleDto:
    most_rented = bicycle_service.get_most_rented_bicycle()
    if most_rented is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Немає даних про прокат, щоб визначити найпопулярніший велосипед.")
    return most_rented