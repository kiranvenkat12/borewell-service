
from sqlalchemy import Column, DateTime,Integer,String,ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class MOdelServiceRequest(Base):
    __tablename__ = "model_service_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_primary=Column(String)
    phone_secondary=Column(String)
    service_type=Column(String)
    borewell_depth=Column(Integer)
    address=Column(String)
    pincode=Column(String)
    description=Column(String)

    #admin fields
    status = Column(String, default="Pending")
    created_at = Column(String)
    updated_at = Column(String)
    admin_id=Column(Integer, ForeignKey("admin_registers.id"))
    admin=relationship("AdminRegister", back_populates="service_request")

    #worker assignment
    assigned_worker_id=Column(Integer, ForeignKey("model_worker_registers.id"))
    worker=relationship("ModelWorkerRegister", back_populates="assigned_requests")
 

    assigned_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)