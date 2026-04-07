from pydantic import BaseModel,Field, field_validator
from typing import Optional


class CreateCustomerRegister(BaseModel):
    name: str = Field(..., example="Jane Doe")
    phoneNumber: str = Field(..., example="0987654321")
    password: str = Field(..., example="password123")

    @field_validator('password')
    def validatepassword(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        
        return value    
    


class CustomerResponse(BaseModel):
    id: int
    name: str
    phoneNumber: str

    class Config:
        from_attributes = True

class CustomerLogin(BaseModel):
    phoneNumber: str = Field(..., example="0987654321")
    password: str = Field(..., example="password123")



class BorewellInfo(BaseModel):
    id: int
    customer_id: int
    borewell_depth: float
    casing_depth: float
    water_level: float
    pipe_size: Optional[str] = None
    pipe_joint: Optional[str] = None
    video_url: Optional[str] = None

    class Config:
        from_attributes = True

        
        