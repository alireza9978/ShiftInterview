from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    family_name: str
    given_name: str
    birthdate: date
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Backward-compatible alias used in existing tests.
User = UserRead
