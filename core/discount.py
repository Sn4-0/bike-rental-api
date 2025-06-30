from typing import List, Optional, Annotated
from datetime import datetime

from fastapi import Depends, HTTPException, status

from crud.discount import DiscountRepository
from schemas.discount import DiscountCreate, DiscountUpdate, Discount as DiscountDto


class DiscountService:
    def __init__(self, discount_repository: DiscountRepository = Depends(DiscountRepository)):
        self.discount_repository = discount_repository

    def get_all(self) -> List[DiscountDto]:
        discounts = self.discount_repository.get_discounts()
        return [DiscountDto.model_validate(d) for d in discounts]

    def get_by_id(self, discount_id: int) -> DiscountDto:
        discount = self.discount_repository.get_discount(discount_id=discount_id)
        if discount is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Знижку з ID {discount_id} не знайдено")
        return DiscountDto.model_validate(discount)

    def create(self, discount_data: DiscountCreate) -> DiscountDto:
        existing_discount = self.discount_repository.get_discount_by_name(name=discount_data.name)
        if existing_discount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Знижка з іменем '{discount_data.name}' вже існує."
            )

        created_discount = self.discount_repository.create_discount(discount=discount_data)
        return DiscountDto.model_validate(created_discount)

    def update(self, discount_id: int, discount_update_data: DiscountUpdate) -> DiscountDto:
        updated_discount = self.discount_repository.update_discount(discount_id=discount_id, discount_update=discount_update_data)
        if updated_discount is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Знижку з ID {discount_id} не знайдено")
        return DiscountDto.model_validate(updated_discount)

    def delete(self, discount_id: int) -> dict:
        if not self.discount_repository.delete_discount(discount_id=discount_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Знижку з ID {discount_id} не знайдено")
        return {"message": f"Знижку з ID {discount_id} видалено"}

    def get_active_discounts(self, current_time: Optional[datetime] = None) -> List[DiscountDto]:
        discounts = self.discount_repository.get_active_discounts(current_time=current_time)
        return [DiscountDto.model_validate(d) for d in discounts]

DiscountServiceDependency = Annotated[DiscountService, Depends]