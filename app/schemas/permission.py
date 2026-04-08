from datetime import date

from pydantic import BaseModel, ConfigDict


class PermissionBase(BaseModel):
    type: str
    granted_date: date


class PermissionCreate(PermissionBase):
    pass


class Permission(PermissionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
