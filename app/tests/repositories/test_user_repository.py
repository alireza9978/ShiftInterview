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
