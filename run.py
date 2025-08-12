import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    print("🚀 Iniciando API Crédito Rural Blockchain...")
    print(f"📍 URL: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 Documentação: http://{settings.HOST}:{settings.PORT}/docs")
    print("─" * 50)
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )