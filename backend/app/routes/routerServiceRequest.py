
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.services.crudserviceRequest import create_service_request,get_service_request,get_all_service_requests,get_requests_for_worker,assign_worker,start_work_request,complete_service_request,delete_service_request, get_all_assigned_service_requests,get_all_completed_service_requests
from app.schemas.schemasServiceRequest import CreateSchemasServiceRequest, ResponseSchemasServiceRequest
from app.db.database import get_db
from app.core.dependency import get_current_user,admin_only,worker_only
from app.schemas.schemasServiceRequest import AssignWorkerRequest


service_requests_router = APIRouter(prefix="/service-requests", tags=["Service Requests"])


@service_requests_router.post("/")
def create_service_request_endpoint(service_request: CreateSchemasServiceRequest,db: Session =Depends(get_db)):
    return create_service_request(db, service_request)




@service_requests_router.get("/", response_model=list[ResponseSchemasServiceRequest])
def get_all_service_requests_endpoint(db: Session = Depends(get_db), admin: dict=Depends(admin_only)):
    return get_all_service_requests(db)

@service_requests_router.get("/worker/{worker_id}/requests", response_model=List[ResponseSchemasServiceRequest])
def get_requests_for_worker_endpoint(worker_id: int, db: Session = Depends(get_db), worker: dict = Depends(worker_only)):
    requests = get_requests_for_worker(db, worker_id)
    if not requests:
        raise HTTPException(status_code=404, detail="No requests found for this worker")
    # Convert each ORM object to Pydantic model
    return [ResponseSchemasServiceRequest.from_orm(r) for r in requests]


#admin will assign the request to worker and change the status to assigned
@service_requests_router.put("/", response_model=ResponseSchemasServiceRequest)
def assign_work(assign_worker_request: AssignWorkerRequest, db: Session = Depends(get_db), admin: dict = Depends(admin_only)):
    request = assign_worker(db, assign_worker_request.request_id, assign_worker_request.worker_id)
    return request 

#worker will start the process
@service_requests_router.put("/{service_request_id}/start",  response_model=list[ResponseSchemasServiceRequest])
def start_work_request_endpoint(service_request_id:int,db:Session=Depends(get_db), worker: dict = Depends(worker_only)):
    start_request=start_work_request(db,service_request_id)
    return start_request


#worker will completed the prosess
@service_requests_router.put("/{service_request_id}/complete", response_model=ResponseSchemasServiceRequest)
def complete_service_request_endpoint(service_request_id:int,db:Session=Depends(get_db), worker: dict = Depends(worker_only)):
    request=complete_service_request(db,service_request_id)
    return request

#deleting the service request by status
@service_requests_router.delete("/{service_request_id}")
def delete_service_request_endpoint(service_request_id:int,db:Session=Depends(get_db), admin: dict = Depends(admin_only)):
    delete_service_request(db,service_request_id)
    return {"detail": "Service request deleted successfully"}


@service_requests_router.get("/assigned", response_model=List[ResponseSchemasServiceRequest])
def  get_all_assigned_service_requests_endpoint(db: Session = Depends(get_db), admin: dict = Depends(admin_only)):
    return get_all_assigned_service_requests(db)

@service_requests_router.get("/completed", response_model=List[ResponseSchemasServiceRequest])
def get_all_completed_service_requests_endpoint(db: Session = Depends(get_db), admin: dict = Depends(admin_only)):
    return get_all_completed_service_requests(db)



@service_requests_router.get("/{service_request_id}")
def get_service_request_endpoint_by_ID(service_request_id: int, db: Session = Depends(get_db), admin: dict =Depends(admin_only)):
    return get_service_request(db, service_request_id)





