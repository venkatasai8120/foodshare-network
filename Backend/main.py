# Backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Backend.database import Base, engine
from Backend.routers import auth, donations

# Create database tables (ONLY RUN ONCE if needed)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FoodShare Network API",
    description="REST API for Food Donation & Redistribution",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(donations.router, prefix="/donations", tags=["Donations"])

@app.get("/")
def root():
    return {"message": "FoodShare API is running"}
