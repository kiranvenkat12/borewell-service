from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Register(Base):
    
    __tablename__ ="registers"

    id =Column(Integer, primary_key=True, index=True)
    name =Column(String)
    email=Column(String, unique=True, nullable=False)
    password=Column(String)

    