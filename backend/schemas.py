from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, List
from enum import Enum


class SarcopeniaStatusEnum(str, Enum):
    NO_SARCOPENIA = "0"
    SARCOPENIA = "1"
    SEVERE_SARCOPENIA = "2"


# ==================== Patient Schemas ====================

class PatientBase(BaseModel):
    name: str
    sex: str  # M/F
    birth_date: datetime
    height_cm: float
    weight_kg: float
    bmi: float


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None


class PatientResponse(PatientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Clinical Data Schemas ====================

class ClinicalDataBase(BaseModel):
    comorbidities: Dict[str, bool]  # {ht: true, dm: false, ...}
    medication_count: int = 0
    falls_last_year: int = 0
    physical_activity_level: str  # low/moderate/high
    sarc_f_score: Optional[float] = None
    adls_score: Optional[float] = None
    iadls_score: Optional[float] = None


class ClinicalDataCreate(ClinicalDataBase):
    patient_id: int


class ClinicalDataResponse(ClinicalDataBase):
    id: int
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Sarcopenia Test Schemas ====================

class SarcopeniaTestBase(BaseModel):
    # Kas gücü
    grip_strength_right: Optional[float] = None
    grip_strength_left: Optional[float] = None
    chair_stand_time: Optional[float] = None  # seconds
    
    # Kas kütlesi
    asm_kg: Optional[float] = None
    asmi_kg_m2: Optional[float] = None
    
    # Fiziksel performans
    gait_speed_m_s: Optional[float] = None
    tug_time: Optional[float] = None
    sppb_score: Optional[float] = None
    
    # Ek ölçümler
    calf_circumference: Optional[float] = None
    muscle_thickness: Optional[float] = None


class SarcopeniaTestCreate(SarcopeniaTestBase):
    patient_id: int


class SarcopeniaTestResponse(SarcopeniaTestBase):
    id: int
    patient_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Label Schemas ====================

class LabelBase(BaseModel):
    sarcopenia_status: SarcopeniaStatusEnum
    low_muscle_strength: Optional[bool] = None
    low_muscle_mass: Optional[bool] = None
    low_physical_performance: Optional[bool] = None
    labeled_by: str


class LabelCreate(LabelBase):
    patient_id: int
    test_id: Optional[int] = None


class LabelResponse(LabelBase):
    id: int
    patient_id: int
    test_id: Optional[int]
    labeled_at: datetime

    class Config:
        from_attributes = True


# ==================== Prediction Schemas ====================

class PredictionRequest(BaseModel):
    # Demografik
    age: float
    sex: str
    bmi: float
    
    # Kas gücü & performans
    grip_strength_max: float
    grip_strength_norm: Optional[float] = None
    chair_stand_time: Optional[float] = None
    gait_speed_m_s: float
    tug_time: Optional[float] = None
    sppb_score: float
    
    # Kas kütlesi
    asm_kg: float
    asmi_kg_m2: float
    
    # Ek özellikler
    sarc_f_score: Optional[float] = None
    falls_last_year: int = 0
    physical_activity_level: str = "moderate"
    comorbidity_count: int = 0


class PredictionResponse(BaseModel):
    predicted_class: str  # "0", "1", "2"
    probability_class_0: float
    probability_class_1: float
    probability_class_2: float
    confidence: float
    low_strength_pred: Optional[bool] = None
    low_mass_pred: Optional[bool] = None
    low_performance_pred: Optional[bool] = None
    recommendation: str


class PredictionHistoryResponse(BaseModel):
    id: int
    patient_id: int
    test_id: int
    model_name: str
    predicted_class: str
    probability_class_0: float
    probability_class_1: float
    probability_class_2: float
    predicted_at: datetime

    class Config:
        from_attributes = True


# ==================== Model Info Schemas ====================

class ModelInfo(BaseModel):
    model_name: str
    model_type: str  # "binary" or "multiclass"
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    training_date: datetime
    number_of_samples: int
    feature_importance: Dict[str, float]


class FeatureImportanceResponse(BaseModel):
    feature_name: str
    importance: float


# ==================== Composite Schemas ====================

class PatientWithData(PatientResponse):
    clinical_data: Optional[List[ClinicalDataResponse]] = None
    sarcopenia_tests: Optional[List[SarcopeniaTestResponse]] = None
    labels: Optional[List[LabelResponse]] = None
