from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.routes import permissions_router, users_router
from app.core.config import settings
from app.core.database import Base, engine, get_db

app = FastAPI(title=settings.app_name, version=settings.app_version)

Base.metadata.create_all(bind=engine)
app.include_router(users_router, prefix="/api")
app.include_router(permissions_router, prefix="/api")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "ShiftInterview FastAPI app is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
def health_db(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
