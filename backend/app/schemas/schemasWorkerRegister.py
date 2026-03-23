from pydantic import BaseModel, EmailStr, Field,field_validator


class CreateWorkerRegister(BaseModel):
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    password: str = Field(..., example="password123")
    confirm_password: str = Field(..., example="password123")   
    @field_validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        
        return value
    

class WorkerResponse(BaseModel):
    name:str
    email:str


    
     
        
    
         