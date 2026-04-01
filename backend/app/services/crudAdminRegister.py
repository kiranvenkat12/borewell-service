from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.modelAdminRegister import AdminRegister
from app.schemas.schemasAdminRegister import CreateRegistration, LoginAdmin
import os
from app.core.security import hash_password, verify_password
from app.core.auth import create_access_token
from app.core.dependency import get_current_user
import shutil

def get_admin_id_from_file():
    secret_path = "/etc/secrets/borewell_service_admin_id"
    try:
        with open(secret_path, "r") as f:
            return f.read().strip()  # removes any extra newline or spaces
    except FileNotFoundError:
        raise ValueError("Server admin ID secret file not found")
    

    
def create_admin(db:Session, user:CreateRegistration):
    admin_id=get_admin_id_from_file()

    if user.new_password != user.confirm_password:
        raise ValueError("passwords do not match")
    
    if db.query(AdminRegister).filter(AdminRegister.email == user.email).first():
        raise ValueError("email already exists")
    
    if user.admin_id != admin_id:
        raise HTTPException(status_code=400, detail="Invalid admin ID")    
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


#delete the admin
def delete_admin(db:Session, admin_id:int):

    admin=db.query(AdminRegister).filter(AdminRegister.id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    db.delete(admin)
    db.commit()
    return {"message": "Admin deleted successfully"}








