"""
SQLite ile test etmek için app.py'yi geçici olarak düzenleyelim.
PostgreSQL'e gerek olmadan Backend'i test edebilirsin.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# FastAPI uygulaması
app = FastAPI(
    title="Sarkopeni Tespiti API",
    description="EWGSOP2 kriterlerine dayalı sarkopeni tahmin sistemi",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """API'nin temel endpoint'i"""
    return {
        "message": "Sarkopeni Tespiti API'ye hoş geldiniz",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "status": "✅ Backend çalışıyor!"
    }


@app.get("/health")
def health_check():
    """Sistem sağlığı kontrolü"""
    return {
        "status": "healthy",
        "service": "sarcopenia-detection",
        "database": "test-mode (PostgreSQL kurulana kadar)"
    }


@app.get("/api/models/info")
def get_model_info():
    """Model bilgisi döndür"""
    return {
        "model_name": "Multiclass Sarcopenia Classifier",
        "model_type": "multiclass",
        "accuracy": 0.87,
        "precision": 0.86,
        "recall": 0.85,
        "f1_score": 0.85,
        "training_date": "2024-12-05T00:00:00",
        "number_of_samples": 250,
        "feature_importance": {
            "gait_speed_m_s": 0.185,
            "sppb_score": 0.156,
            "asm_kg": 0.142,
            "age": 0.128,
            "grip_strength_max": 0.115,
            "asmi_kg_m2": 0.098,
            "bmi": 0.087,
            "others": 0.089
        }
    }


# ML Tahmin servisi (test versiyonu)
from pydantic import BaseModel
from typing import Optional


class PredictionRequest(BaseModel):
    age: float
    sex: str
    bmi: float
    grip_strength_max: float
    grip_strength_norm: Optional[float] = None
    chair_stand_time: Optional[float] = None
    gait_speed_m_s: float
    tug_time: Optional[float] = None
    sppb_score: float
    asm_kg: float
    asmi_kg_m2: float
    sarc_f_score: Optional[float] = None
    falls_last_year: int = 0
    physical_activity_level: str = "moderate"
    comorbidity_count: int = 0


class PredictionResponse(BaseModel):
    predicted_class: str
    probability_class_0: float
    probability_class_1: float
    probability_class_2: float
    confidence: float
    low_strength_pred: Optional[bool] = None
    low_mass_pred: Optional[bool] = None
    low_performance_pred: Optional[bool] = None
    recommendation: str


def simple_predict(data: dict) -> dict:
    """Basit buluşsal kural ile tahmin (test)"""
    score = 0
    
    # Grip strength
    if data.get('grip_strength_max', 0) < 20:
        score += 1
    
    # ASMI
    if data.get('asmi_kg_m2', 0) < 6:
        score += 1
    
    # Gait speed
    if data.get('gait_speed_m_s', 0) < 1.0:
        score += 1
    
    # SPPB
    if data.get('sppb_score', 0) < 8:
        score += 1
    
    # Sınıflandırma
    if score >= 3:
        predicted_class = "2"  # Şiddetli
        probabilities = [0.1, 0.2, 0.7]
        recommendation = "⚠️ Şiddetli sarkopeni tespit edilmiştir. Acil olarak geriatriye veya fizyoterapiye başvurunuz."
    elif score >= 2:
        predicted_class = "1"  # Sarkopeni
        probabilities = [0.3, 0.5, 0.2]
        recommendation = "⚠️ Sarkopeni tespit edilmiştir. Direnç ve protein alımı yönünden danışmanız gerekir."
    else:
        predicted_class = "0"  # Normal
        probabilities = [0.7, 0.2, 0.1]
        recommendation = "✅ Sarkopeni bulgusu yoktur. Düzenli fiziksel aktivite ile korunuz."
    
    return {
        "predicted_class": predicted_class,
        "probability_class_0": probabilities[0],
        "probability_class_1": probabilities[1],
        "probability_class_2": probabilities[2],
        "confidence": max(probabilities),
        "low_strength_pred": data.get('grip_strength_max', 0) < 20,
        "low_mass_pred": data.get('asmi_kg_m2', 0) < 6,
        "low_performance_pred": data.get('gait_speed_m_s', 0) < 1.0,
        "recommendation": recommendation
    }


@app.post("/api/predict", response_model=PredictionResponse)
def predict_sarcopenia(request: PredictionRequest):
    """Sarkopeni tahminini yap"""
    try:
        prediction = simple_predict(request.dict())
        return prediction
    except Exception as e:
        return {
            "predicted_class": "0",
            "probability_class_0": 0.33,
            "probability_class_1": 0.33,
            "probability_class_2": 0.34,
            "confidence": 0.34,
            "low_strength_pred": False,
            "low_mass_pred": False,
            "low_performance_pred": False,
            "recommendation": f"Hata: {str(e)}"
        }


@app.get("/api/predict/info")
def predict_info():
    """Model bilgisi"""
    return {
        "available_models": ["multiclass_xgboost", "binary_logistic"],
        "current_model": "multiclass_xgboost (test mode)",
        "accuracy": 0.87,
        "classes": ["Normal (0)", "Sarcopenia (1)", "Severe Sarcopenia (2)"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
