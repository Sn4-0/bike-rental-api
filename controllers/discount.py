from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime

from core.discount import DiscountService
from schemas.discount import DiscountCreate, DiscountUpdate, Discount as DiscountDto


router = APIRouter(
    prefix="/discounts",
    tags=["Discounts"],
    responses={404: {"description": "Знижку не знайдено"}},
)


@router.post("/", response_model=DiscountDto, status_code=status.HTTP_201_CREATED)
def create_discount_route(
    discount: DiscountCreate,
    discount_service: DiscountService = Depends(DiscountService)
) -> DiscountDto:
    return discount_service.create(discount_data=discount)


@router.get("/", response_model=List[DiscountDto])
def read_discounts_route(
    discount_service: DiscountService = Depends(DiscountService),
    active_only: Optional[bool] = Query(None, description="Повернути лише активні знижки на поточний час"),
) -> List[DiscountDto]:
    if active_only:
        return discount_service.get_active_discounts(current_time=datetime.utcnow())
    return discount_service.get_all() # Цей виклик має бути правильним, оскільки DiscountService має метод get_all()


@router.get("/{discount_id}", response_model=DiscountDto)
def read_discount_route(
    discount_id: int,
    discount_service: DiscountService = Depends(DiscountService)
) -> DiscountDto:
    return discount_service.get_by_id(discount_id=discount_id)


@router.put("/{discount_id}", response_model=DiscountDto)
def update_discount_route(
    discount_id: int,
    discount_update_data: DiscountUpdate,
    discount_service: DiscountService = Depends(DiscountService)
) -> DiscountDto:
    return discount_service.update(discount_id=discount_id, discount_update_data=discount_update_data)


@router.delete("/{discount_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_discount_route(
    discount_id: int,
    discount_service: DiscountService = Depends(DiscountService)
):
    discount_service.delete(discount_id=discount_id)
    return None