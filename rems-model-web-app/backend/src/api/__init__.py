from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.schedules import router as ScheduleRouter
import os

app = FastAPI(
    title = "REMS Scheduling API",
    description = "API for Rice EMS Scheduling Optimization",
    version = "1.0.0"
)

# allowed origins for CORS -- communication between front end and this backend server
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
allow_origins = [o.strip() for o in frontend_origin.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins = allow_origins,
    allow_credentials = True,
    allow_methods = ["*"], # allow all http methods
    allow_headers = ["*"] # allow all http headers
)

app.include_router(ScheduleRouter, prefix = "/api")

@app.get("/", tags = ["Health"])
async def root():
    """Root endpoint"""
    return {"status": "online", "message": "REMS Scheduling app is live and running!"}


