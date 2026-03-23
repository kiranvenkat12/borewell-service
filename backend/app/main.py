from fastapi import FastAPI
from app.db.database import engine,Base
from app.routes.routerAdminRegister import router
from app.routes.routerServiceRequest import service_requests_router
from app.routes.routerWorkerRegister import worker_register_router
Base.metadata.create_all(bind=engine)


app=FastAPI()

app.include_router(router)
app.include_router(service_requests_router)
app.include_router(worker_register_router)
