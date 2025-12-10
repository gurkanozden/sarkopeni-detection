# ✅ BACKEND ÇALIŞIYOR! - API Test Talimatları

## 🎯 Backend Durum

✅ **Backend Server Başarıyla Çalışıyor!**
- **Port:** 8000
- **Adres:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs

---

## 🌐 Tarayıcıda Test Et

### 1. **Health Check** (Sistem sağlık kontrolü)

Tarayıcıda aç:
```
http://localhost:8000/health
```

**Beklediğin Sonuç:**
```json
{
  "status": "healthy",
  "service": "sarcopenia-detection",
  "database": "test-mode (PostgreSQL kurulana kadar)"
}
```

---

### 2. **API Swagger Dokümantasyon** (EN İYİ!)

Tarayıcıda aç:
```
http://localhost:8000/docs
```

✅ **Swagger UI açılacak**

**Burada:**
- Tüm API endpoint'lerini görebilirsin
- "Try it out" ile test edebilirsin
- Request/Response örneklerini görebilirsin

---

### 3. **Tahmin Yap** (API Test)

**Swagger UI'da şu adımları takip et:**

1. **http://localhost:8000/docs** açılı
2. **"POST /api/predict"** endpoint'ini aç
3. **"Try it out"** tuşuna tıkla
4. Request body'ye şunu yapıştır:

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

5. **"Execute"** tuşuna tıkla

**Beklediğin Sonuç:**
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

## 📊 TÜM API ENDPOINT'LERİ

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| **GET** | `/` | Root (Hoş geldin) |
| **GET** | `/health` | Health check |
| **POST** | `/api/predict` | **Tahmin yap (MAIN)** |
| **GET** | `/api/models/info` | Model bilgisi |

---

## 🎯 SONRAKI ADIM: Frontend Başlat

Backend çalışırken, **Terminal 2'de** Frontend'i başlat:

```cmd
cd c:\Users\User\Desktop\sarkopeni\frontend
npm install
npm start
```

Frontend açılacak: **http://localhost:3000**

---

## 📱 Frontend Uygulaması

Frontend başlayınca web uygulaması açılır:
- Form: Hasta bilgileri gir
- Button: "Tahmini Yap" tuşuna tıkla
- Result: Tahmin sonucunu görüntüle

---

## 🔗 API ENDPOINTS (cURL Örnekleri)

### Health Check:
```bash
curl http://localhost:8000/health
```

### Tahmin Yap:
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

---

## ✅ DEVAM ET

### **HEMEN ŞU ADRESTE TEST ET:**
```
http://localhost:8000/docs
```

Swagger UI'da tüm endpoint'leri görebilir ve test edebilirsin!

---

**Backend başarıyla çalışıyor! 🎉**
