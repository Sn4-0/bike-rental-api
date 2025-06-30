from typing import List, Optional, Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.user import UserRepository
from crud.rental import RentalRepository
from schemas.user import UserCreate, UserUpdate, User as UserDto


class UserService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(UserRepository),
        rental_repository: RentalRepository = Depends(RentalRepository)
    ):
        self.user_repository = user_repository
        self.rental_repository = rental_repository

    def get_all(self) -> List[UserDto]:
        users = self.user_repository.get_users()
        return [UserDto.model_validate(u) for u in users]

    def get_by_id(self, user_id: int) -> UserDto:
        user = self.user_repository.get_user(user_id=user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Користувача з ID {user_id} не знайдено")
        return UserDto.model_validate(user)

    def get_by_email(self, email: str) -> UserDto:
        user = self.user_repository.get_user_by_email(email=email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Користувача з email '{email}' не знайдено")
        return UserDto.model_validate(user)

    def get_by_phone(self, phone: str) -> UserDto:
        user = self.user_repository.get_user_by_phone(phone=phone)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Користувача з номером телефону '{phone}' не знайдено")
        return UserDto.model_validate(user)

    def create(self, user_data: UserCreate) -> UserDto:
        existing_user_email = self.user_repository.get_user_by_email(email=user_data.email)
        if existing_user_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Користувач з таким email вже існує")

        existing_user_phone = self.user_repository.get_user_by_phone(phone=user_data.phone)
        if existing_user_phone:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Користувач з таким номером телефону вже існує")

        created_user = self.user_repository.create_user(user=user_data)
        return UserDto.model_validate(created_user)

    def update(self, user_id: int, user_update_data: UserUpdate) -> UserDto:
        updated_user = self.user_repository.update_user(user_id=user_id, user_update=user_update_data)
        if updated_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Користувача з ID {user_id} не знайдено")
        return UserDto.model_validate(updated_user)

    def delete(self, user_id: int) -> dict:
        rentals_for_user = self.rental_repository.get_rentals_by_user_id(user_id=user_id)
        if rentals_for_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Не вдалося видалити користувача з ID {user_id}, оскільки існують пов'язані записи про прокат."
            )

        if not self.user_repository.delete_user(user_id=user_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Користувача з ID {user_id} не знайдено")
        return {"message": f"Користувача з ID {user_id} видалено"}

UserServiceDependency = Annotated[UserService, Depends]