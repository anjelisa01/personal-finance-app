
#==================================CATEGORY

from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from repositories.category import CategoryRepository


def make_repo():
    db = MagicMock(spec=Session)
    return CategoryRepository(db), db


def test_get_by_name():
    repo, db = make_repo()
    category = MagicMock()

    db.scalars.return_value.first.return_value = category

    result = repo.get_by_name(1, "Food")

    assert result == category
    db.scalars.assert_called_once()


def test_get_by_id():
    repo, db = make_repo()
    category = MagicMock()

    db.scalar.return_value = category

    result = repo.get_by_id(1, 2)

    assert result == category
    db.scalar.assert_called_once()


def test_get_all():
    repo, db = make_repo()
    categories = [MagicMock(), MagicMock()]

    db.scalars.return_value.all.return_value = categories

    result = repo.get_all(1)

    assert result == categories
    assert len(result) == 2


def test_create_category():
    repo, db = make_repo()
    category = MagicMock()

    result = repo.create(category)

    assert result == category
    db.add.assert_called_once_with(category)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(category)


def test_update_category():
    repo, db = make_repo()
    category = MagicMock()

    result = repo.update(category, {"category_name": "Transport"})

    assert category.category_name == "Transport"
    assert result == category
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(category)


def test_delete_category():
    repo, db = make_repo()
    category = MagicMock()

    result = repo.delete(category)

    assert result is None
    db.delete.assert_called_once_with(category)
    db.commit.assert_called_once()

