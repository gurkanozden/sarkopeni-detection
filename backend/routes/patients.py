from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
import models
from database import get_db

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.post("/", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    """Yeni hasta ekle"""
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.get("/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Hasta bilgisi getir"""
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    return db_patient


@router.get("/", response_model=List[schemas.PatientResponse])
def list_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Tüm hastaları listele"""
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients


@router.put("/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(
    patient_id: int, 
    patient: schemas.PatientUpdate, 
    db: Session = Depends(get_db)
):
    """Hasta bilgisi güncelle"""
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    
    update_data = patient.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_patient, field, value)
    
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Hasta sil"""
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Hasta bulunamadı")
    
    db.delete(db_patient)
    db.commit()
    return {"message": "Hasta silindi"}
