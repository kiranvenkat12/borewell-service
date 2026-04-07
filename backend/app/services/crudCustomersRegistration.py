import token

from sqlalchemy.orm import Session
from app.models.modelCustomerRegistration import ModelCustomerRegistration
from app.schemas.schemasCustomersRegistration import CreateCustomerRegister
from app.core.security import hash_password, verify_password
from app.core.dependency import customer_only
from fastapi import HTTPException

from app.core.auth import create_access_token




def create_customer_registration(db:Session, customer_registration:CreateCustomerRegister):
    if db.query(ModelCustomerRegistration).filter(ModelCustomerRegistration.phoneNumber == customer_registration.phoneNumber).first():
        raise HTTPException(status_code=400, detail="Phone number already exists")
    
    hashed_password = hash_password(customer_registration.password)

    db_customer_registration=ModelCustomerRegistration(
        name=customer_registration.name,
        phoneNumber=customer_registration.phoneNumber,
        password=hashed_password
    )
    db.add(db_customer_registration)
    db.commit()
    db.refresh(db_customer_registration)
    return db_customer_registration

def customer_login(db:Session, phoneNumber:str, password:str):
    user = db.query(ModelCustomerRegistration).filter(ModelCustomerRegistration.phoneNumber == phoneNumber).first()
    if not user:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    token = create_access_token(user_id=user.phoneNumber, role="customer")
    return {"access_token": token, "token_type": "bearer", "customer_id": user.id, "customer_name": user.name}
    
    
    return user

def get_all_customers(db: Session):
    customers=db.query(ModelCustomerRegistration).all()
    print(f"Queried all customers, Found: {customers}")
    return customers

def get_customer_by_phonenumber(db: Session, phoneNumber: str):
    user = db.query(ModelCustomerRegistration).filter(ModelCustomerRegistration.phoneNumber == phoneNumber).first()
    print(f"Queried phone number: {phoneNumber}, Found: {user}")
    return user




