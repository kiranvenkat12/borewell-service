
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemasWorkerRegister import CreateWorkerRegister, WorkerResponse
from app.services.crudWorkerRegister import create_worker_register, get_worker_by_email, get_worker_by_id
from app.db.database import get_db

worker_register_router = APIRouter(prefix="/worker-registers", tags=["Worker Registers "])

@worker_register_router.post("/workers")
def worker_register_router_endpoint( workers: CreateWorkerRegister,db:Session=Depends(get_db)):
    return create_worker_register(db, workers)

@worker_register_router.get("/{email}")
def get_worker_by_email_endpoint(email:str,db:Session=Depends(get_db), response_model=list[WorkerResponse] ):
    return get_worker_by_email(db,email)

@worker_register_router.get("/{id}")
def get_worker_by_id_endpoint(id:int, db:Session=Depends(get_db),response_model=list[WorkerResponse]):
    return get_worker_by_id(db,id)





