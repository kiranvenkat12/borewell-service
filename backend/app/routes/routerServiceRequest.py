
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.crudserviceRequest import create_service_request,get_service_request,get_all_service_requests
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








