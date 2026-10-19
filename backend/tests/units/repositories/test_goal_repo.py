
#==================================GOAL
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from repositories.goal import GoalRepository


def make_repo():
    db = MagicMock(spec=Session)
    return GoalRepository(db), db


def test_get_by_name():
    repo, db = make_repo()
    goal = MagicMock()

    db.scalars.return_value.first.return_value = goal

    result = repo.get_by_name(1, "Buy a laptop")

    assert result == goal
    db.scalars.assert_called_once()


def test_get_by_id():
    repo, db = make_repo()
    goal = MagicMock()

    db.scalar.return_value = goal

    result = repo.get_by_id(1, 2)

    assert result == goal
    db.scalar.assert_called_once()


def test_get_all():
    repo, db = make_repo()
    goals = [MagicMock(), MagicMock()]

    db.scalars.return_value.all.return_value = goals

    result = repo.get_all(1)

    assert result == goals
    assert len(result) == 2


def test_create_goal():
    repo, db = make_repo()
    goal = MagicMock()

    result = repo.create(goal)

    assert result == goal
    db.add.assert_called_once_with(goal)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(goal)


def test_update_goal():
    repo, db = make_repo()
    goal = MagicMock()

    result = repo.update(
        goal,
        {"goal_name": "Buy a motorcycle"}
    )

    assert goal.goal_name == "Buy a motorcycle"
    assert result == goal
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(goal)


def test_delete_goal():
    repo, db = make_repo()
    goal = MagicMock()

    result = repo.delete(goal)

    assert result is None
    db.delete.assert_called_once_with(goal)
    db.commit.assert_called_once()
