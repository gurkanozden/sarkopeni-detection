# Sarkopeni Tespiti - ML Web Uygulaması

EWGSOP2 kriterlerine dayalı yapay öğrenme kullanarak sarkopeni (yaşlılarda kas kaybı) otomatik teşhisi yapan kapsamlı web uygulaması.

## Özellikler

- **İkili Sınıflandırma**: Sarkopeni var/yok
- **Çok Sınıflı Sınıflandırma**: Normal / Sarkopeni / Şiddetli Sarkopeni
- **Yardımcı Modeller**: "Düşük kas gücü var mı?" gibi alt kriterler
- **Web Arayüzü**: Hasta verileri girişi ve sonuç visualizasyonu
- **REST API**: Entegrasyon için Flask/FastAPI backend
- **Veri Yönetimi**: PostgreSQL ile hasta ve test verileri saklama

## Proje Yapısı

```
sarkopeni/
├── backend/              # FastAPI uygulaması
│   ├── app.py           # Ana uygulama
│   ├── models.py        # Veritabanı modelleri
│   ├── schemas.py       # Pydantic şemaları
│   ├── routes/          # API endpoint'leri
│   ├── requirements.txt  # Python bağımlılıkları
│   └── .env.example     # Ortam değişkenleri
├── frontend/            # React + TypeScript arayüzü
│   ├── src/
│   ├── public/
│   └── package.json
├── ml_models/           # ML model eğitimi ve inference
│   ├── train.py         # Model eğitim script'i
│   ├── feature_engineering.py
│   ├── models/          # Eğitilmiş modeller
│   └── requirements.txt
├── docker/              # Docker yapılandırması
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
└── data/                # Örnek veri ve label'lar
```

## Teknoloji Stack'i

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React 18+, TypeScript, Material-UI
- **ML**: scikit-learn, XGBoost, pandas, numpy
- **Database**: PostgreSQL
- **Deployment**: Docker, Docker Compose

## Kurulum

### Gereksinimler
- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Docker & Docker Compose

### Backend Kurulumu

```bash
cd backend
pip install -r requirements.txt
# PostgreSQL connection ayarla
python -m uvicorn app:app --reload
```

### Frontend Kurulumu

```bash
cd frontend
npm install
npm start
```

## Veritabanı Şeması

### patients (Hastalar)
- id (PK)
- name/code
- sex (M/F)
- birth_date
- height_cm, weight_kg, bmi
- created_at

### clinical_data (Klinik Veriler)
- id (PK)
- patient_id (FK)
- comorbidities (JSON)
- medication_count
- falls_last_year
- physical_activity_level
- sarc_f_score, adls_score

### sarcopenia_tests (Sarkopeni Testleri)
- id (PK)
- patient_id (FK)
- grip_strength_right, grip_strength_left
- chair_stand_time
- asm_kg, asmi_kg_m2
- gait_speed_m_s
- tug_time
- sppb_score
- created_at

### labels (Eğitim Label'ları)
- id (PK)
- patient_id (FK)
- test_id (FK → sarcopenia_tests.id)
- sarcopenia_status (0=yok, 1=var, 2=şiddetli)
- labeled_by
- labeled_at

## API Endpoint'leri

### Hasta Yönetimi
- `POST /api/patients` - Yeni hasta ekle
- `GET /api/patients/{id}` - Hasta bilgisi getir
- `PUT /api/patients/{id}` - Hasta bilgisi güncelle

### Test Yönetimi
- `POST /api/tests` - Yeni test sonucu ekle
- `GET /api/tests/{id}` - Test sonuçları getir

### Sarkopeni Tahmini
- `POST /api/predict` - Sarkopeni tahmini yap
- `GET /api/predict/{id}` - Geçmiş tahminleri getir

### Model Yönetimi
- `GET /api/models/info` - Model bilgisi
- `POST /api/models/retrain` - Model yeniden eğit

## ML Model Mimarisi

### Özellikler (Features)

**Demografik:**
- age, sex, bmi

**Kas Gücü & Performans:**
- grip_strength_max = max(sağ, sol)
- grip_strength_norm = grip / body_weight
- chair_stand_time
- gait_speed_m_s
- tug_time
- sppb_score

**Kas Kütlesi:**
- asm_kg, asmi_kg_m2

**Ek Özellikler:**
- sarc_f_score
- falls_last_year
- physical_activity_level_encoded
- comorbidity_count

### Modeller
1. **Binary Classification** (Sarkopeni var/yok)
   - Logistic Regression (baseline)
   - Random Forest
   - XGBoost

2. **Multi-class Classification** (Normal/Sarkopeni/Şiddetli)
   - Random Forest
   - XGBoost
   - Gradient Boosting

3. **Auxiliary Models** (Alt kriterler)
   - Düşük kas gücü (Low muscle strength)
   - Düşük kas kütlesi (Low muscle mass)
   - Düşük fiziksel performans (Low physical performance)

## Eğitim Veri Formatı

CSV veya JSON formatında, aşağıdaki sütunlar gerekli:

```
age, sex, height_cm, weight_kg, bmi, grip_strength_right, grip_strength_left, 
chair_stand_time, asm_kg, asmi_kg_m2, gait_speed_m_s, tug_time, sppb_score,
sarc_f_score, falls_last_year, physical_activity_level, comorbidities_count,
sarcopenia_status (label)
```

## Modeli Eğitme

```bash
cd ml_models
python train.py --data data.csv --model xgboost --output models/
```

## API Kullanım Örneği

```bash
# Tahmin yap
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 72,
    "sex": "M",
    "bmi": 26.5,
    "grip_strength_max": 25.3,
    "gait_speed_m_s": 0.8,
    "sppb_score": 7,
    "asm_kg": 22.5,
    "asmi_kg_m2": 8.2,
    "sarc_f_score": 4,
    "falls_last_year": 1
  }'
```

## Lisans

MIT

## İletişim

Sorular için: sarkopeni@example.com
