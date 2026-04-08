from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.database import Base

class ModelCustomerRegistration(Base):
    __tablename__ = "model_customer_registrations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phoneNumber = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relationship to borewell info
    borewells = relationship("BoreWellInfo", back_populates="customer")


class BoreWellInfo(Base):
    __tablename__ = "borewell_info"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("model_customer_registrations.id"), nullable=False)
    borewell_depth = Column(Float, nullable=False)
    phoneNumber = Column(String, nullable=False)
    casing_depth = Column(Float, nullable=False)
    water_level = Column(Float, nullable=False)
    pipe_size = Column(String, nullable=True)
    pipe_joint = Column(String, nullable=True)
    water_gaps = Column(String , nullable=True)
    casing_Condition = Column(String, nullable=True)
    pipe_Condition = Column(String, nullable=True)
    Water_Quality = Column(String, nullable=True)

    tds = Column(Float, nullable=True)
    ph = Column(Float, nullable=True)
    hardness = Column(Float, nullable=True)
    iron = Column(Float, nullable=True)
    chlorine = Column(Float, nullable=True)
    nitrate = Column(Float, nullable=True)

    # Visual checks
    water_color = Column(String, nullable=True)
    water_smell = Column(String, nullable=True)

    # Final result
    water_quality_status = Column(String, nullable=True)



    # Relationship back to customer
    customer = relationship("ModelCustomerRegistration", back_populates="borewells")