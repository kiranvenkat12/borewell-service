from pydantic import BaseModel,Field,field_validator,EmailStr


class CreateRegistration(BaseModel):
    name:str=Field(min_length=3, max_length=15)
    email:EmailStr
    new_password:str
    confirm_password:str
    admin_id:str

    
    @field_validator("new_password")
    def new_password(cls,value):
        
        if len(value)<8:
            raise ValueError("password must be more than 8 characters")
        if not any(i.isdigit()   for i in value):
            raise ValueError("password must contain atleast one digit")
        if not any(i.upper()   for i in value):
            raise ValueError("password must contain one upper case letter")
        
        return value
    

class LoginAdmin(BaseModel):
    email:EmailStr
    password:str

           



