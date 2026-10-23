from unittest.mock import MagicMock
from types import SimpleNamespace

import pytest

from services.budget import BudgetService
from schemas.budget import BudgetBase, BudgetUpdate
from core.exceptions import ResourceNotFoundError


def make_service():
    db = MagicMock()
    service = BudgetService(db, user_id=1)
    service.repository = MagicMock()
    return service, db


def test_create_budget():
    service, _ = make_service()
    category = SimpleNamespace(id=10)
    budget = MagicMock(id=20)

    service.repository.get_category.return_value = category
    service.repository.create.return_value = budget

    payload = BudgetBase(amount=500000, period="monthly")
    result = service.create(category_id=10, payload=payload)

    assert result == budget
    created_budget = service.repository.create.call_args.args[0]
    assert created_budget.category_id == 10


def test_create_budget_category_not_found():
    service, _ = make_service()
    service.repository.get_category.return_value = None

    payload = BudgetBase(amount=500000, period="monthly")

    with pytest.raises(ResourceNotFoundError):
        service.create(category_id=10, payload=payload)

    service.repository.create.assert_not_called()


def test_read_budget():
    service, _ = make_service()
    category = SimpleNamespace(id=10)
    budget = MagicMock()

    service.repository.get_category.return_value = category
    service.repository.get_by_category_id.return_value = budget

    result = service.read_one(category_id=10)

    assert result == budget


def test_read_budget_not_found():
    service, _ = make_service()
    service.repository.get_category.return_value = SimpleNamespace(id=10)
    service.repository.get_by_category_id.return_value = None

    with pytest.raises(ResourceNotFoundError):
        service.read_one(category_id=10)


def test_update_budget():
    service, _ = make_service()
    budget = SimpleNamespace(id=20, amount=500000)

    service.read_one = MagicMock(return_value=budget)
    service.repository.update.return_value = budget

    payload = BudgetUpdate(amount=750000)
    result = service.update(category_id=10, payload=payload)

    assert result == budget
    service.repository.update.assert_called_once_with(
        budget,
        {"amount": 750000},
    )


def test_delete_budget():
    service, _ = make_service()
    budget = MagicMock()
    service.read_one = MagicMock(return_value=budget)

    result = service.delete(category_id=10)

    assert result == {"message": "deleted"}
    service.repository.delete.assert_called_once_with(budget)


def test_create_budget_rolls_back_on_error():
    service, db = make_service()
    service.repository.get_category.return_value = SimpleNamespace(id=10)
    service.repository.create.side_effect = RuntimeError("Database error")

    payload = BudgetBase(amount=500000, period="monthly")

    with pytest.raises(RuntimeError):
        service.create(category_id=10, payload=payload)

    db.rollback.assert_called_once()
