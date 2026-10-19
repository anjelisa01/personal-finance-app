
#==================================AUTH

from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from repositories.auth import AuthRepository


def test_get_user_by_email_found():
    db = MagicMock(spec=Session)
    repo = AuthRepository(db)

    user = MagicMock()
    db.scalars.return_value.first.return_value = user

    result = repo.get_user_by_email("alice@example.com")

    assert result == user
    db.scalars.assert_called_once()


def test_get_user_by_email_not_found():
    db = MagicMock(spec=Session)
    repo = AuthRepository(db)

    db.scalars.return_value.first.return_value = None

    result = repo.get_user_by_email("unknown@example.com")

    assert result is None
    db.scalars.assert_called_once()