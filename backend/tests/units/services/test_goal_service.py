
# tests/unit/test_goal_service.py

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from service.goal import GoalService
from core.exceptions import ResourceExistedError, ResourceNotFoundError


@pytest.fixture
def service():
    db = MagicMock()
    service = GoalService(db, user_id=1)
    service.repository = MagicMock()
    return service


@pytest.fixture
def payload():
    data = MagicMock()
    data.goal_name = "Emergency Fund"
    data.model_dump.return_value = {
        "goal_name": "Emergency Fund",
        "target_amount": 5000,
    }
    return data


def test_create_goal(service, payload):
    service.repository.get_by_name.return_value = None
    service.repository.create.side_effect = lambda goal: goal

    result = service.create(payload)

    assert result.goal_name == "Emergency Fund"
    assert result.account_id is None
    service.repository.create.assert_called_once()


def test_create_duplicate_goal(service, payload):
    service.repository.get_by_name.return_value = SimpleNamespace(
        goal_name="Emergency Fund"
    )

    with pytest.raises(ResourceExistedError):
        service.create(payload)

    service.repository.create.assert_not_called()


def test_read_one_goal(service):
    goal = SimpleNamespace(id=10, goal_name="Emergency Fund")
    service.repository.get_by_id.return_value = goal

    result = service.read_one(10)

    assert result == goal
    service.repository.get_by_id.assert_called_once_with(1, 10)


def test_read_one_goal_not_found(service):
    service.repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundError):
        service.read_one(10)


def test_read_all_goals(service):
    goals = [
        SimpleNamespace(id=1, goal_name="Emergency Fund"),
        SimpleNamespace(id=2, goal_name="Vacation"),
    ]
    service.repository.get_all.return_value = goals

    result = service.read_all()

    assert result == goals
    service.repository.get_all.assert_called_once_with(1)


def test_update_goal(service, payload):
    goal = SimpleNamespace(id=10, goal_name="Emergency Fund")
    updated_goal = SimpleNamespace(id=10, goal_name="House Fund")

    payload.model_dump.return_value = {"goal_name": "House Fund"}
    service.repository.get_by_id.return_value = goal
    service.repository.get_by_name.return_value = None
    service.repository.update.return_value = updated_goal

    result = service.update(10, payload)

    assert result.goal_name == "House Fund"
    service.repository.update.assert_called_once_with(
        goal, {"goal_name": "House Fund"}
    )


def test_update_duplicate_goal_name(service, payload):
    goal = SimpleNamespace(id=10, goal_name="Emergency Fund")
    existing_goal = SimpleNamespace(id=20, goal_name="Vacation")

    payload.model_dump.return_value = {"goal_name": "Vacation"}
    service.repository.get_by_id.return_value = goal
    service.repository.get_by_name.return_value = existing_goal

    with pytest.raises(ResourceExistedError):
        service.update(10, payload)

    service.repository.update.assert_not_called()


def test_delete_goal(service):
    goal = SimpleNamespace(id=10, goal_name="Emergency Fund")
    service.repository.get_by_id.return_value = goal

    result = service.delete(10)

    assert result == {"message": "deleted"}
    service.repository.delete.assert_called_once_with(goal)


def test_create_goal_rolls_back_on_error(service, payload):
    service.repository.get_by_name.return_value = None
    service.repository.create.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        service.create(payload)

    service.db.rollback.assert_called_once()
