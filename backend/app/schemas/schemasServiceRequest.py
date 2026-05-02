from pydantic import BaseModel,Field,field_validator,EmailStr
from typing import Optional
from datetime import datetime

class CreateSchemasServiceRequest(BaseModel):
    name: str = Field(..., max_length=100)
    phone_primary: str = Field(..., max_length=20)
    phone_secondary: Optional[str] = Field(None, max_length=20)
    
    service_type: str = Field(..., max_length=100)
    borewell_depth: Optional[int] = Field(None, ge=0)
    address: str = Field(..., max_length=200)
    
    pincode: str = Field(..., max_length=10)
    description: Optional[str] = Field(None, max_length=200)
    @field_validator("borewell_depth", mode="before")
    @classmethod
    def validate_depth(cls, v):
        if v == "" or v is None:
            return None
        return int(v)
    
class ResponseSchemasServiceRequest(BaseModel):
    id: int
    name: str
    phone_primary: str
    phone_secondary: str
    
    service_type: str
    borewell_depth: Optional[int]
    address: str
   
    pincode: str
    description: str
    status: str
    assigned_worker_id: Optional[int] = None
    assigned_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True



class AssignWorkerRequest(BaseModel):
    worker_id: int
    request_id: int       


class BorewellDetails(BaseModel):
         bore_depth: float
         water_level:float
         casing_diameter: float
         floors_supply: int
         electricity_supply:int
         usage_type:int
         class Config:
             from_attributes = True


