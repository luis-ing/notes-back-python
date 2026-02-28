from sqlalchemy.orm import Session
from app.models.models import Notes
from app.schemas.note_schema import NotesBase, CreateNote, NotesInsert
from fastapi import HTTPException
from datetime import datetime

# Crear nota
def create_note(db: Session, note_data: CreateNote):
    try:
        data_note = NotesInsert(
            title=note_data.title,
            content=note_data.content,
            userCreated=note_data.userCreated,
            userUpdated=note_data.userCreated,
            dateCreated=datetime.now(),
            dateUpdated=datetime.now()
        )
        
        new_note = Notes(**data_note.model_dump())
        db.add(new_note)
        db.commit()
        db.refresh(new_note)
        return {"message": "Nota creada exitosamente", "note": new_note}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear la nota: {str(e)}")

# Actualizar información
def update_note(db: Session, note_id: int, note_data: NotesBase):
    try:
        note = db.query(Notes).filter(Notes.id == note_id and Notes.isActive == True).first()
        
        if not note:
            raise HTTPException(status_code=404, detail="Nota no encontrada o inactiva")
        
        for key, value in note_data.model_dump().items():
            setattr(note, key, value)
            
        note.userUpdated = note_data.userCreated
        note.dateUpdated = datetime.now()
            
        db.commit()
        db.refresh(note)
        return {"message": "Nota actualizada exitosamente", "note": note}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar la nota: {str(e)}")

# Eliminar nota
def delete_note(db: Session, note_id: int):
    try:
        note = db.query(Notes).filter(Notes.id == note_id and Notes.isActive == True).first()
        if not note:
            raise HTTPException(status_code=404, detail="Nota no encontrada o inactiva")
        
        note.isActive = False
        db.commit()
        return {"message": "Nota eliminada exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar la nota: {str(e)}")
    
# Obtener nota por id
def get_note_by_id(db: Session, note_id: int):
    note = db.query(Notes).filter(Notes.id == note_id and Notes.isActive == True).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="Nota no encontrada o inactiva")
    
    return note

# Obtener listado de notas por usuario
def get_notes_by_user(db: Session, user_id: int):
    notes = db.query(Notes).filter(Notes.userCreated == user_id and Notes.isActive == True).all()
    
    return notes