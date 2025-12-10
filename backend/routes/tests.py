from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas
import models
from database import get_db

router = APIRouter(prefix="/api/tests", tags=["tests"])


@router.post("/", response_model=schemas.SarcopeniaTestResponse)
def create_test(test: schemas.SarcopeniaTestCreate, db: Session = Depends(get_db)):
    """Yeni sarkopeni testi sonucu ekle"""
    db_test = models.SarcopeniaTest(**test.dict())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test


@router.get("/{test_id}", response_model=schemas.SarcopeniaTestResponse)
def get_test(test_id: int, db: Session = Depends(get_db)):
    """Test sonucu getir"""
    db_test = db.query(models.SarcopeniaTest).filter(
        models.SarcopeniaTest.id == test_id
    ).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Test bulunamadı")
    return db_test


@router.get("/patient/{patient_id}", response_model=List[schemas.SarcopeniaTestResponse])
def get_patient_tests(patient_id: int, db: Session = Depends(get_db)):
    """Hastanın tüm test sonuçlarını getir"""
    tests = db.query(models.SarcopeniaTest).filter(
        models.SarcopeniaTest.patient_id == patient_id
    ).all()
    return tests


@router.put("/{test_id}", response_model=schemas.SarcopeniaTestResponse)
def update_test(
    test_id: int,
    test: schemas.SarcopeniaTestBase,
    db: Session = Depends(get_db)
):
    """Test sonucu güncelle"""
    db_test = db.query(models.SarcopeniaTest).filter(
        models.SarcopeniaTest.id == test_id
    ).first()
    if not db_test:
        raise HTTPException(status_code=404, detail="Test bulunamadı")
    
    update_data = test.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_test, field, value)
    
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test
