from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional, List, Annotated

from db.database import get_db
from models.user import User as DBUser
from schemas.user import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_user(self, user_id: int) -> Optional[DBUser]:
        return self.db.query(DBUser).filter(DBUser.id == user_id).first()

    def get_users(self) -> List[DBUser]:
        return self.db.query(DBUser).all()

    def get_user_by_email(self, email: str) -> Optional[DBUser]:
        return self.db.query(DBUser).filter(DBUser.email == email).first()

    def get_user_by_phone(self, phone: str) -> Optional[DBUser]:
        return self.db.query(DBUser).filter(DBUser.phone == phone).first()

    def create_user(self, user: UserCreate) -> DBUser:
        db_user = DBUser(
            email=user.email,
            phone=user.phone,
            first_name=user.first_name,
            last_name=user.last_name,
            address=user.address,
            is_active=True
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[DBUser]:
        db_user = self.get_user(user_id)
        if db_user:
            update_data = user_update.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(db_user, field, value)

            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        db_user = self.get_user(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return True
        return False

UserRepositoryDependency = Annotated[UserRepository, Depends]