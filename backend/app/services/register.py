from sqlalchemy.orm import Session
from app.models.register_model import Register
from app.schemas.schemasregister import CreateRegistration


def create_user(db:Session, user:CreateRegistration):
    db_user=Register(
        name=user.name,
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db:Session):
    return db.query(Register).all()


