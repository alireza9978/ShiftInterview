from datetime import date

from app.models.permission import Permission
from app.models.user import User
from app.repositories.permission_repository import PermissionRepository


def test_permission_repository_create_list_by_user_and_delete(db_session) -> None:
    user = User(
        family_name="Doe",
        given_name="Jane",
        birthdate=date(1990, 1, 2),
        email="jane.doe@example.com",
    )
    db_session.add(user)
    db_session.commit()

    repository = PermissionRepository(db_session)
    permission = Permission(
        type="admin",
        granted_date=date(2026, 4, 8),
        user_id=user.id,
    )

    repository.create(permission)
    db_session.commit()

    assert repository.get_by_id(permission.id) == permission
    assert repository.list_all() == [permission]
    assert repository.list_by_user(user.id) == [permission]

    repository.delete(permission)
    db_session.commit()

    assert repository.get_by_id(permission.id) is None
    assert repository.list_all() == []
