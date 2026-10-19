
from sqlalchemy.orm import Session

from models.goal import Goal
from schemas.goal import GoalBase, GoalUpdate

from core.logger import logger
from core.exceptions import ResourceNotFoundError, ResourceExistedError

from repositories.goal import GoalRepository


class GoalService:
    def __init__(self, db: Session, user_id: int):
        self.db = db
        self.user_id = user_id
        self.repository = GoalRepository(db)

    def create(self, payload: GoalBase):
        existing = self.repository.get_by_name(
            self.user_id, payload.goal_name
        )
        if existing:
            raise ResourceExistedError("Goal", payload.goal_name)

        goal = Goal(**payload.model_dump())
        goal.account_id = None

        try:
            goal = self.repository.create(goal)
        except Exception:
            self.db.rollback()
            raise

        logger.info("Goal created, goal id=%s", goal.id)
        return goal

    def read_one(self, goal_id: int):
        goal = self.repository.get_by_id(self.user_id, goal_id)
        if goal is None:
            raise ResourceNotFoundError("Goal", goal_id)
        return goal

    def read_all(self):
        return self.repository.get_all(self.user_id)

    def update(self, goal_id: int, payload: GoalUpdate):
        goal = self.repository.get_by_id(self.user_id, goal_id)
        if goal is None:
            raise ResourceNotFoundError("Goal", goal_id)

        update_data = payload.model_dump(exclude_unset=True)

        if "goal_name" in update_data:
            existing = self.repository.get_by_name(
                self.user_id, update_data["goal_name"]
            )
            if existing:
                raise ResourceExistedError(
                    "Account", update_data["goal_name"]
                )

        try:
            goal = self.repository.update(goal, update_data)
        except Exception:
            self.db.rollback()
            raise

        logger.info("Goal updated, goal id =%s", goal_id)
        return goal

    def delete(self, goal_id: int):
        goal = self.repository.get_by_id(self.user_id, goal_id)
        if goal is None:
            raise ResourceNotFoundError("Goal", goal_id)

        try:
            self.repository.delete(goal)
        except Exception:
            self.db.rollback()
            raise

        logger.info("Goal deleted, goal id=%s", goal_id)
        return {"message": "deleted"}
