
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.crudserviceRequest import create_service_request,get_service_request,get_all_service_requests,get_request_for_worker,assign_worker,start_work_request,complete_service_request
from app.schemas.schemasServiceRequest import CreateSchemasServiceRequest, ResponseSchemasServiceRequest
from app.db.database import get_db
from app.core.dependency import get_current_user,admin_only
service_requests_router = APIRouter(prefix="/service-requests", tags=["Service Requests"])


@service_requests_router.post("/")
def create_service_request_endpoint(service_request: CreateSchemasServiceRequest,db: Session =Depends(get_db)):
    return create_service_request(db, service_request)


@service_requests_router.get("/{service_request_id}")
def get_service_request_endpoint(service_request_id: int, db: Session = Depends(get_db)):
    return get_service_request(db, service_request_id)


@service_requests_router.get("/", response_model=list[ResponseSchemasServiceRequest])
def get_all_service_requests_endpoint(db: Session = Depends(get_db), admin: dict=Depends(admin_only)):
    return get_all_service_requests(db)

#showing the all requests to worker 

@service_requests_router.get("/{worker_id}",response_model=List[ResponseSchemasServiceRequest])
def assign_work_endpoint(worker_id:int, db:Session=Depends(get_db)):
    request=get_request_for_worker(db, worker_id)
    if not request:
        raise HTTPException(status_code=404, detail="No requests found for this worker")
    return request


#admin will assign the request to worker and change the status to assigned

@service_requests_router.put("/{service_request_id}/{worker_id}", response_model=list[ResponseSchemasServiceRequest])
def assign_work(service_request_id : int,worker_id:int,db:Session=Depends(get_db) ):
    request=assign_worker(db,service_request_id,worker_id)
    return request

#worker will start the process
@service_requests_router.put("/{service_request_id}/start",  response_model=list[ResponseSchemasServiceRequest])
def start_work_request_endpoint(service_request_id:int,db:Session=Depends(get_db)):
    start_request=start_work_request(db,service_request_id)
    return start_request


#worker will completed the prosess
@service_requests_router.put("/{service_request_id}/complete", response_model=list[ResponseSchemasServiceRequest])
def complete_service_request(service_request_id:int,db:Session=Depends(get_db)):
    request=complete_service_request(db,service_request_id)
    return request











