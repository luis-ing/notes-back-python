from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    name: str
    mail: EmailStr

class UserBaseResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserRegister(UserBase):
    pass_: str
    
class UserRegisterInternal(UserBase):
    pass_: str
    dateCreated: datetime
    
class UserLogin(BaseModel):
    mail: EmailStr
    pass_: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True