from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Enterprise IT Asset & Access Management Portal")

# Allow CORS for local frontend development
origins = [
    os.getenv("CORS_ORIGIN", "http://localhost:5173"),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

from app.api.auth import router as auth_router
from app.api.users import router as users_router

app.include_router(auth_router)
app.include_router(users_router)
