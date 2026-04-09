from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """
    Repository for User persistence operations.
    Handles all database queries for User entities.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[User]:
        """Fetch all users from database."""
        stmt = select(User)
        return list(self.db.scalars(stmt).all())

    def search_by_family_name(self, family_name: str) -> list[User]:
        """Fetch users whose family name matches the search text (case-insensitive)."""
        stmt = select(User).where(User.family_name.ilike(f"%{family_name}%"))
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, user_id: int) -> User | None:
        """Fetch a user by ID. Returns None if not found."""
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        """Fetch a user by email. Returns None if not found."""
        stmt = select(User).where(User.email == email)
        return self.db.scalars(stmt).first()

    def create(self, user: User) -> User:
        """
        Persist a user and return the refreshed entity.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """
        Delete a user and commit the transaction.
        """
        self.db.delete(user)
        self.db.commit()
