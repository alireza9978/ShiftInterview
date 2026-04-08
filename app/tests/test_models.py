from app.models.permission import Permission
from app.models.user import User


def test_user_model_table_and_columns() -> None:
    assert User.__tablename__ == "users"

    columns = User.__table__.columns
    assert set(columns.keys()) == {
        "id",
        "family_name",
        "given_name",
        "birthdate",
        "email",
    }
    assert columns["id"].primary_key is True
    assert columns["email"].unique is True
    assert columns["email"].nullable is False


def test_permission_model_table_and_columns() -> None:
    assert Permission.__tablename__ == "permissions"

    columns = Permission.__table__.columns
    assert set(columns.keys()) == {"id", "type", "granted_date", "user_id"}
    assert columns["id"].primary_key is True
    assert columns["user_id"].nullable is False

    fk_targets = {fk.target_fullname for fk in columns["user_id"].foreign_keys}
    assert fk_targets == {"users.id"}


def test_user_permission_relationships() -> None:
    assert User.permissions.property.mapper.class_ is Permission
    assert Permission.user.property.mapper.class_ is User
