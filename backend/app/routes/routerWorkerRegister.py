
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemasWorkerRegister import CreateWorkerRegister, WorkerResponse, WorkerLogin
from app.services.crudWorkerRegister import create_worker_register, get_all_workers, get_worker_by_email, get_worker_by_id,delete_worker_by_id, worker_Login
from app.db.database import get_db
from app.core.dependency import get_current_user,admin_only,worker_only

worker_register_router = APIRouter(prefix="/worker-registers", tags=["Worker Registers "])

@worker_register_router.post("/workers")
def worker_register_router_endpoint( workers: CreateWorkerRegister,db:Session=Depends(get_db)):
    return create_worker_register(db, workers)

@worker_register_router.get("/workers",response_model=list[WorkerResponse])
def get_all_workers_endpoint(db:Session=Depends(get_db), admin: dict = Depends(admin_only)):
    return get_all_workers(db)


@worker_register_router.get("/worker-registers/{phoneNumber}", response_model=WorkerResponse)
def get_worker_by_email_endpoint(phoneNumber: str, db: Session = Depends(get_db), admin: dict = Depends(admin_only)):
    worker = get_worker_by_email(db, phoneNumber)
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@worker_register_router.get("/{id}",response_model=WorkerResponse)
def get_worker_by_id_endpoint(id:int, db:Session=Depends(get_db), admin: dict = Depends(admin_only)):
    return get_worker_by_id(db,id)


@worker_register_router.delete("/worker-registers/{id}")
def delete_worker_by_id_endpoint(id:int, db:Session=Depends(get_db), admin: dict = Depends(admin_only)):
    return delete_worker_by_id(db, id)



@worker_register_router.post("/login")
def worker_login_endpoint(credentials:WorkerLogin, db: Session = Depends(get_db)):
    return worker_Login(db, credentials.email, credentials.password)


