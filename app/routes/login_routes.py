from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.user_schema import UserRegister, UserLogin
from app.services import user_service

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post("")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return user_service.login_user(db, user)

@router.post("/create")
def create_user(user: UserRegister, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)