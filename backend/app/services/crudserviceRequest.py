from sqlalchemy.orm import Session
from app.models.modelServiceRequest import MOdelServiceRequest
from app.schemas.schemasServiceRequest import CreateSchemasServiceRequest, ResponseSchemasServiceRequest
from datetime import datetime
from fastapi import HTTPException
from app.models.modelWorkerRegister import ModelWorkerRegister

def create_service_request(db:Session, service_request:CreateSchemasServiceRequest):
    db_service_request=MOdelServiceRequest(
 
        name=service_request.name,
        phone_primary=service_request.phone_primary,
        phone_secondary=service_request.phone_secondary,
        
        service_type=service_request.service_type,
        borewell_depth=service_request.borewell_depth if service_request.borewell_depth else None,

        address=service_request.address,
        
        pincode=service_request.pincode,
        description=service_request.description,
        status="Pending",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()

    )
    db.add(db_service_request)
    db.commit()
    db.refresh(db_service_request)
    return db_service_request


def get_service_request(db: Session, service_request_id: int):
    service_request = db.query(MOdelServiceRequest).filter(
        MOdelServiceRequest.id == service_request_id
    ).first()

    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")

    return service_request


def get_all_service_requests(db: Session):
    return db.query(MOdelServiceRequest).all()

#It will assing the workes 

def assign_worker(db:Session, service_request_id: int, worker_id: int):
    service_request = db.query(MOdelServiceRequest).filter(MOdelServiceRequest.id == service_request_id).first()

    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    worker=db.query(ModelWorkerRegister).filter(ModelWorkerRegister.id== worker_id).first()

    if not worker:
        raise HTTPException(status_code=404, detail="worker is not found")
    
    service_request.assigned_worker_id=worker.id
    service_request.status="Assigned"
    service_request.assigned_at = datetime.utcnow()

    db.commit()
    db.refresh(service_request)
    return service_request


#it will start the work

def start_work_request(db:Session, service_request_id:int):
    service_request=db.query( MOdelServiceRequest).filter( MOdelServiceRequest.id==service_request_id).first()

    if not service_request or service_request.status !="Assigned":
        raise HTTPException(status_code=404, detail="cannot start request")
    
    service_request.status="In Progress"
    service_request.started_at=datetime.utcnow()
    db.commit()
    db.refresh(service_request)
    return [service_request]


#it will complete the task 
def complete_service_request(db: Session, service_request_id: int):
    service_request = db.query(MOdelServiceRequest).filter(
        MOdelServiceRequest.id == service_request_id
    ).first()

    if not service_request or service_request.status != "In Progress":
        raise HTTPException(status_code=400, detail="Cannot complete request")
    
    service_request.status = "Completed"
    service_request.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(service_request)
    return service_request


# Get all assigned requests for a worker
def get_requests_for_worker(db: Session, worker_id: int):
    return db.query(MOdelServiceRequest).filter(MOdelServiceRequest.assigned_worker_id == worker_id).all()


#delete the service request by status
def delete_service_request(db: Session, service_request_id: int):
    service_request = db.query(MOdelServiceRequest).filter(
        MOdelServiceRequest.id == service_request_id
    ).first()



    if not service_request:
        raise HTTPException(status_code=404, detail="Service request not found")
    
    if service_request.status in ["In Progress", "Assigned"]:
        raise HTTPException(status_code=400, detail="Cannot delete request that is in progress or assigned")
    
    db.delete(service_request)
    db.commit()
    return {"detail": "Service request deleted successfully"}