from sqlalchemy.orm import Session
from app.models.modelWorkerRegister import ModelWorkerRegister
from app.schemas.schemasWorkerRegister import CreateWorkerRegister
from fastapi import HTTPException

def create_worker_register(db:Session, worker_register:CreateWorkerRegister):

    if db.query(ModelWorkerRegister).filter(ModelWorkerRegister.email == worker_register.email).first():
        raise ValueError("Email already exists")

    if worker_register.password != worker_register.confirm_password:
        raise ValueError("Password and confirm password do not match")
    

    db_worker_register=ModelWorkerRegister(
        name=worker_register.name,
        email=worker_register.email,
        password=worker_register.password
    )
    db.add(db_worker_register)
    db.commit()
    db.refresh(db_worker_register)
    return db_worker_register


def get_all_workers(db: Session):
    workers=db.query(ModelWorkerRegister).all()
    print(f"Queried all workers, Found: {workers}")
    return workers


def get_worker_by_email(db: Session, email: str):
    user = db.query(ModelWorkerRegister).filter(ModelWorkerRegister.email == email).first()
    print(f"Queried email: {email}, Found: {user}")
    return user


def get_worker_by_id(db:Session, worker_id:int):
    user=db.query(ModelWorkerRegister).filter(ModelWorkerRegister.id == worker_id).first()
    print(f"Queried ID: {worker_id}, Found:{user}")
    if not user:
        raise HTTPException(status_code=404, detail="worker not found")
    
    return user


