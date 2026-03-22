from fastapi import APIRouter, Depends
from typing import List  # Added for list response model
from sqlalchemy.orm import Session
from app.db.database import get_db  # Removed unused SessionLocal
from app.services.register import create_user, get_user
from app.schemas.schemasregister import CreateRegistration, RegisterResponse

router = APIRouter(prefix="/user", tags=["Users"])

@router.post("/", response_model=RegisterResponse)  # Fixed: response -> response_model
def create_user_endpoint(user: CreateRegistration, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/", response_model=List[RegisterResponse])  # Fixed: response -> response_model, added List for multiple users
def get_users(db: Session = Depends(get_db)):  # Renamed function for clarity (returns list)
    return get_user(db)