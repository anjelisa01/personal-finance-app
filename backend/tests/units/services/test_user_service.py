
# tests/unit/test_user_service.py

from datetime import UTC, datetime
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from core.security import hash_password
from services.user import UserService
from core.exceptions import ResourceExistedError


@pytest.fixture
def service():
    db = MagicMock()
    service = UserService(db)
    service.repository = MagicMock()
    return service


@pytest.fixture
def payload():
    data = MagicMock()
    data.name = "Alice"
    data.email = "alice@example.com"
    data.currency = "USD"
    data.password = "password123"
    return data


def test_create_user(service, payload, monkeypatch):
    monkeypatch.setattr(
        "services.user.hash_password",
        lambda password: "hashed_password",
    )
    service.repository.get_by_email.return_value = None
    service.repository.create.side_effect = lambda user: user

    result = service.create(payload)

    assert result.name == "Alice"
    assert result.email == "alice@example.com"
    assert result.hashed_password == "hashed_password"
    assert result.deleted_at is None
    service.repository.create.assert_called_once()


def test_create_duplicate_user(service, payload):
    service.repository.get_by_email.return_value = SimpleNamespace(
        email="alice@example.com"
    )

    with pytest.raises(ResourceExistedError):
        service.create(payload)

    service.repository.create.assert_not_called()


def test_read_one_user(service):
    user = SimpleNamespace(id=1, name="Alice")
    service.repository.get_by_id.return_value = user

    result = service.read_one(1)

    assert result == user
    service.repository.get_by_id.assert_called_once_with(1)


def test_update_user_details(service):
    user = SimpleNamespace(id=1, name="Alice", email="alice@example.com")
    updated_user = SimpleNamespace(id=1, name="Alice Smith")

    payload = MagicMock()
    payload.model_dump.return_value = {"name": "Alice Smith"}

    service.repository.get_by_id.return_value = user
    service.repository.update.return_value = updated_user

    result = service.update(1, payload)

    assert result.name == "Alice Smith"
    service.repository.update.assert_called_once_with(
        user, {"name": "Alice Smith"}
    )


def test_update_user_password(service, monkeypatch):
    user = SimpleNamespace(
        id=1,
        name="Alice",
        email="alice@example.com",
        hashed_password="old_hash",
    )

    payload = MagicMock()
    payload.model_dump.return_value = {"password": "new_password"}

    monkeypatch.setattr(
        "services.user.hash_password",
        lambda password: "new_hash",
    )

    service.repository.get_by_id.return_value = user
    service.repository.update.return_value = user

    result = service.update(1, payload)

    assert result.hashed_password == "new_hash"
    service.repository.update.assert_called_once_with(user, {})


def test_delete_user_soft_delete(service):
    user = SimpleNamespace(
        id=1,
        name="Alice",
        email="alice@example.com",
        hashed_password="hashed_password",
        deleted_at=None,
    )
    service.repository.get_by_id.return_value = user

    result = service.delete(1)

    assert result == {"message": "deleted"}
    assert user.name is None
    assert user.email is None
    assert user.hashed_password is None
    assert isinstance(user.deleted_at, datetime)
    service.repository.save.assert_called_once()


def test_create_user_rolls_back_on_error(service, payload, monkeypatch):
    monkeypatch.setattr(
        "core.security.hash_password",
        lambda password: "hashed_password",
    )
    service.repository.get_by_email.return_value = None
    service.repository.create.side_effect = Exception("Database error")

    with pytest.raises(Exception, match="Database error"):
        service.create(payload)

    service.db.rollback.assert_called_once()


def test_update_duplicate_email(service):
    user = SimpleNamespace(id=1, email="alice@example.com")
    existing_user = SimpleNamespace(id=2, email="bob@example.com")

    payload = MagicMock()
    payload.model_dump.return_value = {"email": "bob@example.com"}

    service.repository.get_by_id.return_value = user
    service.repository.get_by_email.return_value = existing_user

    with pytest.raises(ResourceExistedError):
        service.update(1, payload)

    service.repository.update.assert_not_called()
