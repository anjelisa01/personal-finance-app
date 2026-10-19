
#==================================USER

from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from repositories.user import UserRepository


def make_repo():
    db = MagicMock(spec=Session)
    return UserRepository(db), db


def test_get_by_email():
    repo, db = make_repo()
    user = MagicMock()

    db.scalars.return_value.first.return_value = user

    result = repo.get_by_email("alice@example.com")

    assert result == user
    db.scalars.assert_called_once()


def test_get_by_id():
    repo, db = make_repo()
    user = MagicMock()

    db.scalar.return_value = user

    result = repo.get_by_id(1)

    assert result == user
    db.scalar.assert_called_once()


def test_create_user():
    repo, db = make_repo()
    user = MagicMock()

    result = repo.create(user)

    assert result == user
    db.add.assert_called_once_with(user)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)


def test_update_user():
    repo, db = make_repo()
    user = MagicMock()

    result = repo.update(user, {"name": "Alice"})

    assert user.name == "Alice"
    assert result == user
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)


def test_save():
    repo, db = make_repo()

    repo.save()

    db.commit.assert_called_once()




#==================================DASHBOARD
#--------------------SKIP,DOESNT DO ANYTHING
