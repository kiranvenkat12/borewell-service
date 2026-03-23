from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.modelAdminRegister import AdminRegister
from app.schemas.schemasAdminRegister import CreateRegistration, LoginAdmin
import os
from app.core.security import hash_password, verify_password
from app.core.auth import create_access_token
from app.core.dependency import get_current_user
import shutil

admin_id=os.environ.get("borewell_service_admin_id")

def create_admin(db:Session, user:CreateRegistration):
    if user.new_password != user.confirm_password:
        raise ValueError("passwords do not match")
    
    if db.query(AdminRegister).filter(AdminRegister.email == user.email).first():
        raise ValueError("email already exists")
    
    if user.admin_id != admin_id:
        raise ValueError("invalid admin id")
    
    hashed_password=hash_password(user.new_password)

    db_user=AdminRegister(
        name=user.name,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_admin(db:Session, credentials:LoginAdmin):
    user=db.query(AdminRegister).filter(AdminRegister.email == credentials.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email ")
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid  password")
    
    token=create_access_token(user_id=user.id, role=user.role)

    return {"message": "Login successful", "access_token": token, "token_type": "bearer"}


def get_admin(db:Session):
    return db.query(AdminRegister).all()






