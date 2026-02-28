from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.services import user_service
from app.core.security import validate_token

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    # attach token validation to every path in this router
    # dependencies=[Depends(validate_token)],
)

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, user_id)