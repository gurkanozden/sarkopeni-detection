from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import schemas
import models
from database import get_db
from ml_service import SarcopeniaPredictor
import json

router = APIRouter(prefix="/api/predict", tags=["predictions"])

# ML modeli yükle
predictor = SarcopeniaPredictor()


@router.post("/", response_model=schemas.PredictionResponse)
def predict_sarcopenia(
    request: schemas.PredictionRequest,
    patient_id: int = None,
    test_id: int = None,
    db: Session = Depends(get_db)
):
    """Sarkopeni tahminini yap"""
    try:
        # Tahmin yap
        prediction = predictor.predict(request.dict())
        
        # Veritabanına kaydet (eğer patient_id varsa)
        if patient_id and test_id:
            history = models.PredictionHistory(
                patient_id=patient_id,
                test_id=test_id,
                model_name="multiclass_xgboost",
                predicted_class=prediction["predicted_class"],
                probability_class_0=prediction["probability_class_0"],
                probability_class_1=prediction["probability_class_1"],
                probability_class_2=prediction["probability_class_2"],
                low_strength_pred=prediction.get("low_strength_pred"),
                low_mass_pred=prediction.get("low_mass_pred"),
                low_performance_pred=prediction.get("low_performance_pred"),
            )
            db.add(history)
            db.commit()
        
        return prediction
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{patient_id}", response_model=list)
def get_prediction_history(patient_id: int, db: Session = Depends(get_db)):
    """Hastanın tahmin geçmişini getir"""
    history = db.query(models.PredictionHistory).filter(
        models.PredictionHistory.patient_id == patient_id
    ).all()
    return history


@router.get("/info")
def get_model_info():
    """Model bilgisi getir"""
    return predictor.get_model_info()


@router.post("/retrain")
def retrain_model(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Modeli yeniden eğit"""
    try:
        # Dosya oku
        contents = file.file.read()
        training_data = json.loads(contents)
        
        # Modeli eğit
        predictor.train(training_data)
        
        return {"message": "Model başarıyla yeniden eğitildi"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
