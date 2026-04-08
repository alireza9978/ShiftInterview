from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import User as UserSchema
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


def _get_user_or_404(user_id: int, db: Session) -> UserModel:
    """Helper to fetch a user by ID or raise 404."""
    user = db.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.get("", response_model=list[UserSchema])
def list_users(db: Session = Depends(get_db)) -> list[UserModel]:
    return db.query(UserModel).all()


@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserModel:
    return _get_user_or_404(user_id, db)


@router.post("", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def add_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserModel:
    existing_user = db.query(UserModel).filter(UserModel.email == payload.email).first()
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    user = UserModel(
        family_name=payload.family_name,
        given_name=payload.given_name,
        birthdate=payload.birthdate,
        email=payload.email,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(user_id: int, db: Session = Depends(get_db)) -> Response:
    user = _get_user_or_404(user_id, db)
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
