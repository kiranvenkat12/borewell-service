from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.db.database import engine, Base
from app.routes.routerAdminRegister import router as admin_router
from app.routes.routerServiceRequest import service_requests_router
from app.routes.routerWorkerRegister import worker_register_router
from app.routes.routerCustomerRegistration import customer_register_rooter

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# ----------------------------
# CORS CONFIGURATION (FIXED)
# ----------------------------
origins = [
    "https://borewellservice.in",
    "https://www.borewellservice.in",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# HANDLE PREFLIGHT (IMPORTANT FOR RENDER)
# ----------------------------
@app.options("/{rest_of_path:path}")
async def preflight_handler():
    return Response()

# ----------------------------
# ROUTERS
# ----------------------------
app.include_router(admin_router)
app.include_router(service_requests_router)
app.include_router(worker_register_router)
app.include_router(customer_register_rooter)

# ----------------------------
# HEALTH CHECK
# ----------------------------
@app.get("/")
async def root():
    return {"status": "Backend running!"}