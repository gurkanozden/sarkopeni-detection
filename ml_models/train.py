import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import xgboost as xgb
import joblib
import json
import argparse
from pathlib import Path


class SarcopeniaModelTrainer:
    """Sarkopeni model eğitim sınıfı"""
    
    def __init__(self, output_dir: str = "models"):
        """
        Eğitim sınıfını başlat
        
        Args:
            output_dir: Modellerin kaydedileceği klasör
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.scaler = StandardScaler()
        self.feature_names = None
        self.label_encoder = LabelEncoder()
        self.models = {}
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Eğitim verilerini yükle
        
        Args:
            filepath: CSV veya JSON dosyasının yolu
        
        Returns:
            Veri çerçevesi
        """
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith('.json'):
            df = pd.read_json(filepath)
        else:
            raise ValueError("CSV veya JSON formatı gerekli")
        
        print(f"Veri yüklendi: {df.shape}")
        print(f"Sütunlar: {df.columns.tolist()}")
        print(f"\nYazan istatistikleri:\n{df.describe()}")
        
        return df
    
    def prepare_features(self, df: pd.DataFrame):
        """
        Özellik matrisi hazırla
        
        Args:
            df: Orijinal veri çerçevesi
        
        Returns:
            Feature matrisi ve etiketler
        """
        # Gerekli sütunlar
        required_features = [
            'age', 'bmi',
            'grip_strength_max', 'chair_stand_time',
            'gait_speed_m_s', 'sppb_score',
            'asm_kg', 'asmi_kg_m2',
            'sarc_f_score', 'falls_last_year', 'comorbidity_count'
        ]
        
        # Varolan sütunları filtrele
        available_features = [f for f in required_features if f in df.columns]
        
        # Cinsiyet kodlaması
        if 'sex' in df.columns:
            sex_encoded = pd.get_dummies(df['sex'], prefix='sex', drop_first=True)
            X = pd.concat([df[available_features], sex_encoded], axis=1)
        else:
            X = df[available_features]
        
        # Fiziksel aktivite kodlaması
        if 'physical_activity_level' in df.columns:
            activity = pd.get_dummies(
                df['physical_activity_level'],
                prefix='physical_activity_level',
                drop_first=True
            )
            X = pd.concat([X, activity], axis=1)
        
        # Eksik değerleri doldur
        X = X.fillna(X.mean())
        
        self.feature_names = X.columns.tolist()
        
        # Hedef değişkeni encode et
        if 'sarcopenia_status' not in df.columns:
            raise ValueError("sarcopenia_status sütunu gerekli")
        
        y = df['sarcopenia_status'].astype(str)
        
        print(f"\nÖzellik sayısı: {X.shape[1]}")
        print(f"Özellik adları: {self.feature_names}")
        print(f"\nHedef değişken dağılımı:")
        print(y.value_counts())
        
        return X, y
    
    def train_binary_classifier(self, X_train, X_test, y_train, y_test):
        """
        İkili sınıflandırıcı eğit (Sarkopeni var/yok)
        """
        print("\n=== İKİLİ SINIFLANDIRICI EĞİTİMİ ===")
        
        # Hedefi binary'ye dönüştür (0: yok, 1 or 2: var)
        y_train_binary = (y_train != '0').astype(int)
        y_test_binary = (y_test != '0').astype(int)
        
        # Modelleri eğit
        models = {
            "logistic_regression": LogisticRegression(max_iter=1000, random_state=42),
            "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "xgboost": xgb.XGBClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=42
            )
        }
        
        results = {}
        for name, model in models.items():
            print(f"\n{name}:")
            model.fit(X_train, y_train_binary)
            
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test_binary, y_pred)
            prec = precision_score(y_test_binary, y_pred, zero_division=0)
            rec = recall_score(y_test_binary, y_pred, zero_division=0)
            f1 = f1_score(y_test_binary, y_pred, zero_division=0)
            
            print(f"  Accuracy: {acc:.4f}")
            print(f"  Precision: {prec:.4f}")
            print(f"  Recall: {rec:.4f}")
            print(f"  F1-Score: {f1:.4f}")
            
            results[name] = {
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "f1": f1
            }
            
            # En iyi modeli kaydet
            joblib.dump(model, self.output_dir / f"binary_{name}.pkl")
        
        return results
    
    def train_multiclass_classifier(self, X_train, X_test, y_train, y_test):
        """
        Çok sınıflı sınıflandırıcı eğit (Normal/Sarkopeni/Şiddetli)
        """
        print("\n=== ÇOKSINIFLI SINIFLANDIRICI EĞİTİMİ ===")
        
        models = {
            "random_forest": RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            ),
            "gradient_boosting": GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                random_state=42
            ),
            "xgboost": xgb.XGBClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                num_class=3,
                random_state=42
            )
        }
        
        results = {}
        for name, model in models.items():
            print(f"\n{name}:")
            model.fit(X_train, y_train)
            
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
            
            print(f"  Accuracy: {acc:.4f}")
            print(f"  Precision (weighted): {prec:.4f}")
            print(f"  Recall (weighted): {rec:.4f}")
            print(f"  F1-Score (weighted): {f1:.4f}")
            print("\n" + classification_report(y_test, y_pred))
            
            results[name] = {
                "accuracy": acc,
                "precision": prec,
                "recall": rec,
                "f1": f1
            }
            
            # Modeli kaydet
            joblib.dump(model, self.output_dir / f"multiclass_{name}.pkl")
            
            # Feature importance
            if hasattr(model, 'feature_importances_'):
                importance_dict = {
                    name: float(imp)
                    for name, imp in zip(self.feature_names, model.feature_importances_)
                }
                with open(self.output_dir / f"{name}_importance.json", 'w') as f:
                    json.dump(importance_dict, f, indent=2)
        
        return results
    
    def train_auxiliary_models(self, df: pd.DataFrame, X, y):
        """
        Yardımcı modelleri eğit (Düşük kas gücü, kütlesi, performans)
        """
        print("\n=== YARDIMCI MODELLER EĞİTİMİ ===")
        
        X_train, X_test, _, _ = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Düşük kas gücü
        print("\nDüşük kas gücü modeli:")
        if 'low_muscle_strength' in df.columns:
            y_strength = df.loc[X.index, 'low_muscle_strength'].astype(int)
            y_train_strength = y_strength.iloc[X_train.index]
            y_test_strength = y_strength.iloc[X_test.index]
            
            model_strength = RandomForestClassifier(n_estimators=50, random_state=42)
            model_strength.fit(X_train, y_train_strength)
            acc = accuracy_score(y_test_strength, model_strength.predict(X_test))
            print(f"  Accuracy: {acc:.4f}")
            joblib.dump(model_strength, self.output_dir / "aux_strength_model.pkl")
        
        # Düşük kas kütlesi
        print("\nDüşük kas kütlesi modeli:")
        if 'low_muscle_mass' in df.columns:
            y_mass = df.loc[X.index, 'low_muscle_mass'].astype(int)
            y_train_mass = y_mass.iloc[X_train.index]
            y_test_mass = y_mass.iloc[X_test.index]
            
            model_mass = RandomForestClassifier(n_estimators=50, random_state=42)
            model_mass.fit(X_train, y_train_mass)
            acc = accuracy_score(y_test_mass, model_mass.predict(X_test))
            print(f"  Accuracy: {acc:.4f}")
            joblib.dump(model_mass, self.output_dir / "aux_mass_model.pkl")
        
        # Düşük fiziksel performans
        print("\nDüşük fiziksel performans modeli:")
        if 'low_physical_performance' in df.columns:
            y_perf = df.loc[X.index, 'low_physical_performance'].astype(int)
            y_train_perf = y_perf.iloc[X_train.index]
            y_test_perf = y_perf.iloc[X_test.index]
            
            model_perf = RandomForestClassifier(n_estimators=50, random_state=42)
            model_perf.fit(X_train, y_train_perf)
            acc = accuracy_score(y_test_perf, model_perf.predict(X_test))
            print(f"  Accuracy: {acc:.4f}")
            joblib.dump(model_perf, self.output_dir / "aux_performance_model.pkl")
    
    def save_artifacts(self):
        """Eğitim artefaktlarını kaydet"""
        joblib.dump(self.scaler, self.output_dir / "scaler.pkl")
        joblib.dump(self.feature_names, self.output_dir / "feature_names.pkl")
        
        config = {
            "feature_names": self.feature_names,
            "scaler_type": "StandardScaler"
        }
        with open(self.output_dir / "config.json", 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\nArtefaktlar {self.output_dir} klasörüne kaydedildi")
    
    def run(self, data_path: str):
        """
        Tam eğitim pipeline'ını çalıştır
        """
        print("="*60)
        print("SARKOPENI MODEL EĞİTİMİ")
        print("="*60)
        
        # Veri yükle
        df = self.load_data(data_path)
        
        # Özellik hazırla
        X, y = self.prepare_features(df)
        
        # Ölçekleyiciyi eğit
        X_scaled = self.scaler.fit_transform(X)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Modelleri eğit
        binary_results = self.train_binary_classifier(X_train, X_test, y_train, y_test)
        multiclass_results = self.train_multiclass_classifier(X_train, X_test, y_train, y_test)
        self.train_auxiliary_models(df, X, y)
        
        # Artefaktları kaydet
        self.save_artifacts()
        
        # Sonuçları özetle
        print("\n" + "="*60)
        print("ÖZET")
        print("="*60)
        print("\nİKİLİ SINIFLANDIRICI SONUÇLARI:")
        for name, metrics in binary_results.items():
            print(f"\n{name}:")
            for metric, value in metrics.items():
                print(f"  {metric}: {value:.4f}")
        
        print("\n\nÇOKSINIFLI SINIFLANDIRICI SONUÇLARI:")
        for name, metrics in multiclass_results.items():
            print(f"\n{name}:")
            for metric, value in metrics.items():
                print(f"  {metric}: {value:.4f}")


def main():
    parser = argparse.ArgumentParser(
        description="Sarkopeni model eğitim script'i"
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Eğitim veri dosyası (CSV veya JSON)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="models",
        help="Model çıktı klasörü"
    )
    
    args = parser.parse_args()
    
    trainer = SarcopeniaModelTrainer(output_dir=args.output)
    trainer.run(args.data)


if __name__ == "__main__":
    main()
