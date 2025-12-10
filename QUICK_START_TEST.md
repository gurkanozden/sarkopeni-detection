# 🚀 HIZLI TEST - PostgreSQL Olmadan Backend Başlat

## ⚠️ DURUM

PostgreSQL kurulu değil. Veritabanısız test modunda Backend'i başlatabiliriz.

---

## ✅ BACKEND'İ HEMEN BAŞLAT (Test Modu)

### Terminal'de (CMD) şu komutları çalıştır:

```cmd
cd c:\Users\User\Desktop\sarkopeni\backend

REM Virtual environment'i aktifleştir
venv\Scripts\activate.bat

REM Test Backend'i başlat (app_test.py)
python -m uvicorn app_test:app --reload --port 8000
```

### Beklediğin Çıktı:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

## 🌐 BACKEND'İ TEST ET

### 1. Tarayıcıda Aç:
```
http://localhost:8000/docs
```

✅ **Swagger UI** açılmalı (interaktif API dokümantasyonu)

### 2. Health Check:
```
http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "sarcopenia-detection",
  "database": "test-mode"
}
```

### 3. Tahmin Yap (Swagger'de TEST ET):

**Swagger UI açık → "POST /api/predict" → Try it out**

Aşağıdaki örnek veriyi yapıştır:

```json
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

**"Execute" tuşuna tıkla → Tahmin sonucunu gör!**

---

## 📊 BEKLENEN SONUÇ

```json
{
  "predicted_class": "1",
  "probability_class_0": 0.3,
  "probability_class_1": 0.5,
  "probability_class_2": 0.2,
  "confidence": 0.5,
  "low_strength_pred": true,
  "low_mass_pred": false,
  "low_performance_pred": true,
  "recommendation": "⚠️ Sarkopeni tespit edilmiştir. Direnç ve protein alımı yönünden danışmanız gerekir."
}
```

---

## 🎯 SONRAKI ADIM: Frontend'i Başlat

Backend çalışırken **ayrı bir Terminal'de**:

```cmd
cd c:\Users\User\Desktop\sarkopeni\frontend
npm install
npm start
```

Frontend açılacak: **http://localhost:3000**

---

## 🔧 PostgreSQL KURULDUKTAN SONRA

Sonra ana `app.py` dosyası ile başlatabilirsin:

```cmd
python -m uvicorn app:app --reload --port 8000
```

Şimdilik `app_test.py` kullan!

---

**✅ Backend test modunda çalışıyor!**
