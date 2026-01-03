from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.database import init_db
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
init_db()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

# CORS configuration with environment-based origins
# In development: Allow localhost origins
# In production: Only allow specific domain
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS", 
    "http://localhost:5173,http://localhost:3000"
).split(",")

print(f"🔒 CORS allowed origins: {ALLOWED_ORIGINS}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Restricted origins from environment
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only allow necessary methods
    allow_headers=["*"],
)

# include router
app.include_router(router)