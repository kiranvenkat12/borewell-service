from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
class ModelWorkerRegister(Base):
    __tablename__ = "model_worker_registers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

