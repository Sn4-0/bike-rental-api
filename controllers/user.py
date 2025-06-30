from typing import List, Optional, Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from core.user import UserService
from schemas.user import UserCreate, UserUpdate, User as UserDto


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Користувача не знайдено"}},
)

@router.post("/", response_model=UserDto, status_code=status.HTTP_201_CREATED)
def create_user_route(
    user: UserCreate,
    user_service: UserService = Depends(UserService) # Змінено тут
) -> UserDto:
    return user_service.create(user_data=user)

@router.get("/", response_model=List[UserDto])
def read_users_route(
    user_service: UserService = Depends(UserService) # Змінено тут
) -> List[UserDto]:
    return user_service.get_all()

@router.get("/{user_id}", response_model=UserDto)
def read_user_route(
    user_id: int,
    user_service: UserService = Depends(UserService) # Змінено тут
) -> UserDto:
    return user_service.get_by_id(user_id=user_id)

@router.put("/{user_id}", response_model=UserDto)
def update_user_route(
    user_id: int,
    user_update_data: UserUpdate,
    user_service: UserService = Depends(UserService) # Змінено тут
) -> UserDto:
    return user_service.update(user_id=user_id, user_update_data=user_update_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(
    user_id: int,
    user_service: UserService = Depends(UserService) # Змінено тут
):
    user_service.delete(user_id=user_id)
    return None