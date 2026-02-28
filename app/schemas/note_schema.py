from pydantic import BaseModel
from datetime import datetime

class NotesBase(BaseModel):
    title: str
    content: str

class NotesInsert(NotesBase):
    userUpdated: int
    dateCreated: datetime
    dateUpdated: datetime
    userCreated: int


class CreateNote(NotesBase):
    userCreated: int


    class Config:
        from_attributes = True