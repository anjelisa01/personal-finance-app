
from sqlalchemy.orm import Session
from datetime import datetime, UTC

from models.user import User
from schemas.user import UserCreate, UserUpdate

from core.security import hash_password
from core.logger import logger
from core.exceptions import ResourceExistedError

from repositories.user import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create(self, payload: UserCreate):
        existing = self.repository.get_by_email(payload.email)
        if existing:
            raise ResourceExistedError("User", payload.email)

        user = User(
            name=payload.name,
            email=payload.email,
            currency=payload.currency,
            hashed_password=hash_password(payload.password),
            deleted_at=None,
        )

        try:
            user = self.repository.create(user)
        except Exception:
            self.db.rollback()
            raise

        logger.info(
            "User created successfully, user_id=%s",
            user.id,
        )
        return user

    def read_one(self, user_id: int):
        # no exception for if user existed or not, because user MUST existed to even access this service
        return self.repository.get_by_id(user_id)

    def update(self, user_id: int, payload: UserUpdate):
        user = self.repository.get_by_id(user_id)
        # no exception for if user existed or not, because user MUST existed to even access this service

        update_data = payload.model_dump(exclude_unset=True)

        if "password" in update_data:
            user.hashed_password = hash_password(
                update_data.pop("password")
            )

        if "email" in update_data:
            existing = self.repository.get_by_email(
                update_data["email"]
            )
            if existing:
                raise ResourceExistedError(
                    "User", update_data["email"]
                )

        try:
            user = self.repository.update(user, update_data)
        except Exception:
            self.db.rollback()
            raise

        logger.info("User updated, user_id=%s", user_id)
        return user

    def delete(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        # no exception for if user existed or not, because user MUST existed to even access this service

        # doing soft delete
        user.name = None
        user.email = None
        user.hashed_password = None
        user.deleted_at = datetime.now(UTC)

        try:
            self.repository.save()
        except Exception:
            self.db.rollback()
            raise

        logger.info("User deleted, user_id=%s", user_id)
        return {"message": "deleted"}
