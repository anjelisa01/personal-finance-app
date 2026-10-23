
from sqlalchemy.orm import Session

from models.budget import Budget
from schemas.budget import BudgetBase, BudgetUpdate

from repositories.budget import BudgetRepository

from core.logger import logger
from core.exceptions import ResourceNotFoundError


class BudgetService:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.repository = BudgetRepository(db)

    def create(self, category_id: int, payload: BudgetBase):
        category = self.repository.get_category(
            self.user_id, category_id
        )
        if category is None:
            raise ResourceNotFoundError("Category", category_id)

        budget = Budget(**payload.model_dump())
        budget.category_id = category.id

        #add guardrail to restrict one budget for one category

        try:
            budget = self.repository.create(budget)
        except Exception:
            self.db.rollback()
            raise

        logger.info("Budget created, budget id=%s", budget.id)
        return budget

    def read_one(self, category_id: int):
        category = self.repository.get_category(
            self.user_id, category_id
        )
        if category is None:
            raise ResourceNotFoundError("Category", category_id)

        budget = self.repository.get_by_category_id(category.id)
        if budget is None:
            raise ResourceNotFoundError(
                "Budget for Category", category_id
            )

        return budget

    def update(self, category_id: int, payload: BudgetUpdate):
        budget = self.read_one(category_id)
        update_data = payload.model_dump(exclude_unset=True)

        try:
            budget = self.repository.update(budget, update_data)
        except Exception:
            self.db.rollback()
            raise

        logger.info("Budget updated, category id=%s", category_id)
        return budget

    def delete(self, category_id: int):
        budget = self.read_one(category_id)

        try:
            self.repository.delete(budget)
        except Exception:
            self.db.rollback()
            raise

        logger.info("Budget deleted, category id=%s", category_id)
        return {"message": "deleted"}
