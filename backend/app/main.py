from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.database import engine
from app.models.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FlowForge", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"message": "FlowForge API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}