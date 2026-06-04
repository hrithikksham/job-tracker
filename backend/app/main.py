from fastapi import FastAPI

from app.database.mongodb import connect_to_mongo
from app.api.resume import router as resume_router
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router


app = FastAPI(
    title="Job Application Tracker API",
    description="API for tracking job applications, including companies, job listings, and application statuses.",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    await connect_to_mongo()


@app.get("/")
async def root():
    return {
        "success": True,
        "message": "Welcome to the Job Application Tracker API!"
    }


app.include_router(auth_router)
app.include_router(resume_router)
app.include_router(profile_router)