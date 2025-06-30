from typing import List, Optional, Union, Annotated
from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status


from schemas.rental import RentalCreate, RentalUpdate, Rental as RentalDto

from crud.rental import RentalRepository
from crud.user import UserRepository
from crud.bicycle import BicycleRepository
from crud.discount import DiscountRepository


def make_utc_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


class RentalService:
    def __init__(
        self,
        rental_repository: RentalRepository = Depends(RentalRepository),
        user_repository: UserRepository = Depends(UserRepository),
        bicycle_repository: BicycleRepository = Depends(BicycleRepository),
        discount_repository: DiscountRepository = Depends(DiscountRepository)
    ):
        self.rental_repository = rental_repository
        self.user_repository = user_repository
        self.bicycle_repository = bicycle_repository
        self.discount_repository = discount_repository

    def get_all(self) -> List[RentalDto]:
        rentals = self.rental_repository.get_rentals()
        return [RentalDto.model_validate(r) for r in rentals]

    def get_by_id(self, rental_id: int) -> RentalDto:
        rental = self.rental_repository.get_rental(rental_id=rental_id)
        if rental is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запис про прокат з ID {rental_id} не знайдено")
        return RentalDto.model_validate(rental)

    def create(self, rental_data: RentalCreate) -> RentalDto:
        user = self.user_repository.get_user(user_id=rental_data.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Користувача не знайдено")

        bicycle = self.bicycle_repository.get_bicycle(bicycle_id=rental_data.bicycle_id)
        if not bicycle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Велосипед не знайдено")

        if bicycle.status != "доступний":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Велосипед недоступний. Поточний статус: {bicycle.status}")

        rental_start_aware = make_utc_aware(rental_data.rental_start_time)

        if rental_data.discount_id is not None:
            discount = self.discount_repository.get_discount(discount_id=rental_data.discount_id)

            if not discount:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Недійсна або неактивна знижка")

            discount_valid_from_aware = make_utc_aware(discount.valid_from)
            discount_valid_to_aware = make_utc_aware(discount.valid_to)

            is_discount_active = discount.is_active
            is_in_valid_range = (discount_valid_from_aware <= rental_start_aware <= discount_valid_to_aware)

            if not is_discount_active or not is_in_valid_range:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недійсна або неактивна знижка")

        try:
            created_rental = self.rental_repository.create_rental(rental=rental_data)
            return RentalDto.model_validate(created_rental)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def update(self, rental_id: int, rental_update_data: RentalUpdate) -> RentalDto:
        db_rental = self.rental_repository.get_rental(rental_id=rental_id)
        if not db_rental:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запис про прокат з ID {rental_id} не знайдено")

        if rental_update_data.bicycle_id is not None and rental_update_data.bicycle_id != db_rental.bicycle_id:
            bicycle = self.bicycle_repository.get_bicycle(bicycle_id=rental_update_data.bicycle_id)
            if not bicycle:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Велосипед не знайдено для оновлення")

        if rental_update_data.discount_id is not None and rental_update_data.discount_id != db_rental.discount_id:
            discount = self.discount_repository.get_discount(discount_id=rental_update_data.discount_id)

            rental_start_aware_for_update = make_utc_aware(db_rental.rental_start_time)
            discount_valid_from_aware = make_utc_aware(discount.valid_from) if discount else None
            discount_valid_to_aware = make_utc_aware(discount.valid_to) if discount else None

            if not discount or not discount.is_active or \
                    not (
                            discount_valid_from_aware <= rental_start_aware_for_update <= discount_valid_to_aware):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Недійсна або неактивна знижка для оновлення")

        try:
            updated_rental = self.rental_repository.update_rental(rental_id=rental_id, rental_update=rental_update_data)
            if updated_rental is None:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Помилка при оновленні запису про прокат")
            return RentalDto.model_validate(updated_rental)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    def delete(self, rental_id: int) -> dict:
        if not self.rental_repository.delete_rental(rental_id=rental_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Запис про прокат з ID {rental_id} не знайдено")
        return {"message": f"Запис про прокат з ID {rental_id} видалено"}

    def get_rental_history_for_bicycle(self, bicycle_id: int) -> List[RentalDto]:
        rentals = self.rental_repository.get_rentals_by_bicycle_id(bicycle_id=bicycle_id)
        return [RentalDto.model_validate(r) for r in rentals]

    def get_revenue_by_time_range(self, start_date: datetime, end_date: datetime) -> float:
        start_date_aware = make_utc_aware(start_date)
        end_date_aware = make_utc_aware(end_date)
        return self.rental_repository.get_total_revenue_by_time_range(start_time=start_date_aware, end_time=end_date_aware)

    def get_rentals_in_time_range(self, start_date: datetime, end_date: datetime) -> List[RentalDto]:
        start_date_aware = make_utc_aware(start_date)
        end_date_aware = make_utc_aware(end_date)
        rentals = self.rental_repository.get_rentals_by_time_range(start_time=start_date_aware, end_time=end_date_aware)
        return [RentalDto.model_validate(r) for r in rentals]

RentalServiceDependency = Annotated[RentalService, Depends]