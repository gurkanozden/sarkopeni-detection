from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class Patient(Base):
    """Hasta bilgileri"""
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sex = Column(String)  # M/F
    birth_date = Column(DateTime)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    bmi = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    clinical_data = relationship("ClinicalData", back_populates="patient")
    sarcopenia_tests = relationship("SarcopeniaTest", back_populates="patient")
    labels = relationship("Label", back_populates="patient")


class ClinicalData(Base):
    """Klinik veriler"""
    __tablename__ = "clinical_data"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), index=True)
    comorbidities = Column(JSON)  # {ht: true, dm: false, ...}
    medication_count = Column(Integer, default=0)
    falls_last_year = Column(Integer, default=0)
    physical_activity_level = Column(String)  # low/moderate/high
    sarc_f_score = Column(Float, nullable=True)
    adls_score = Column(Float, nullable=True)
    iadls_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="clinical_data")


class SarcopeniaTest(Base):
    """Sarkopeni test sonuçları"""
    __tablename__ = "sarcopenia_tests"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), index=True)
    
    # Kas gücü (Muscle Strength)
    grip_strength_right = Column(Float, nullable=True)
    grip_strength_left = Column(Float, nullable=True)
    chair_stand_time = Column(Float, nullable=True)  # seconds
    
    # Kas kütlesi (Muscle Mass)
    asm_kg = Column(Float, nullable=True)  # Appendicular skeletal mass
    asmi_kg_m2 = Column(Float, nullable=True)  # ASM Index
    
    # Fiziksel performans (Physical Performance)
    gait_speed_m_s = Column(Float, nullable=True)  # 4m walk test
    tug_time = Column(Float, nullable=True)  # Timed Up and Go (seconds)
    sppb_score = Column(Float, nullable=True)  # Short Physical Performance Battery
    
    # Ek ölçümler
    calf_circumference = Column(Float, nullable=True)
    muscle_thickness = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="sarcopenia_tests")
    labels = relationship("Label", back_populates="test")


class SarcopeniaStatus(str, enum.Enum):
    """Sarkopeni durum enum"""
    NO_SARCOPENIA = "0"  # Normal
    SARCOPENIA = "1"     # Sarkopeni
    SEVERE_SARCOPENIA = "2"  # Şiddetli Sarkopeni


class Label(Base):
    """Eğitim veri label'ları"""
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), index=True)
    test_id = Column(Integer, ForeignKey("sarcopenia_tests.id"), nullable=True, index=True)
    
    sarcopenia_status = Column(Enum(SarcopeniaStatus))  # 0: yok, 1: var, 2: şiddetli
    low_muscle_strength = Column(Boolean, nullable=True)
    low_muscle_mass = Column(Boolean, nullable=True)
    low_physical_performance = Column(Boolean, nullable=True)
    
    labeled_by = Column(String)  # Uzman adı
    labeled_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="labels")
    test = relationship("SarcopeniaTest", back_populates="labels")


class PredictionHistory(Base):
    """Model tahminleri geçmişi"""
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), index=True)
    test_id = Column(Integer, ForeignKey("sarcopenia_tests.id"), index=True)
    
    model_name = Column(String)
    predicted_class = Column(String)  # 0, 1, 2
    probability_class_0 = Column(Float)
    probability_class_1 = Column(Float)
    probability_class_2 = Column(Float)
    
    low_strength_pred = Column(Boolean, nullable=True)
    low_mass_pred = Column(Boolean, nullable=True)
    low_performance_pred = Column(Boolean, nullable=True)
    
    predicted_at = Column(DateTime, default=datetime.utcnow)
