from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from app.db.database import engine, Base
from app.routes.routerAdminRegister import router
from app.routes.routerServiceRequest import service_requests_router
from app.routes.routerWorkerRegister import worker_register_router

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create app
app = FastAPI()

# ✅ FIX 1: OPTIONS handler AFTER app creation
@app.options("/{full_path:path}")
async def preflight_handler():
    return Response(status_code=200)

# ✅ FIX 2: Correct origins (NO trailing slash)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://borewell-services.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)
app.include_router(service_requests_router)
app.include_router(worker_register_router)