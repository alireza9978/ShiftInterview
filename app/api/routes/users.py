from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import (
    EmailAlreadyExistsError,
    UserNotFoundError,
    UserService,
)

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """
    Dependency injection for UserService.
    Creates service with repository for each request.
    """
    repository = UserRepository(db)
    return UserService(repository=repository, db=db)


@router.get("", response_model=list[UserRead])
def list_users(
    family_name: str | None = Query(default=None),
    service: UserService = Depends(get_user_service),
) -> list[User]:
    """
    List all users, optionally filtered by family name.
    """
    if family_name is not None:
        return service.search_users_by_family_name(family_name)

    return service.list_users()


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)) -> User:
    """
    Get a user by ID.
    """
    try:
        return service.get_user(user_id)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def add_user(
    payload: UserCreate, service: UserService = Depends(get_user_service)
) -> User:
    """
    Create a new user.
    """
    try:
        return service.create_user(payload)
    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    user_id: int, service: UserService = Depends(get_user_service)
) -> Response:
    """
    Delete a user by ID.
    """
    try:
        service.delete_user(user_id)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
