# 🎉 SARKOPENI TESPITI SİSTEMİ - BAŞLAMA TALIMATÇ

## ✅ DURUM: Backend Çalışıyor!

```
🟢 Backend Server (Port 8000) - ACTIVE
   ✅ Health Check: http://localhost:8000/health
   ✅ Swagger UI: http://localhost:8000/docs
   ✅ API Ready: http://localhost:8000/api/predict
```

---

## 🚀 BAŞLANGIC ADIMLARI

### Adım 1: Swagger API Dokümantasyonunu Aç
```
http://localhost:8000/docs
```

### Adım 2: Tahmin Test Et (Swagger'de)
1. **POST /api/predict** endpoint'ini aç
2. **"Try it out"** tuşuna tıkla
3. Aşağıdaki test verilerini yapıştır:

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

4. **"Execute"** tuşuna tıkla

### Adım 3: Sonucu Gözlemle
```json
{
  "predicted_class": "1",      ← Sarkopeni tespit edildi
  "confidence": 0.5,           ← %50 güven
  "probability_class_0": 0.3,  ← Normal: %30
  "probability_class_1": 0.5,  ← Sarkopeni: %50
  "probability_class_2": 0.2,  ← Şiddetli: %20
  "recommendation": "Sarkopeni tespit edilmiştir..."
}
```

---

## 🌐 Mevcut API Endpoints

| Endpoint | Metod | Açıklama |
|----------|-------|----------|
| `/` | GET | Root endpoint |
| `/health` | GET | Health check |
| `/api/predict` | POST | **Tahmin yap** |
| `/api/models/info` | GET | Model bilgisi |

---

## 📝 Tahmini Sınıfları

| Sınıf | Değer | Anlamı |
|-------|-------|--------|
| **0** | Normal | Sarkopeni bulgusu yok |
| **1** | Sarkopeni | Kas gücü ve/veya performans düşüklüğü |
| **2** | Şiddetli Sarkopeni | Tüm kriterler düşük |

---

## 🎯 SON ADIM: Frontend Başlat

Backend çalışırken, **YENİ BİR TERMINAL PENCERESI AÇARAK:**

```cmd
cd c:\Users\User\Desktop\sarkopeni\frontend
npm install
npm start
```

Frontend açılacak: **http://localhost:3000**

Web uygulamasında:
- Hasta bilgileri formu doldur
- "Tahmini Yap" tuşuna tıkla
- Sonucu grafikle görüntüle

---

## 📚 Dokümantasyon Referansları

| Dosya | İçerik |
|-------|--------|
| **BACKEND_RUNNING.md** | Backend talimatları (bu dosya) |
| **RUN_PROJECT.md** | Tam proje başlatma rehberi |
| **API_DOCUMENTATION.md** | Detaylı API referansı |
| **INSTALLATION_REQUIREMENTS.md** | Gerekli yazılım kurulumu |
| **README.md** | Proje özeti |

---

## 💡 Önemli Noktalar

✅ Backend test modunda (PostgreSQL olmadan)  
✅ Swagger UI ile API test edebilirsin  
✅ Frontend için Node.js gerekli  
✅ 3 farklı sarkopeni sınıfı tahmin yapılabiliyor  
✅ ML modelleri basit heuristik kullanıyor  

---

## 🆘 Sorun?

- **Backend kapanıyorsa**: Tekrar başlat
- **Port zaten kullanılıyorsa**: Port değiştir (8001 vb.)
- **Swagger açılmıyorsa**: Tarayıcıyı yenile (F5)
- **API Timeout**: Backend çalışıp çalışmadığını kontrol et

---

## 🎉 BAŞARILI BAŞLAMA!

**Şimdi Swagger UI'da Test Et:**
```
👉 http://localhost:8000/docs
```

**Terminal'de Backend şu çalışıyor:**
```
✅ INFO:     Application startup complete
✅ INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

**Proje başarıyla çalışıyor! 🚀**

Sonraki: Frontend'i başlat ve web uygulamasını kullan!
