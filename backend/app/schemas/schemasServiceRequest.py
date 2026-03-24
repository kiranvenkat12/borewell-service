from pydantic import BaseModel,Field,field_validator,EmailStr
from typing import Optional
from datetime import datetime

class CreateSchemasServiceRequest(BaseModel):
    name: str = Field(..., max_length=100)
    phone_primary: str = Field(..., max_length=20)
    phone_secondary: str = Field(None, max_length=20)
    email: EmailStr = Field(None)
    service_type: str = Field(..., max_length=100)
    borewell_depth: int = Field(..., ge=0)
    address: str = Field(..., max_length=200)
    area: str = Field(..., max_length=100)
    pincode: str = Field(..., max_length=10)
    description: str = Field(None, max_length=200)
    
class ResponseSchemasServiceRequest(BaseModel):
    id: int
    name: str
    phone_primary: str
    phone_secondary: str
    email: EmailStr
    service_type: str
    borewell_depth: int
    address: str
    area: str
    pincode: str
    description: str
    status: str
    assigned_worker_id: Optional[int] = None
    assigned_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        orm_mode=True
