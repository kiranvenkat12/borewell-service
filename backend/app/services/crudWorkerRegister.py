from sqlalchemy.orm import Session
from app.models.modelWorkerRegister import ModelWorkerRegister
from app.schemas.schemasWorkerRegister import CreateWorkerRegister
from app.core.security import  hash_password, verify_password
from app.core.dependency import get_current_user,admin_only,worker_only
from app.core.auth import create_access_token
from fastapi import HTTPException
from app.core.security import hash_password, verify_password

from app.core.security import verify_password

def create_worker_register(db:Session, worker_register:CreateWorkerRegister):

    if db.query(ModelWorkerRegister).filter(ModelWorkerRegister.phoneNumber  == worker_register.phoneNumber).first():
        raise ValueError("Phone number already exists")

    if worker_register.password != worker_register.confirm_password:
        raise ValueError("Password and confirm password do not match")
    raw_pass = worker_register.password
    hashed_password=hash_password(raw_pass)

    db_worker_register=ModelWorkerRegister(
        name=worker_register.name,
        phoneNumber=worker_register.phoneNumber,
        password=hashed_password
    )
    db.add(db_worker_register)
    db.commit()
    db.refresh(db_worker_register)
    return db_worker_register


def get_all_workers(db: Session):
    workers=db.query(ModelWorkerRegister).all()
    print(f"Queried all workers, Found: {workers}")
    return workers


def get_worker_by_email(db: Session, phoneNumber: str):
    user = db.query(ModelWorkerRegister).filter(ModelWorkerRegister.phoneNumber == phoneNumber).first()
    print(f"Queried phone number: {phoneNumber}, Found: {user}")
    return user


def get_worker_by_id(db:Session, worker_id:int):
    user=db.query(ModelWorkerRegister).filter(ModelWorkerRegister.id == worker_id).first()
    print(f"Queried ID: {worker_id}, Found:{user}")
    if not user:
        raise HTTPException(status_code=404, detail="worker not found")
    
    return user

#delete worker by id
def delete_worker_by_id(db:Session, worker_id:int):
    user=db.query(ModelWorkerRegister).filter(ModelWorkerRegister.id == worker_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="worker not found")
    
    db.delete(user)
    db.commit()
    return {"message": "Worker deleted successfully"}


def worker_Login(db:Session, email:str, password:str):
    worker = db.query(ModelWorkerRegister).filter(ModelWorkerRegister.email == email).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    if not verify_password(password, worker.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    token=create_access_token(user_id=worker.id, role="worker")

    return {"message": "Login successful", "access_token": token, "token_type": "bearer"}
    
    return worker