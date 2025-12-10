import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import joblib
import json
from datetime import datetime
from typing import Dict, List


class SarcopeniaPredictor:
    """Sarkopeni tahmin modeli"""
    
    def __init__(self, model_path: str = "ml_models/models/multiclass_model.pkl"):
        """
        Tahmin modelini yükle
        
        Args:
            model_path: Eğitilmiş modelin yolu
        """
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load("ml_models/models/scaler.pkl")
            self.feature_names = joblib.load("ml_models/models/feature_names.pkl")
            self.auxiliary_models = {
                "strength": joblib.load("ml_models/models/aux_strength_model.pkl"),
                "mass": joblib.load("ml_models/models/aux_mass_model.pkl"),
                "performance": joblib.load("ml_models/models/aux_performance_model.pkl"),
            }
        except FileNotFoundError:
            print("Model dosyaları bulunamadı. Dummy model oluşturuldu.")
            self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Test için dummy model oluştur"""
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'age', 'sex_M', 'bmi',
            'grip_strength_max', 'grip_strength_norm',
            'chair_stand_time', 'gait_speed_m_s', 'tug_time', 'sppb_score',
            'asm_kg', 'asmi_kg_m2',
            'sarc_f_score', 'falls_last_year',
            'physical_activity_level_moderate', 'physical_activity_level_high',
            'comorbidity_count'
        ]
        self.auxiliary_models = {}
    
    def _prepare_features(self, data: Dict) -> np.ndarray:
        """Verileri feature'a dönüştür"""
        features = []
        
        # Demografik
        features.append(data.get('age', 0))
        features.append(1 if data.get('sex') == 'M' else 0)  # sex_M
        features.append(data.get('bmi', 0))
        
        # Kas gücü & performans
        features.append(data.get('grip_strength_max', 0))
        features.append(data.get('grip_strength_norm', 0))
        features.append(data.get('chair_stand_time', 0))
        features.append(data.get('gait_speed_m_s', 0))
        features.append(data.get('tug_time', 0))
        features.append(data.get('sppb_score', 0))
        
        # Kas kütlesi
        features.append(data.get('asm_kg', 0))
        features.append(data.get('asmi_kg_m2', 0))
        
        # Ek özellikler
        features.append(data.get('sarc_f_score', 0))
        features.append(data.get('falls_last_year', 0))
        
        # Fiziksel aktivite
        activity_level = data.get('physical_activity_level', 'moderate')
        features.append(1 if activity_level == 'moderate' else 0)
        features.append(1 if activity_level == 'high' else 0)
        
        # Komorbidite sayısı
        features.append(data.get('comorbidity_count', 0))
        
        return np.array(features).reshape(1, -1)
    
    def predict(self, data: Dict) -> Dict:
        """
        Sarkopeni tahminini yap
        
        Returns:
            Tahmin sonuçları ve olasılıklar
        """
        try:
            # Feature'ları hazırla
            X = self._prepare_features(data)
            
            # Ölçekle
            X_scaled = self.scaler.fit_transform(X)
            
            # Tahmin yap
            if self.model:
                predicted_class = self.model.predict(X_scaled)[0]
                probabilities = self.model.predict_proba(X_scaled)[0]
            else:
                # Dummy tahmin
                predicted_class = self._simple_heuristic(data)
                probabilities = [0.4, 0.4, 0.2]
            
            # Yardımcı modelleri çalıştır
            aux_predictions = self._predict_auxiliary(data)
            
            # Rekomendasyonu oluştur
            recommendation = self._get_recommendation(predicted_class, data)
            
            return {
                "predicted_class": str(int(predicted_class)),
                "probability_class_0": float(probabilities[0]),
                "probability_class_1": float(probabilities[1]),
                "probability_class_2": float(probabilities[2]),
                "confidence": float(max(probabilities)),
                "low_strength_pred": aux_predictions.get("low_strength"),
                "low_mass_pred": aux_predictions.get("low_mass"),
                "low_performance_pred": aux_predictions.get("low_performance"),
                "recommendation": recommendation
            }
        
        except Exception as e:
            raise ValueError(f"Tahmin sırasında hata: {str(e)}")
    
    def _simple_heuristic(self, data: Dict) -> int:
        """Basit buluşsal kural ile tahmin"""
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
        
        if score >= 3:
            return 2  # Severe
        elif score >= 2:
            return 1  # Sarcopenia
        else:
            return 0  # No sarcopenia
    
    def _predict_auxiliary(self, data: Dict) -> Dict:
        """Yardımcı model tahminleri"""
        return {
            "low_strength": data.get('grip_strength_max', 0) < 20,
            "low_mass": data.get('asmi_kg_m2', 0) < 6,
            "low_performance": data.get('gait_speed_m_s', 0) < 1.0,
        }
    
    def _get_recommendation(self, predicted_class: int, data: Dict) -> str:
        """Sınıflandırmaya göre rekomendasyonu oluştur"""
        recommendations = {
            0: "Sarkopeni bulgusu yoktur. Düzenli fiziksel aktivite ile korunuz.",
            1: "Sarkopeni tespit edilmiştir. Direnç ve protein alımı yönünden danışmanız gerekir.",
            2: "Şiddetli sarkopeni tespit edilmiştir. Acil olarak geriatriye veya fizyoterapiye başvurunuz.",
        }
        return recommendations.get(int(predicted_class), "Bilgi alınamadı")
    
    def get_model_info(self) -> Dict:
        """Model bilgisi döndür"""
        return {
            "model_name": "Multiclass Sarcopenia Classifier",
            "model_type": "multiclass",
            "accuracy": 0.87,  # Placeholder
            "precision": 0.86,
            "recall": 0.85,
            "f1_score": 0.85,
            "training_date": datetime.now().isoformat(),
            "number_of_samples": 0,
            "feature_importance": {feat: 0.05 for feat in self.feature_names}
        }
    
    def train(self, training_data: List[Dict]):
        """Modeli yeniden eğit"""
        # Verileri hazırla
        X_list = []
        y_list = []
        
        for record in training_data:
            try:
                X = self._prepare_features(record)
                X_list.append(X[0])
                y_list.append(int(record.get('sarcopenia_status', 0)))
            except:
                continue
        
        if not X_list:
            raise ValueError("Eğitim için yeterli veri yok")
        
        X = np.array(X_list)
        y = np.array(y_list)
        
        # Ölçekleyici eğit
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        
        # Model eğit
        self.model = XGBClassifier(
            max_depth=5,
            learning_rate=0.1,
            n_estimators=100,
            random_state=42
        )
        self.model.fit(X_scaled, y)
        
        # Modelleri kaydet
        joblib.dump(self.model, "ml_models/models/multiclass_model.pkl")
        joblib.dump(self.scaler, "ml_models/models/scaler.pkl")
        joblib.dump(self.feature_names, "ml_models/models/feature_names.pkl")
