from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.user_schema import UserBase, UserRegister, UserRegisterInternal, UserLogin, UserBaseResponse
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException
from datetime import datetime

# Iniciar sesión de usuario
def login_user(db: Session, user_data: UserLogin):
    try:
        
        user = db.query(User).filter(User.mail == user_data.mail).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        is_valid = verify_password(user_data.pass_, user.pass_)
        if not is_valid:
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        
        token = create_access_token(data={"user_id": user.id, "mail": user.mail})
        user_response = UserBaseResponse(name=user.name, mail=user.mail, id=user.id, created_at=user.dateCreated)

        return {"user": user_response, "token": token}
    except HTTPException:
        # re-lanzar excepciones HTTP para que FastAPI las maneje
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar sesión: {str(e)}")


# Crear usuario
def create_user(db: Session, user_data: UserRegister):
    try:
        password_hashed = hash_password(user_data.pass_)
        user_dict = UserRegisterInternal(**{
            **user_data.model_dump(),
            "pass_": password_hashed,
            "dateCreated": datetime.now()
            })

        # Validar si ya existe
        existing_user = db.query(User).filter(User.mail == user_data.mail).first()
        
        if existing_user:
            raise HTTPException(status_code=409, detail="El email ya está registrado")
        
        new_user = User(**user_dict.model_dump())
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except HTTPException:
        # re-lanzar excepciones HTTP para que FastAPI las maneje
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear el usuario: {str(e)}")


# Actualizar información de usuario
def update_user(db: Session, user_id: int, user_data: UserBase):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Actualizar los campos del usuario
        for key, value in user_data.model_dump().items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return {"message": "Usuario actualizado exitosamente", "user": user}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar el usuario: {str(e)}")


# Obtener un usuario por ID
def get_user_by_id(db: Session, user_id: int):

    user = db.query(User).filter(User.id == user_id and User.isActive == True).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    data_user = UserBaseResponse(name=user.name, mail=user.mail, id=user.id, created_at=user.dateCreated)
    return data_user


# Obtener lista de usuarios
def get_all_users(db: Session):

    users = db.query(User).filter(User.isActive == True).all()
    user_data = [UserBaseResponse(name=user.name, mail=user.mail, id=user.id, created_at=user.dateCreated) for user in users]
    return user_data