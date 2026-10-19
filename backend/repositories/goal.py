
from sqlalchemy.orm import Session
from sqlalchemy import select

from models.goal import Goal


def get_goal_name(db: Session, user_id: int, goal_name: str):
    stmt = select(Goal).where(
        Goal.user_id == user_id,
        Goal.goal_name == goal_name,
    )
    return db.scalars(stmt).first()


class GoalRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, user_id: int, goal_name: str):
        return get_goal_name(self.db, user_id, goal_name)

    def get_by_id(self, user_id: int, goal_id: int):
        stmt = select(Goal).where(
            Goal.user_id == user_id,
            Goal.id == goal_id,
        )
        return self.db.scalar(stmt)

    def get_all(self, user_id: int):
        stmt = select(Goal).where(Goal.user_id == user_id)
        return self.db.scalars(stmt).all()

    def create(self, goal: Goal):
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def update(self, goal: Goal, update_data: dict):
        for field, value in update_data.items():
            setattr(goal, field, value)

        self.db.commit()
        self.db.refresh(goal)
        return goal

    def delete(self, goal: Goal):
        self.db.delete(goal)
        self.db.commit()
