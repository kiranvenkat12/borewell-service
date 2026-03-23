
from sqlalchemy import Column,Integer,String,ForeignKey
from app.db.database import Base
from sqlalchemy.orm import relationship

class MOdelServiceRequest(Base):
    __tablename__ = "model_service_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_primary=Column(String)
    phone_secondary=Column(String)
    email=Column(String)
    service_type=Column(String)
    borewell_depth=Column(Integer)
    address=Column(String)
    area=Column(String)
    pincode=Column(String)
    description=Column(String)

    #admin fields
    status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)

    admin_id=Column(Integer, ForeignKey("admin_registers.id"))
    admin=relationship("AdminRegister", back_populates="service_request")
