# from sqlalchemy import Column, Integer, String
# from app.core.database import Base

# class User(Base):
#     __tablename__ = "user"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(60), nullable=False)
#     mail = Column(String(50), unique=True, index=True)
#     passw = Column(String(150), nullable=False)
#     isActive = Column(Integer, default=1)
#     dateCreated = Column(String(50), nullable=False)
