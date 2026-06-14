"""
BreachLens Backend — FastAPI Application
Connected to MongoDB Atlas for all data persistence.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers import auth, scan, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: verify MongoDB connection, seed demo data. Shutdown: cleanup."""
    # Connect to MongoDB Atlas
    from services.mongodb_service import connect_mongodb, is_connected, close_mongodb

    db = connect_mongodb()
    if db is not None and is_connected():
        print("MongoDB Atlas connection verified successfully")

        # Seed demo users and sample data
        from seed_data import seed_all
        seed_all()
    else:
        print("WARNING: MongoDB Atlas not available. Some features may not work.")

    yield

    # Shutdown — close MongoDB connection
    close_mongodb()
    print("MongoDB connection closed")


app = FastAPI(
    title="BreachLens API",
    description="Autonomous Web-Based Penetration Testing Platform with Executive Risk Intelligence",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(scan.router, prefix="/api", tags=["Scanner"])
app.include_router(reports.router, prefix="/api", tags=["Reports"])


@app.get("/api/health")
def health_check():
    """Health check endpoint — also reports MongoDB connection status."""
    from services.mongodb_service import is_connected, get_collection_names
    mongo_ok = is_connected()
    return {
        "status": "healthy",
        "service": "BreachLens API",
        "mongodb": "connected" if mongo_ok else "disconnected",
        "collections": get_collection_names() if mongo_ok else [],
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
