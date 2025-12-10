from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import models
from database import engine
from routes import patients, tests, clinical, predictions

# Veritabanı tablolarını oluştur
models.Base.metadata.create_all(bind=engine)

# Lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Uygulama başlatılıyor...")
    yield
    # Shutdown
    print("Uygulama kapatılıyor...")


# FastAPI uygulaması
app = FastAPI(
    title="Sarkopeni Tespiti API",
    description="EWGSOP2 kriterlerine dayalı sarkopeni tahmin sistemi",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotaları ekle
app.include_router(patients.router)
app.include_router(tests.router)
app.include_router(clinical.router)
app.include_router(predictions.router)


@app.get("/")
def read_root():
    """API'nin temel endpoint'i"""
    return {
        "message": "Sarkopeni Tespiti API'ye hoş geldiniz",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """Sistem sağlığı kontrolü"""
    return {"status": "healthy", "service": "sarcopenia-detection"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
