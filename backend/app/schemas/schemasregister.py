from pydantic import BaseModel,Field,field_validator


class CreateRegistration(BaseModel):
    name:str=Field(min_length=3, max_length=15)
    email:str
    password:str

    @field_validator("email")
    def email(cls,value):
        if not value.endswith("@gmail.com"):
            raise ValueError("email must ends with @gmail.com")
        
    @field_validator("password")
    def password(cls,value):
        
        if len(value)<8:
            raise ValueError("password must be more than 8 characters")
        if not any(i.isdigit()   for i in value):
            raise ValueError("password must contain atleast one digit")
        if not any(i.upper()   for i in value):
            raise ValueError("password must contain one upper case letter")
        
        return value
    

class RegisterResponse(BaseModel):
    id:int
    name:str
    email:str

    class Config:
        orm_mode=True
           



