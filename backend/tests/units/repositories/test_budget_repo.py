
#==================================BUDGET

from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from repositories.budget import BudgetRepository


def make_repo():
    db = MagicMock(spec=Session)
    return BudgetRepository(db), db


def test_get_category():
    repo, db = make_repo()
    category = MagicMock()

    db.scalar.return_value = category

    result = repo.get_category(user_id=1, category_id=2)

    assert result == category
    db.scalar.assert_called_once()


def test_get_by_category_id():
    repo, db = make_repo()
    budget = MagicMock()

    db.scalar.return_value = budget

    result = repo.get_by_category_id(category_id=2)

    assert result == budget
    db.scalar.assert_called_once()


def test_create_budget():
    repo, db = make_repo()
    budget = MagicMock()

    result = repo.create(budget)

    assert result == budget
    db.add.assert_called_once_with(budget)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(budget)


def test_update_budget():
    repo, db = make_repo()
    budget = MagicMock()

    result = repo.update(
        budget,
        {"amount": 500000}
    )

    assert budget.amount == 500000
    assert result == budget
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(budget)


def test_delete_budget():
    repo, db = make_repo()
    budget = MagicMock()

    result = repo.delete(budget)

    assert result is None
    db.delete.assert_called_once_with(budget)
    db.commit.assert_called_once()
