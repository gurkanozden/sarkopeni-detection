from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
import models
from database import get_db

router = APIRouter(prefix="/api/clinical", tags=["clinical"])


@router.post("/", response_model=schemas.ClinicalDataResponse)
def create_clinical_data(
    data: schemas.ClinicalDataCreate,
    db: Session = Depends(get_db)
):
    """Yeni klinik veri ekle"""
    # Hastanın varlığını kontrol et
    patient = db.query(models.Patient).filter(
        models.Patient.id == data.patient_id
    ).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    
    db_data = models.ClinicalData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


@router.get("/{clinical_id}", response_model=schemas.ClinicalDataResponse)
def get_clinical_data(clinical_id: int, db: Session = Depends(get_db)):
    """Klinik veri getir"""
    db_data = db.query(models.ClinicalData).filter(
        models.ClinicalData.id == clinical_id
    ).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Klinik veri bulunamadı")
    return db_data


@router.get("/patient/{patient_id}", response_model=List[schemas.ClinicalDataResponse])
def get_patient_clinical_data(patient_id: int, db: Session = Depends(get_db)):
    """Hastanın tüm klinik verilerini getir"""
    data_list = db.query(models.ClinicalData).filter(
        models.ClinicalData.patient_id == patient_id
    ).all()
    return data_list


@router.put("/{clinical_id}", response_model=schemas.ClinicalDataResponse)
def update_clinical_data(
    clinical_id: int,
    data: schemas.ClinicalDataBase,
    db: Session = Depends(get_db)
):
    """Klinik veri güncelle"""
    db_data = db.query(models.ClinicalData).filter(
        models.ClinicalData.id == clinical_id
    ).first()
    if not db_data:
        raise HTTPException(status_code=404, detail="Klinik veri bulunamadı")
    
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_data, field, value)
    
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
