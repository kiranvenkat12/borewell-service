from sqlalchemy.orm import Session
from app.models.modelServiceRequest import MOdelServiceRequest
from app.schemas.schemasServiceRequest import CreateSchemasServiceRequest, ResponseSchemasServiceRequest
from datetime import datetime
from fastapi import HTTPException


def create_service_request(db:Session, service_request:CreateSchemasServiceRequest):
    db_service_request=MOdelServiceRequest(
        name=service_request.name,
        phone_primary=service_request.phone_primary,
        phone_secondary=service_request.phone_secondary,
        email=service_request.email,
        service_type=service_request.service_type,
        borewell_depth=service_request.borewell_depth,
        address=service_request.address,
        area=service_request.area,
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