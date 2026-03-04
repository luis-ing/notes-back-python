from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.schemas.note_schema import CreateNote
from app.services import notes_service
from app.core.security import validate_token

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
    # dependencies=[Depends(validate_token)],
)

@router.get("/")
def list_notes( db: Session = Depends(get_db), token_data: dict = Depends(validate_token)):
    user_id = token_data["user_id"]
    return notes_service.get_notes_by_user(db, user_id)

@router.get("/{note_id}")
def get_note_by_id(note_id: int, db: Session = Depends(get_db), token_data: dict = Depends(validate_token)):
    user_id = token_data["user_id"]
    return notes_service.get_note_by_id(db, note_id, user_id)

@router.post("/create")
def create_note(note_data: CreateNote, db: Session = Depends(get_db)):
    
    return notes_service.create_note(db, note_data)

@router.put("/update/{note_id}")
def update_note(note_id: int, note_data: CreateNote, db: Session = Depends(get_db)):
    return notes_service.update_note(db, note_id, note_data)