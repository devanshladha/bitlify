from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from .database import engine, Base
from .routers import auth, urls
from . import mongo, task
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- 1. App Initialization ---
app = FastAPI(title="URL Shortener API", version="1.0.0")

# --- Initilize Scheduler 
scheduler = AsyncIOScheduler()

# --- 2. Database Startup (Async Table Creation) ---
@app.on_event("startup")
async def startup():
    print("-"*10, "Application Starting Now", "-"*10)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await mongo.connect_to_mongo()

    scheduler.add_job(task.flush_analytics_to_mongo, 'interval', minutes=1)
    scheduler.start()
    print("Analytics Scheduler Started")

@app.on_event("shutdown")
async def shutdown():
    scheduler.shutdown()
    await mongo.close_mongo_connection()

app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SECRET_KEY", "super-secret-random-string")
)

# --- 3. CORS Configuration (Critical for React) ---
origins = [
    "http://localhost:3000",       # FRONTEND DOMAIN
    "https://localhost:8000"       # BACKEND DOMAIN
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# --- 4. Include Routers ---
app.include_router(auth.router)
app.include_router(urls.router)

# --- 5. Health Check Endpoint ---
@app.get("/")
def read_root():
    return {"status": "active", "message": "URL Shortener API is running"}