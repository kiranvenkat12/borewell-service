from fastapi import APIRouter, Depends, HTTPException
from typing import List  # Added for list response model
from sqlalchemy.orm import Session
from app.db.database import get_db  # Removed unused SessionLocal
from app.services.crudAdminRegister import create_admin, login_admin, get_admin,delete_admin,get_borewell_info,send_borewell_info
from app.schemas.schemasAdminRegister import CreateRegistration, LoginAdmin
from app.core.dependency import get_current_user,admin_only , customer_only
from app.schemas.schemasCustomersRegistration import BorewellInfo ,BorewellResponseSchema
router = APIRouter(prefix="/admin", tags=["Admins"])

@router.post("/",)  # Fixed: response -> response_model
def create_admin_endpoint(user: CreateRegistration, db: Session = Depends(get_db)):
    return create_admin(db, user)


@router.post("/login")
def login_admin_endpoint(credentials:LoginAdmin, db: Session = Depends(get_db)):
    return login_admin(db, credentials)

@router.get("/admins")
def get_admins_endpoint(db: Session = Depends(get_db), current_user: dict = Depends(admin_only)):
    return get_admin(db)

@router.delete("/delete/{admin_id}")
def delete_admin_endpoint(admin_id: int, db: Session = Depends(get_db), current_user: dict = Depends(admin_only)):
    return delete_admin(db, admin_id)   

@router.post("/borewell-info/{customer_num}")
def send_borewell_info_endpoint(customer_num: str, borewell_data: BorewellInfo, db: Session = Depends(get_db), current_user: dict = Depends(admin_only)):
    return send_borewell_info(db, customer_num, borewell_data)
    
@router.get("/borewell-info/{customer_num}", response_model=List[BorewellResponseSchema])  # Added response_model for list of BorewellInfo
def get_borewell_info_endpoint(customer_num: str, db: Session = Depends(get_db), current_user: dict = Depends(customer_only)):
    return get_borewell_info(db, customer_num)

    