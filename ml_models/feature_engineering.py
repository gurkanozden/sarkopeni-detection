import numpy as np
import pandas as pd
from pathlib import Path


def create_feature_engineering_guide():
    """Özellik mühendisliği rehberi oluştur"""
    
    guide = """
# SARKOPENI ÖZELLİK MÜHENDİSLİĞİ REHBERİ

## 1. Demografik Özellikler

### Yaş (age)
- Sarkopeni riski yaşla artış gösterir
- Kategorik değişken olarak da kodlanabilir: 60-69, 70-79, 80+
- Interaction: age * physical_activity_level

### Cinsiyet (sex)
- Cinsiyete göre farklı eşik değerleri vardır
- M/F one-hot encoding

### BMI
- Aşırı zayıflık ve obeite her ikisi de sarkopeni riskini artırır
- Polinomial features: bmi^2
- Categories: Underweight, Normal, Overweight, Obese

## 2. Kas Gücü Özelikleri

### Kavrama Gücü (Grip Strength)
- **grip_strength_max**: sağ ve sol el arasından maksimum
- **grip_strength_min**: minimum
- **grip_strength_mean**: ortalama
- **grip_strength_norm**: kavrama gücü / vücut ağırlığı (normalizasyon)
- **grip_strength_diff**: sağ - sol (asimetri)
- Cinsiyet ve yaşa göre referans değerleri:
  * Erkekler: <27 kg (60-69y), <25 kg (70-79y), <23 kg (80+y)
  * Kadınlar: <16 kg (60-69y), <15 kg (70-79y), <13 kg (80+y)

### Sandalyeden Kalkma Testi (Chair Stand Time)
- Kas gücü ve fonksiyonel performans göstergesi
- 30 saniye içindeki tekrar sayısı normalize edilebilir
- >12 saniye = düşük performans

## 3. Kas Kütlesi Özelikleri

### ASMI (Appendicular Skeletal Muscle Index)
- **asm_kg**: Toplam appendiküler kas kütlesi
- **asmi_kg_m2**: ASM / (height_m^2) - normalize edilmiş
- Eşik değerleri (EWGSOP2):
  * Erkekler: <7.0 kg/m²
  * Kadınlar: <5.5 kg/m²

### Alt Ekstremite Ölçümleri
- Baldır çevresi: <31 cm → düşük kas kütlesi göstergesi
- Uyluk çevresi
- Kas kalınlığı (ultrason): anterior femoral

## 4. Fiziksel Performans Özelikleri

### Gait Speed (4m Yürüyüş Testi)
- **gait_speed_m_s**: meter/saniye cinsinden
- Eşik: <1.0 m/s → düşük performans
- Inverse: 1 / gait_speed (daha lineer ilişki)
- Kategorik: slow (<0.8), moderate (0.8-1.2), fast (>1.2)

### TUG (Timed Up and Go)
- Toplam saniye
- Mobilite ve düşme riskinin göstergesi
- Eşik: >12 saniye → düşük performans

### SPPB (Short Physical Performance Battery)
- Gait speed component (0-4 puan)
- Chair stand component (0-4 puan)
- Balance component (0-4 puan)
- Toplam: 0-12 puan
- Eşik: <8 puan → düşük performans

## 5. Fonksiyonel ve Anket Özelikleri

### SARC-F Skoru
- Kas gücü: 0-2 puan
- Yardımla yapılan faaliyetler: 0-2 puan
- Hastalanma süresi: 0-2 puan
- Düşme sayısı: 0-2 puan
- Mobilite: 0-2 puan
- Toplam: 0-10 puan
- Eşik: ≥4 → sarkopeni olasılığı yüksek

### ADL (Günlük Yaşam Aktiviteleri)
- Banyo, tuvalet, giyinme vb.
- Toplam skor: 0-6
- Categories: Independent, Dependent

### IADL (Enstrümental ADL)
- Telefon, alışveriş, temizlik, ilaç yönetimi vb.
- Toplam skor: 0-8

## 6. Klinik Özellikler

### Komorbidite
- Yüksek tansiyon (HT)
- Diabetes (DM)
- Koroner arter hastalığı (CAD)
- KOAH
- Totaldeki komorbidite sayısı
- One-hot encoding veya toplam sayı

### Polıfarmasi (İlaç Sayısı)
- Sayı: 0-15+
- Kategorik: <5, 5-9, ≥10

### Düşme Öyküsü
- Son 1 yıl düşme sayısı
- Binary: Düşme var/yok
- Multinom kategoriler: 0, 1-2, 3+

### Fiziksel Aktivite
- IPAQ kategorileri: Low, Moderate, High
- Haftalık ortalama aktivite saati
- Sedanter davranış (oturma saati)

## 7. Türetilmiş (Derived) Özellikler

### Kas Fonksiyon Oranı
- muscle_strength_ratio = grip_strength / asm_kg
- Kas kalitesi göstergesi

### Yaşa Normalizasyon
- age_normalized = (age - 65) / 20
- Linear model'ler için yararlı

### Etkileşim Terimleri
- age * bmi
- asm_kg * gait_speed
- age * grip_strength

### Polinomial Özellikler
- bmi^2
- age^2

## 8. Eksik Veri İşleme

### Eksik Değerlerin Doldurulması
1. Ortalama ile doldur (sayısal)
2. Medyan ile doldur (robust)
3. KNN ile doldur (k=5)
4. Domain knowledge ile doldur
5. Eksik veri kategorisi oluştur (isNaN feature)

### Eksik Veri Göstergesi
- is_grip_strength_missing = 1 if grip_strength is NaN else 0

## 9. Normalizasyon ve Standardizasyon

### StandardScaler (Z-score normalizasyon)
- Uygun: Linear regression, Logistic regression, SVM
- Formula: (x - mean) / std

### MinMaxScaler
- Uygun: Neural networks, tree-based models'de seçmeli
- Range: [0, 1]

### RobustScaler
- Uygun: Outlier'lar varsa
- Quartiles kullanır

## 10. Outlier Tespiti ve İşleme

### IQR Yöntemi
- Lower bound: Q1 - 1.5 * IQR
- Upper bound: Q3 + 1.5 * IQR
- Outlier: boundaries dışında

### Z-score Yöntemi
- |z| > 3: Strong outlier
- |z| > 2.5: Moderate outlier

### İşleme Yöntemleri
1. Silme (az sayıda ise)
2. Capping (min/max değerle sınırla)
3. Transformation (log, square root)
4. Ayrı kategori oluştur

## Özetlenmiş Feature Set

### Minimum (Temel) Set (~10 özellik)
- age
- sex
- bmi
- grip_strength_max
- asm_kg
- asmi_kg_m2
- gait_speed_m_s
- sppb_score
- sarcopenia_status (hedef)

### Standard Set (~20 özellik)
- Minimum set +
- grip_strength_norm
- grip_strength_diff
- chair_stand_time
- tug_time
- calf_circumference
- sarc_f_score
- falls_last_year
- medication_count
- physical_activity_level
- comorbidity_count

### Extended Set (~40+ özellik)
- Standard set +
- Tüm cinsiyet/aktivite etkileşimleri
- Polinomial features
- Türetilmiş oranlar
- Demografik kategoriler
- Outlier göstergeleri

## Uygulama Örneği (Python)

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Veri yükleme
df = pd.read_csv('sarcopenia_data.csv')

# 1. Temel özellikler
df['grip_strength_max'] = df[['grip_strength_right', 'grip_strength_left']].max(axis=1)
df['grip_strength_norm'] = df['grip_strength_max'] / df['weight_kg']
df['grip_strength_diff'] = df['grip_strength_right'] - df['grip_strength_left']

# 2. Kategorik kodlama
df['sex_M'] = (df['sex'] == 'M').astype(int)
activity_dummies = pd.get_dummies(df['physical_activity_level'], prefix='activity', drop_first=True)
df = pd.concat([df, activity_dummies], axis=1)

# 3. Etkileşim terimleri
df['age_bmi'] = df['age'] * df['bmi']
df['asm_gait_speed'] = df['asm_kg'] * df['gait_speed_m_s']

# 4. Normalizasyon
scaler = StandardScaler()
numeric_features = ['age', 'bmi', 'grip_strength_max', 'asm_kg', 'asmi_kg_m2', 'gait_speed_m_s', 'sppb_score']
df[numeric_features] = scaler.fit_transform(df[numeric_features])

# 5. Eksik veri
df.fillna(df.mean(), inplace=True)

print("Özellikler hazırlandı!")
print(f"Toplam özellik: {len(df.columns)}")
```

## Kaynaklar
- EWGSOP2 Konsensus: https://onlinelibrary.wiley.com/doi/full/10.1111/j.1748-1716.2010.02117.x
- Sarcopenia Criteria: Age and Ageing journal
"""
    
    return guide


if __name__ == "__main__":
    guide_content = create_feature_engineering_guide()
    
    with open("FEATURE_ENGINEERING.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("Özellik mühendisliği rehberi oluşturuldu: FEATURE_ENGINEERING.md")
