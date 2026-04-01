from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
from app.routes.routerAdminRegister import router as admin_router
from app.routes.routerServiceRequest import service_requests_router
from app.routes.routerWorkerRegister import worker_register_router

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# ----------------------------
# 1️⃣ CORS configuration
# ----------------------------
origins = [
    "https://borewell-services.vercel.app",  # your frontend
    "http://localhost:3000",                 # optional for local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # allow these domains
    allow_credentials=True,
    allow_methods=["*"],     # allow GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],     # allow Content-Type, Authorization, etc.
)

# ----------------------------
# 2️⃣ Include routers
# ----------------------------
app.include_router(admin_router)
app.include_router(service_requests_router, prefix="/service-requests")
app.include_router(worker_register_router)

# ----------------------------
# 3️⃣ Optional root for health check
# ----------------------------
@app.get("/")
async def root():
    return {"status": "Backend running!"}