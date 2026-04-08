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

    def get_by_id(self, user_id: int) -> User | None:
        """Fetch a user by ID. Returns None if not found."""
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        """Fetch a user by email. Returns None if not found."""
        stmt = select(User).where(User.email == email)
        return self.db.scalars(stmt).first()

    def create(self, user: User) -> User:
        """
        Add a user to the database session.
        """
        self.db.add(user)
        return user

    def delete(self, user: User) -> None:
        """
        Mark a user for deletion in the database session.
        """
        self.db.delete(user)
