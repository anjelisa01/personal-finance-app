
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.user import User


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        return self.db.scalars(stmt).first()
