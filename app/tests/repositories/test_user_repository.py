from datetime import date

from app.models.user import User
from app.repositories.user_repository import UserRepository


def test_user_repository_create_get_list_and_delete(db_session) -> None:
    repository = UserRepository(db_session)
    user = User(
        family_name="Doe",
        given_name="Jane",
        birth_date=date(1990, 1, 2),
        email="jane.doe@example.com",
    )

    repository.create(user)
    db_session.commit()

    assert repository.get_by_id(user.id) == user
    assert repository.list_all() == [user]

    repository.delete(user)
    db_session.commit()

    assert repository.get_by_id(user.id) is None
    assert repository.list_all() == []


def test_user_repository_search_by_family_name(db_session) -> None:
    repository = UserRepository(db_session)
    user_one = User(
        family_name="Dove",
        given_name="Jane",
        birth_date=date(1990, 1, 2),
        email="jane.doe@example.com",
    )
    user_two = User(
        family_name="Dover",
        given_name="John",
        birth_date=date(1988, 3, 4),
        email="john.dover@example.com",
    )
    user_three = User(
        family_name="Smith",
        given_name="Ann",
        birth_date=date(1992, 5, 6),
        email="ann.smith@example.com",
    )

    repository.create(user_one)
    repository.create(user_two)
    repository.create(user_three)
    db_session.commit()

    results = repository.search_by_family_name("ov")

    assert len(results) == 2
    assert user_one in results
    assert user_two in results
