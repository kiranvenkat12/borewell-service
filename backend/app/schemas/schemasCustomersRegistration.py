from pydantic import BaseModel,Field, field_validator
from typing import Optional, List, Dict, Any


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


from pydantic import BaseModel
from typing import Optional

class BorewellInfo(BaseModel):
    
    borewell_depth: float
    
    casing_depth: float
    water_level: float

    pipe_size: Optional[str] = None
    pipe_joint: Optional[str] = None
    water_gaps: Optional[str] = None
    casing_Condition: Optional[str] = None
    pipe_Condition: Optional[str] = None
    Water_Quality: Optional[str] = None

    tds: Optional[float] = None
    ph: Optional[float] = None
    hardness: Optional[float] = None
    iron: Optional[float] = None
    chlorine: Optional[float] = None
    nitrate: Optional[float] = None

    water_color: Optional[str] = None
    water_smell: Optional[str] = None

    water_quality_status: Optional[str] = None

    class Config:
        from_attributes = True

        
        
class AnalysisSchema(BaseModel):
    status: str
    color: str
    issues: List[str]
    solutions: Dict[str, List[str]]


class BorewellDataSchema(BaseModel):
    borewell_depth: float
    casing_depth: float
    water_level: float
    pipe_size: Optional[str] = None
    pipe_joint: Optional[str] = None
    water_gaps: Optional[str] = None
    casing_Condition: Optional[str] = None
    pipe_Condition: Optional[str] = None
    Water_Quality: Optional[str] = None
    tds: float | None
    ph: float | None
    hardness: float | None
    iron: float | None
    chlorine: float | None
    nitrate: float | None
    water_color: str | None
    water_smell: str | None
class RecommendationsSchema(BaseModel):
    drinking: Dict[str, List[str]]
    bathing: Dict[str, List[str]]
    washing: Dict[str, List[str]]

class BorewellResponseSchema(BaseModel):
    borewell_data: BorewellDataSchema
    analysis: AnalysisSchema
    recommendations: RecommendationsSchema 

    class Config:
        from_attributes = True  