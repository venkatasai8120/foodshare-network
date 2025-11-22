# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, donations

app = FastAPI(
    title="FoodShare Network API",
    description="REST API for Food Donation & Redistribution system (FoodShare).",
    version="1.0.0",
)

# CORS – allow your Codespaces frontend to call the API
origins = ["*"]  # for demo; restrict later if you want

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(donations.router)


@app.get("/")
def root():
    return {"message": "FoodShare API is running"}
