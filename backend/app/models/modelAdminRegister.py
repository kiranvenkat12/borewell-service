from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.orm import relationship

class AdminRegister(Base):
    
    __tablename__ ="admin_registers"

    id =Column(Integer, primary_key=True, index=True)
    name =Column(String)
    email=Column(String, unique=True, nullable=False)
    password=Column(String)
    role=Column(String, default="admin")

    service_request=relationship("MOdelServiceRequest", back_populates="admin")

    