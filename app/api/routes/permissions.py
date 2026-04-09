from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.permission import Permission as PermissionModel
from app.repositories.permission_repository import PermissionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.permission import Permission, PermissionCreate
from app.services.permission_service import (
    PermissionNotFoundError,
    PermissionService,
    UserNotFoundError,
)

router = APIRouter(prefix="/permissions", tags=["permissions"])


def get_permission_service(db: Session = Depends(get_db)) -> PermissionService:
    """
    Dependency injection for PermissionService.
    Creates service with repository for each request.
    """
    repository = PermissionRepository(db)
    user_repository = UserRepository(db)
    return PermissionService(
        repository=repository,
        user_repository=user_repository,
    )


@router.get("", response_model=list[Permission])
def list_permissions(
    user_id: int | None = None,
    service: PermissionService = Depends(get_permission_service),
) -> list[PermissionModel]:
    """
    List permissions, optionally filtered by user_id.
    """
    return service.list_permissions(user_id=user_id)


@router.post("", response_model=Permission, status_code=status.HTTP_201_CREATED)
def grant_permission(
    payload: PermissionCreate,
    service: PermissionService = Depends(get_permission_service),
) -> PermissionModel:
    """
    Create and Grant a permission to a user.
    """
    try:
        return service.grant_permission(payload)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get("/{permission_id}", response_model=Permission)
def get_permission(
    permission_id: int,
    service: PermissionService = Depends(get_permission_service),
) -> PermissionModel:
    """
    Get a permission by ID.
    """
    try:
        return service.get_permission(permission_id)
    except PermissionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_permission(
    permission_id: int,
    service: PermissionService = Depends(get_permission_service),
) -> Response:
    """
    Revoke a permission by ID.
    """
    try:
        service.revoke_permission(permission_id)
    except PermissionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
