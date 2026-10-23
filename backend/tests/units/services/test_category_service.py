
# tests/unit/test_category_service.py

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from services.category import CategoryService
from core.exceptions import ResourceExistedError, ResourceNotFoundError


@pytest.fixture
def service():
    db = MagicMock()
    service = CategoryService(db, user_id=1)
    service.repository = MagicMock()
    return service


@pytest.fixture
def payload():
    data = MagicMock()
    data.model_dump.return_value = {
        "category_name": "Food",
        "category_type": "expense",
    }
    return data


def test_create_category(service, payload):
    service.repository.get_by_name.return_value = None
    service.repository.create.side_effect = lambda category: category

    result = service.create(payload)

    assert result.category_name == "Food"
    assert result.user_id == 1
    service.repository.create.assert_called_once()


def test_create_duplicate_category(service, payload):
    service.repository.get_by_name.return_value = SimpleNamespace(
        category_name="Food"
    )

    with pytest.raises(ResourceExistedError):
        service.create(payload)

    service.repository.create.assert_not_called()


def test_read_one_category(service):
    category = SimpleNamespace(id=10, category_name="Food")
    service.repository.get_by_id.return_value = category

    result = service.read_one(10)

    assert result == category
    service.repository.get_by_id.assert_called_once_with(1, 10)


def test_read_one_category_not_found(service):
    service.repository.get_by_id.return_value = None

    with pytest.raises(ResourceNotFoundError):
        service.read_one(10)


def test_read_all_categories(service):
    categories = [
        SimpleNamespace(id=1, category_name="Food"),
        SimpleNamespace(id=2, category_name="Travel"),
    ]
    service.repository.get_all.return_value = categories

    result = service.read_all()

    assert result == categories
    service.repository.get_all.assert_called_once_with(1)


def test_update_category(service, payload):
    category = SimpleNamespace(id=10, category_name="Food")
    updated_category = SimpleNamespace(id=10, category_name="Dining")

    service.repository.get_by_id.return_value = category
    payload.model_dump.return_value = {"category_name": "Dining"}
    service.repository.get_by_name.return_value = None
    service.repository.update.return_value = updated_category

    result = service.update(10, payload)

    assert result.category_name == "Dining"
    service.repository.update.assert_called_once_with(
        category, {"category_name": "Dining"}
    )


def test_update_duplicate_category_name(service, payload):
    category = SimpleNamespace(id=10, category_name="Food")
    existing = SimpleNamespace(id=20, category_name="Travel")

    service.repository.get_by_id.return_value = category
    payload.model_dump.return_value = {"category_name": "Travel"}
    service.repository.get_by_name.return_value = existing

    with pytest.raises(ResourceExistedError):
        service.update(10, payload)

    service.repository.update.assert_not_called()


def test_delete_category(service):
    category = SimpleNamespace(id=10, category_name="Food")
    service.repository.get_by_id.return_value = category

    result = service.delete(10)

    assert result == {"message": "deleted"}
    service.repository.delete.assert_called_once_with(category)


def test_create_category_rolls_back_on_error(service, payload):
    service.repository.get_by_name.return_value = None
    service.repository.create.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        service.create(payload)

    service.db.rollback.assert_called_once()
