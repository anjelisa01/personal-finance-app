from unittest.mock import MagicMock
from types import SimpleNamespace

import pytest
import service.auth as auth_module

from service.auth import AuthService
from schemas.auth import UserLogin
from core.exceptions import AuthFailedCredential


def make_service():
    db = MagicMock()
    service = AuthService(db)
    service.repository = MagicMock()
    return service


def test_login_success(monkeypatch):
    service = make_service()

    user = SimpleNamespace(
        id=1,
        hashed_password="hashed_password",
    )
    service.repository.get_user_by_email.return_value = user

    monkeypatch.setattr(
        auth_module, "verify_password", lambda password, hashed: True
    )
    monkeypatch.setattr(
        auth_module, "create_access_token", lambda data: "fake-token"
    )

    payload = UserLogin(
        email="alice@example.com",
        password="secret123",
    )

    result = service.login(payload)

    assert result == {
        "access_token": "fake-token",
        "token_type": "bearer",
    }

    service.repository.get_user_by_email.assert_called_once_with(
        payload.email
    )


def test_login_user_not_found(monkeypatch):
    service = make_service()
    service.repository.get_user_by_email.return_value = None

    monkeypatch.setattr(
        auth_module,
        "verify_password",
        MagicMock(),
    )

    payload = UserLogin(
        email="unknown@example.com",
        password="secret123",
    )

    with pytest.raises(AuthFailedCredential):
        service.login(payload)

    auth_module.verify_password.assert_not_called()


def test_login_wrong_password(monkeypatch):
    service = make_service()

    user = SimpleNamespace(
        id=1,
        hashed_password="hashed_password",
    )
    service.repository.get_user_by_email.return_value = user

    monkeypatch.setattr(
        auth_module, "verify_password", lambda password, hashed: False
    )

    payload = UserLogin(
        email="alice@example.com",
        password="wrong-password",
    )

    with pytest.raises(AuthFailedCredential):
        service.login(payload)