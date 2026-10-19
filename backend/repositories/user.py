
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        return self.db.scalars(stmt).first()

    def get_by_id(self, user_id: int):
        stmt = select(User).where(User.id == user_id)
        return self.db.scalar(stmt)

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, update_data: dict):
        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def save(self):
        self.db.commit()
