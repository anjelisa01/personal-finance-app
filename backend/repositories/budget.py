
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.budget import Budget
from models.category import Category


class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_category(self, user_id: int, category_id: int):
        stmt = select(Category).where(
            Category.user_id == user_id,
            Category.id == category_id,
        )
        return self.db.scalar(stmt)

    def get_by_category_id(self, category_id: int):
        stmt = select(Budget).where(
            Budget.category_id == category_id
        )
        return self.db.scalar(stmt)

    def create(self, budget: Budget):
        self.db.add(budget)
        self.db.commit()
        self.db.refresh(budget)
        return budget

    def update(self, budget: Budget, update_data: dict):
        for field, value in update_data.items():
            setattr(budget, field, value)

        self.db.commit()
        self.db.refresh(budget)
        return budget

    def delete(self, budget: Budget):
        self.db.delete(budget)
        self.db.commit()
