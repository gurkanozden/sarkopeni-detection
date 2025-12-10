import pandas as pd
import numpy as np
from pathlib import Path


def create_sample_data(output_file: str = "sample_training_data.csv", n_samples: int = 200):
    """
    Örnek eğitim veri seti oluştur
    
    Args:
        output_file: Çıktı dosyasının adı
        n_samples: Örnek sayısı
    """
    np.random.seed(42)
    
    data = {
        # Demografik
        'age': np.random.uniform(60, 85, n_samples),
        'sex': np.random.choice(['M', 'F'], n_samples),
        'height_cm': np.random.uniform(150, 185, n_samples),
        'weight_kg': np.random.uniform(50, 100, n_samples),
        'bmi': np.random.uniform(18, 35, n_samples),
        
        # Kas gücü
        'grip_strength_right': np.random.uniform(10, 50, n_samples),
        'grip_strength_left': np.random.uniform(10, 50, n_samples),
        'chair_stand_time': np.random.uniform(5, 20, n_samples),
        
        # Kas kütlesi
        'asm_kg': np.random.uniform(15, 30, n_samples),
        'asmi_kg_m2': np.random.uniform(4, 10, n_samples),
        
        # Fiziksel performans
        'gait_speed_m_s': np.random.uniform(0.5, 1.5, n_samples),
        'tug_time': np.random.uniform(10, 30, n_samples),
        'sppb_score': np.random.uniform(0, 12, n_samples),
        
        # Ek ölçümler
        'calf_circumference': np.random.uniform(25, 40, n_samples),
        'muscle_thickness': np.random.uniform(15, 35, n_samples),
        
        # Fonksiyonel
        'sarc_f_score': np.random.uniform(0, 10, n_samples),
        'adls_score': np.random.uniform(0, 6, n_samples),
        'iadls_score': np.random.uniform(0, 8, n_samples),
        
        # Klinik
        'medication_count': np.random.randint(0, 10, n_samples),
        'falls_last_year': np.random.randint(0, 5, n_samples),
        'physical_activity_level': np.random.choice(['low', 'moderate', 'high'], n_samples),
        'comorbidity_count': np.random.randint(0, 5, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Hedef değişkenleri oluştur (basit buluşsal kurallarla)
    df['grip_strength_max'] = df[['grip_strength_right', 'grip_strength_left']].max(axis=1)
    df['grip_strength_norm'] = df['grip_strength_max'] / df['weight_kg']
    
    # Sarkopeni durumu (0: yok, 1: var, 2: şiddetli)
    sarcopenia_score = 0
    sarcopenia_score += (df['grip_strength_max'] < 20).astype(int)
    sarcopenia_score += (df['asmi_kg_m2'] < 6).astype(int)
    sarcopenia_score += (df['gait_speed_m_s'] < 1.0).astype(int)
    sarcopenia_score += (df['sppb_score'] < 8).astype(int)
    
    df['sarcopenia_status'] = pd.cut(
        sarcopenia_score,
        bins=[-0.5, 1.5, 2.5, 4.5],
        labels=['0', '1', '2']
    ).astype(str)
    
    # Alt kriterler
    df['low_muscle_strength'] = (df['grip_strength_max'] < 20).astype(int)
    df['low_muscle_mass'] = (df['asmi_kg_m2'] < 6).astype(int)
    df['low_physical_performance'] = (df['gait_speed_m_s'] < 1.0).astype(int)
    
    # Labeling bilgileri
    experts = ['Dr. Ahmet', 'Dr. Fatma', 'Dr. Mehmet', 'Pt. Ayşe']
    df['labeled_by'] = np.random.choice(experts, n_samples)
    df['labeled_at'] = pd.date_range(start='2024-01-01', periods=n_samples, freq='D')
    
    # Dosyaya kaydet
    df.to_csv(output_file, index=False)
    print(f"Örnek veri {output_file} adıyla kaydedildi ({n_samples} kayıt)")
    print(f"\nVeri özeti:")
    print(df.head())
    print(f"\nSütunlar: {df.columns.tolist()}")
    print(f"\nSarkopeni durumu dağılımı:")
    print(df['sarcopenia_status'].value_counts())


if __name__ == "__main__":
    create_sample_data()
