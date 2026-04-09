from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserNotFoundError(Exception):
    """Raised when trying to access a user that doesn't exist."""

    pass


class EmailAlreadyExistsError(Exception):
    """Raised when trying to create a user with an email that already exists."""

    pass


class UserService:
    """
    Service layer for User logic.
    """

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def list_users(self) -> list[User]:
        """Get all users."""
        return self.repository.list_all()

    def search_users_by_family_name(self, family_name: str) -> list[User]:
        """Search users by family name (case-insensitive)."""
        return self.repository.search_by_family_name(family_name)

    def get_user(self, user_id: int) -> User:
        """Get a user by ID."""
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with ID {user_id} not found")
        return user

    def create_user(self, payload: UserCreate) -> User:
        """Create a new user."""
        # email must be unique
        existing_user = self.repository.get_by_email(str(payload.email))
        if existing_user is not None:
            raise EmailAlreadyExistsError(f"Email {payload.email} already exists")

        # Create new User model from validated schema data
        user = User(
            family_name=payload.family_name,
            given_name=payload.given_name,
            birth_date=payload.birth_date,
            email=str(payload.email),
        )

        # Persist to database
        return self.repository.create(user)

    def delete_user(self, user_id: int) -> None:
        """
        Delete a user by ID.
        """
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"User with ID {user_id} not found")

        self.repository.delete(user)
