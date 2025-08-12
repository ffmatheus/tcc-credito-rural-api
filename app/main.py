from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import safras, blockchain

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(safras.router)
app.include_router(blockchain.router)

@app.get("/")
async def root():
    return {
        "message": "🌾 API Crédito Rural Blockchain",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "🟢 Online"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api-credito-rural"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )