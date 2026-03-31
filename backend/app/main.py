from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse

from app.db.database import engine, Base
from app.routes.routerAdminRegister import router as admin_router
from app.routes.routerServiceRequest import service_requests_router
from app.routes.routerWorkerRegister import worker_register_router

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create app
app = FastAPI()

# ✅ 1️⃣ CORS origins (include all frontend domains, no trailing slashes)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://borewell-services.vercel.app",
    "https://borewell-services-6p94c9qxq-kiranvenkats-projects-97f074f7.vercel.app",  # preview Vercel
]

# ✅ 2️⃣ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 3️⃣ Global OPTIONS preflight handler
@app.options("/{full_path:path}")
async def preflight_handler(request: Request):
    # Respond to OPTIONS requests with proper CORS headers
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": request.headers.get(
                "access-control-request-headers", "*"
            ),
            "Access-Control-Allow-Credentials": "true",
        },
    )

# ✅ 4️⃣ Include routers
app.include_router(admin_router)
app.include_router(service_requests_router)
app.include_router(worker_register_router)