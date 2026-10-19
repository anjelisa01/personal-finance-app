
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.category import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, user_id: int, category_name: str):
        stmt = select(Category).where(
            Category.user_id == user_id,
            Category.category_name == category_name,
        )
        return self.db.scalars(stmt).first()

    def get_by_id(self, user_id: int, category_id: int):
        stmt = select(Category).where(
            Category.user_id == user_id,
            Category.id == category_id,
        )
        return self.db.scalar(stmt)

    def get_all(self, user_id: int):
        stmt = select(Category).where(
            Category.user_id == user_id
        )
        return self.db.scalars(stmt).all()

    def create(self, category: Category):
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: Category, update_data: dict):
        for field, value in update_data.items():
            setattr(category, field, value)

        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: Category):
        self.db.delete(category)
        self.db.commit()
