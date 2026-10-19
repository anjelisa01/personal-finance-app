
from sqlalchemy.orm import Session

from models.category import Category
from schemas.category import CategoryBase

from repositories.category import CategoryRepository

from core.logger import logger
from core.exceptions import ResourceExistedError, ResourceNotFoundError


class CategoryService:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.repository = CategoryRepository(db)

    def create(self, payload: CategoryBase):
        existing = self.repository.get_by_name(
            self.user_id, payload.category_name
        )
        if existing:
            raise ResourceExistedError("Category", payload.category_name)

        category = Category(**payload.model_dump())
        category.user_id = self.user_id

        try:
            category = self.repository.create(category)
        except Exception:
            self.db.rollback()
            raise

        logger.info("Category created, category id=%s", category.id)
        return category

    def read_one(self, category_id: int):
        category = self.repository.get_by_id(
            self.user_id, category_id
        )
        if category is None:
            raise ResourceNotFoundError("Category", category_id)
        return category

    def read_all(self):
        return self.repository.get_all(self.user_id)

    def update(self, category_id: int, payload: CategoryBase):
        category = self.read_one(category_id)
        update_data = payload.model_dump(exclude_unset=True)

        if "category_name" in update_data:
            existing = self.repository.get_by_name(
                self.user_id, update_data["category_name"]
            )
            if existing and existing.id != category_id:
                raise ResourceExistedError(
                    "Category", update_data["category_name"]
                )

        try:
            category = self.repository.update(category, update_data)
        except Exception:
            self.db.rollback()
            raise

        logger.info("Category updated, category id=%s", category_id)
        return category

    def delete(self, category_id: int):
        category = self.read_one(category_id)

        try:
            self.repository.delete(category)
        except Exception:
            self.db.rollback()
            raise

        logger.info("Category deleted, category id=%s", category_id)
        return {"message": "deleted"}
