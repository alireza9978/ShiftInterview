from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.permission import Permission as PermissionModel
from app.models.user import User as UserModel
from app.schemas.permission import Permission as PermissionSchema
from app.schemas.permission import PermissionCreate

router = APIRouter(prefix="/permissions", tags=["permissions"])


def _get_permission_or_404(permission_id: int, db: Session) -> PermissionModel:
    """Helper to fetch a permission by ID or raise 404."""
    permission = db.get(PermissionModel, permission_id)
    if permission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return permission


@router.get("", response_model=list[PermissionSchema])
def list_permissions(user_id: int | None = None, db: Session = Depends(get_db)) -> list[PermissionModel]:
    query = db.query(PermissionModel)
    if user_id is not None:
        query = query.filter(PermissionModel.user_id == user_id)
    return query.all()


@router.post("", response_model=PermissionSchema, status_code=status.HTTP_201_CREATED)
def grant_permission(payload: PermissionCreate, db: Session = Depends(get_db)) -> PermissionModel:
    # Verify user exists
    user = db.get(UserModel, payload.user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    permission = PermissionModel(
        type=payload.type,
        granted_date=payload.granted_date,
        user_id=payload.user_id,
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


@router.get("/{permission_id}", response_model=PermissionSchema)
def get_permission(permission_id: int, db: Session = Depends(get_db)) -> PermissionModel:
    return _get_permission_or_404(permission_id, db)


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_permission(permission_id: int, db: Session = Depends(get_db)) -> Response:
    permission = _get_permission_or_404(permission_id, db)
    db.delete(permission)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
