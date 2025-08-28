"""Aplicação FastAPI para gerenciamento de emails."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.emails import router as emails_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API para recebimento e gerenciamento de emails",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    emails_router,
    prefix=f"{settings.api_v1_str}/emails",
    tags=["emails"]
)


@app.get("/health")
def health_check():
    """Endpoint de liveness simples para verificação de saúde do serviço."""
    return {"status": "ok"}
