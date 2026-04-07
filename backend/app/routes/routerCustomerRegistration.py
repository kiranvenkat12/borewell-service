from app.schemas.schemasCustomersRegistration import CreateCustomerRegister, CustomerResponse, CustomerLogin
from app.services.crudCustomersRegistration import create_customer_registration, customer_login, get_all_customers, get_customer_by_phonenumber
from fastapi import APIRouter, Depends, HTTPException
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.core.dependency import admin_only, customer_only



customer_register_rooter = APIRouter(prefix="/customer-registrations", tags=["Customer Registrations"])



@customer_register_rooter.post("/register")
def register_customer(customer_registration: CreateCustomerRegister, db: Session = Depends(get_db)):
    return create_customer_registration(db, customer_registration)


@customer_register_rooter.post("/login")
def login_customer(credentials: CustomerLogin, db: Session = Depends(get_db)):
    return customer_login(db, credentials.phoneNumber, credentials.password)

@customer_register_rooter.get("/customers", response_model=list[CustomerResponse])  
def get_all_customers_endpoint(db: Session = Depends(get_db), customer: dict = Depends(customer_only)):
    return get_all_customers(db)

@customer_register_rooter.get("/customer-registrations/{phoneNumber}", response_model=CustomerResponse)
def get_customer_by_phonenumber_endpoint(phoneNumber: str, db: Session = Depends(get_db) , customer: dict = Depends(customer_only)):
    customer = get_customer_by_phonenumber(db, phoneNumber)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer







