# Sarkopeni Tespiti Web Uygulaması

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Docker & Docker Compose
- OR
- Python 3.10+, Node.js 18+, PostgreSQL 14+

### Docker ile Çalıştırma (Önerilen)

```bash
cd docker
docker-compose up -d
```

Uygulamaya erişin:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Dokümantasyon: http://localhost:8000/docs
- PgAdmin: http://localhost:5050

### Manuel Kurulum

#### Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt

# .env dosyası oluştur
cp .env.example .env

# Veritabanı migrate et
# (modeller otomatik oluşturulur)

python -m uvicorn app:app --reload
```

#### Frontend

```bash
cd frontend
npm install
npm start
```

#### ML Model Eğitimi

```bash
cd ml_models

# Örnek veri oluştur
python create_sample_data.py

# Model eğit
python train.py --data sample_training_data.csv --output models/
```

---

## 📊 API Endpoint'leri

### Base URL
```
http://localhost:8000/api
```

### 1. Hasta Yönetimi

#### Yeni Hasta Ekle
```http
POST /patients
Content-Type: application/json

{
  "name": "Ahmet Yılmaz",
  "sex": "M",
  "birth_date": "1952-03-15T00:00:00",
  "height_cm": 175,
  "weight_kg": 78.5,
  "bmi": 25.6
}
```

**Response (201)**
```json
{
  "id": 1,
  "name": "Ahmet Yılmaz",
  "sex": "M",
  "birth_date": "1952-03-15T00:00:00",
  "height_cm": 175,
  "weight_kg": 78.5,
  "bmi": 25.6,
  "created_at": "2024-12-05T10:30:00"
}
```

#### Hasta Bilgisi Getir
```http
GET /patients/1
```

#### Tüm Hastaları Listele
```http
GET /patients?skip=0&limit=100
```

#### Hasta Bilgisi Güncelle
```http
PUT /patients/1
Content-Type: application/json

{
  "weight_kg": 79.0,
  "bmi": 25.8
}
```

#### Hasta Sil
```http
DELETE /patients/1
```

---

### 2. Sarkopeni Testi

#### Test Sonucu Ekle
```http
POST /tests
Content-Type: application/json

{
  "patient_id": 1,
  "grip_strength_right": 28.5,
  "grip_strength_left": 26.3,
  "chair_stand_time": 14.2,
  "asm_kg": 23.5,
  "asmi_kg_m2": 8.6,
  "gait_speed_m_s": 0.95,
  "tug_time": 16.8,
  "sppb_score": 9,
  "calf_circumference": 35.2,
  "muscle_thickness": 28.5
}
```

#### Hastanın Test Sonuçlarını Getir
```http
GET /tests/patient/1
```

#### Test Sonucu Güncelle
```http
PUT /tests/1
Content-Type: application/json

{
  "asm_kg": 24.0
}
```

---

### 3. Klinik Veriler

#### Klinik Veri Ekle
```http
POST /clinical
Content-Type: application/json

{
  "patient_id": 1,
  "comorbidities": {
    "hypertension": true,
    "diabetes": false,
    "cad": true,
    "copd": false
  },
  "medication_count": 5,
  "falls_last_year": 1,
  "physical_activity_level": "moderate",
  "sarc_f_score": 3,
  "adls_score": 5,
  "iadls_score": 7
}
```

#### Hastanın Klinik Verilerini Getir
```http
GET /clinical/patient/1
```

---

### 4. Sarkopeni Tahminleme

#### Tahmin Yap
```http
POST /predict
Content-Type: application/json

{
  "age": 72,
  "sex": "M",
  "bmi": 26.5,
  "grip_strength_max": 25.3,
  "grip_strength_norm": 0.32,
  "chair_stand_time": 14.2,
  "gait_speed_m_s": 0.8,
  "tug_time": 18,
  "sppb_score": 7,
  "asm_kg": 22.5,
  "asmi_kg_m2": 8.2,
  "sarc_f_score": 4,
  "falls_last_year": 1,
  "physical_activity_level": "moderate",
  "comorbidity_count": 2
}
```

**Response (200)**
```json
{
  "predicted_class": "1",
  "probability_class_0": 0.25,
  "probability_class_1": 0.55,
  "probability_class_2": 0.20,
  "confidence": 0.55,
  "low_strength_pred": true,
  "low_mass_pred": false,
  "low_performance_pred": true,
  "recommendation": "Sarkopeni tespit edilmiştir. Direnç ve protein alımı yönünden danışmanız gerekir."
}
```

#### Tahmin Geçmişini Getir
```http
GET /predict/history/1
```

#### Model Bilgisi
```http
GET /predict/info
```

Response:
```json
{
  "model_name": "Multiclass Sarcopenia Classifier",
  "model_type": "multiclass",
  "accuracy": 0.87,
  "precision": 0.86,
  "recall": 0.85,
  "f1_score": 0.85,
  "training_date": "2024-12-05T10:30:00",
  "number_of_samples": 250,
  "feature_importance": {
    "gait_speed_m_s": 0.185,
    "sppb_score": 0.156,
    "asm_kg": 0.142,
    ...
  }
}
```

---

## 🧠 Tahmini Sınıflar

| Sınıf | Değer | Anlamı | EWGSOP2 Tanı |
|-------|-------|--------|------------|
| Normal | 0 | Sarkopeni bulgusu yok | Sarkopeni Yok |
| Sarkopeni | 1 | Kas gücü ve/veya performans düşüklüğü mevcut | Pre-Sarkopeni / Sarcopenia |
| Şiddetli Sarkopeni | 2 | Kas gücü, kütlesi ve performansında düşüklük | Severe Sarcopenia |

---

## 📈 Özellik Açıklamaları

### Demografik
- **age**: Yaş (yıl)
- **sex**: Cinsiyet (M=Erkek, F=Kadın)
- **bmi**: Vücut Kitle İndeksi (kg/m²)

### Kas Gücü & Performans
- **grip_strength_max**: Kavrama gücü maksimum (kg)
- **grip_strength_norm**: Normalize edilmiş kavrama gücü
- **chair_stand_time**: Sandalyeden 5 kez kalkma süresi (sn)
- **gait_speed_m_s**: 4m yürüyüş hızı (m/sn)
- **tug_time**: Timed Up and Go (saniye)
- **sppb_score**: Kısa Fiziksel Performans Bataryası (0-12)

### Kas Kütlesi
- **asm_kg**: Appendiküler İskeletsel Kas Kütlesi (kg)
- **asmi_kg_m2**: ASM İndeksi (kg/m²)

### Fonksiyonel
- **sarc_f_score**: SARC-F Tarama Anketi (0-10)
- **falls_last_year**: Son 1 yıl düşme sayısı

### Klinik
- **physical_activity_level**: Fiziksel aktivite (low/moderate/high)
- **comorbidity_count**: Komorbidite sayısı

---

## 🔄 İş Akışı Örneği

### Senaryo: Yeni Hasta Değerlendirmesi

```bash
# 1. Yeni hasta ekle
POST /api/patients
{
  "name": "Mehmet Kaya",
  "sex": "M",
  "birth_date": "1950-06-20",
  "height_cm": 178,
  "weight_kg": 82.0,
  "bmi": 25.9
}
→ patient_id: 5

# 2. Klinik veri ekle
POST /api/clinical
{
  "patient_id": 5,
  "comorbidities": {"ht": true, "dm": true},
  "medication_count": 6,
  "falls_last_year": 2,
  "physical_activity_level": "low",
  "sarc_f_score": 5,
  "adls_score": 4,
  "iadls_score": 5
}
→ clinical_id: 12

# 3. Test verileri ekle
POST /api/tests
{
  "patient_id": 5,
  "grip_strength_right": 18.2,
  "grip_strength_left": 17.5,
  "chair_stand_time": 19.5,
  "asm_kg": 20.1,
  "asmi_kg_m2": 6.3,
  "gait_speed_m_s": 0.72,
  "tug_time": 22.3,
  "sppb_score": 5
}
→ test_id: 15

# 4. Tahmin yap
POST /api/predict
{
  "age": 74,
  "sex": "M",
  "bmi": 25.9,
  "grip_strength_max": 18.2,
  "grip_strength_norm": 0.22,
  "chair_stand_time": 19.5,
  "gait_speed_m_s": 0.72,
  "tug_time": 22.3,
  "sppb_score": 5,
  "asm_kg": 20.1,
  "asmi_kg_m2": 6.3,
  "sarc_f_score": 5,
  "falls_last_year": 2,
  "physical_activity_level": "low",
  "comorbidity_count": 2
}
→ predicted_class: "2" (Şiddetli Sarkopeni) ⚠️

# 5. Tahmini kaydet (sonra label eklenebilir)
# Uzman değerlendirmesi sonrası...
```

---

## 🏗️ Proje Yapısı

```
sarkopeni/
├── backend/
│   ├── app.py              # FastAPI ana app
│   ├── models.py           # SQLAlchemy DB models
│   ├── schemas.py          # Pydantic schemas
│   ├── database.py         # DB connection
│   ├── ml_service.py       # ML inference
│   ├── routes/
│   │   ├── patients.py     # Hasta endpoints
│   │   ├── tests.py        # Test endpoints
│   │   ├── clinical.py     # Klinik veri endpoints
│   │   └── predictions.py  # Tahmin endpoints
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js          # Ana React component
│   │   ├── index.js        # React entry point
│   │   └── index.css
│   ├── public/
│   │   └── index.html
│   └── package.json
├── ml_models/
│   ├── train.py            # Model eğitim script
│   ├── create_sample_data.py
│   ├── feature_engineering.py
│   ├── models/             # Eğitilmiş modeller
│   └── requirements.txt
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
└── README.md
```

---

## 🔐 Ortam Değişkenleri

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/sarcopenia_db
SECRET_KEY=your-secret-key-here
DEBUG=True
ENVIRONMENT=development
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:8000/api
```

---

## 📚 Kaynaklar ve Referanslar

### EWGSOP2 Kriterleri
- **Kas Gücü Eşikleri**: [EWGSOP2 Consensus](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1748-1716.2010.02117.x)
- **Kas Kütlesi Ölçümü**: BIA veya DXA
- **Fiziksel Performans**: SPPB, Gait Speed, TUG

### Veri Kaynakları
- Geriatri klinikleri
- Fizik tedavi merkezleri
- Yaşlı bakım evleri
- Uzman değerlendirmeler

---

## 🐛 Sorun Giderme

### Veritabanı Bağlantı Hatası
```
Error: could not connect to server: Connection refused
```
Çözüm: PostgreSQL çalıştığından emin olun
```bash
docker-compose up postgres
```

### API 404 Hatası
```
"detail": "Not Found"
```
Çözüm: Endpoint yollarını kontrol edin, base URL doğru olsun

### CORS Hatası
Çözüm: Backend CORS ayarları kontrol edin (app.py'da configure edilmiştir)

---

## 📝 Test Örnekleri

### cURL ile Test

```bash
# Model bilgisi
curl http://localhost:8000/api/predict/info

# Tahmin yap
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 75,
    "sex": "F",
    "bmi": 24.5,
    "grip_strength_max": 14.2,
    "grip_strength_norm": 0.23,
    "chair_stand_time": 20.5,
    "gait_speed_m_s": 0.65,
    "tug_time": 25.0,
    "sppb_score": 4,
    "asm_kg": 18.5,
    "asmi_kg_m2": 5.2,
    "sarc_f_score": 6,
    "falls_last_year": 1,
    "physical_activity_level": "low",
    "comorbidity_count": 3
  }'
```

---

## 📞 Destek

Sorular veya problemler için:
- 📧 Email: support@sarkopeni.com
- 🐛 Buglar: GitHub Issues
- 💬 Soru-Cevap: Discussions

---

## 📄 Lisans

MIT License

**Dikkat**: Bu sistem klinik karar verme amacıyla değil, araştırma ve eğitim amacıyla kullanılmalıdır.

