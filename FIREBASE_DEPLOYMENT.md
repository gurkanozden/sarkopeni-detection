# 🚀 Firebase'e Dağıtım Rehberi (Adım Adım)

## 📋 Gerekli Bilgiler

- **Google Hesabı** (Gmail): Var mı?
- **Kredi Kartı**: Firebase kullanımı için (ilk 12 ay ücretsiz)
- **Bilgisayarında**: Node.js, npm (✅ Zaten var)

---

## 🎯 Adım 1: Firebase Projesini Oluştur

### 1.1 Firebase Console'e Git
```
https://console.firebase.google.com
```

### 1.2 Google Hesabıyla Giriş Yap
- Gmail adresin ile oturum aç
- Ücretsiz deneme başlat (kredi kartı gerekli ama para çekilmez ilk 12 ay)

### 1.3 Yeni Proje Oluştur
1. **"+ Proje Oluştur"** tuşuna tıkla
2. Proje Adı: `sarkopeni-detection` (veya istediğin ad)
3. **Devam Et** tıkla
4. Google Analytics: **Devre Dışı Bırak** (maliyeti azaltır)
5. **Proje Oluştur** tıkla (2-3 dakika bekle)

### 1.4 Proje Türünü Seç
Proje açıldıktan sonra sol tarafta menu görülecek:
- Hosting
- Realtime Database
- Cloud Firestore
- Cloud Functions
- vb.

---

## 🌐 Adım 2: Frontend'i Firebase Hosting'e Yükle

### 2.1 Firebase CLI'yı Kur
PowerShell'de çalıştır:
```powershell
npm install -g firebase-tools
```

### 2.2 Firebase'de Oturum Aç
```powershell
firebase login
```
- Tarayıcı açılacak
- Google hesapla oturum aç
- "Allow" tuşuna tıkla
- Terminal'de tamamlanacak

### 2.3 Frontend Klasöründe Firebase Başlat
```powershell
cd c:\Users\User\Desktop\sarkopeni\frontend
firebase init hosting
```

**Sorular sorulacak:**

1️⃣ **"Which Firebase project do you want to associate with this directory?"**
   - `sarkopeni-detection` seç (veya oluşturduğun proje adı)

2️⃣ **"What do you want to use as your public directory?"**
   - `build` yazıp Enter (React build klasörü)

3️⃣ **"Configure as a single-page app?"**
   - `Y` (Yes) yazıp Enter

4️⃣ **"Set up automatic builds?"**
   - `N` (No) yazıp Enter (GitHub Actions istemiyoruz)

5️⃣ **"Overwrite existing file?"**
   - `N` (No) yazıp Enter

### 2.4 Firebase Dosyaları Kontrol Et
```powershell
ls -la firebase.json
```

`firebase.json` dosyası oluşmuş olmalı.

### 2.5 Frontend'i Build Et
```powershell
cd c:\Users\User\Desktop\sarkopeni\frontend
npm run build
```

**Bu komut:**
- React kodunu derler (compile)
- `build/` klasörü oluşturur
- 2-3 dakika alır

Bittiğinde:
```
The build folder is ready to be deployed.
```

### 2.6 Firebase Hosting'e Deploy Et
```powershell
firebase deploy --only hosting
```

**Çıktı örneği:**
```
✔ Deploy complete!

Project Console: https://console.firebase.google.com/project/sarkopeni-detection/overview
Hosting URL: https://sarkopeni-detection.web.app
```

🎉 **Frontend'in URL'si**: `https://sarkopeni-detection.web.app`

---

## ⚙️ Adım 3: Backend'i Cloud Functions'a Yükle

### 3.1 Cloud Functions'ı Aç
Firebase Console'de:
1. Sol menüden **"Build"** > **"Functions"** tıkla
2. **"Başlayın"** tıkla
3. Plan seç: **Spark Plan** (ücretsiz) veya **Blaze** (pay-as-you-go)

### 3.2 Backend Klasöründe Firebase Başlat
```powershell
cd c:\Users\User\Desktop\sarkopeni\backend
firebase init functions
```

**Sorular:**

1️⃣ **"Which project?"**
   - `sarkopeni-detection` seç

2️⃣ **"What language?"**
   - `Python` seç (veya JavaScript)

3️⃣ **"Do you want to install dependencies?"**
   - `Y` yazıp Enter

### 3.3 Backend Kodunu Düzenle
`backend/functions/main.py` oluşacak. Bunu düzenle:

```python
import functions_framework
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
import json

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Health Check
@app.get("/health")
def health():
    return {"status": "healthy", "service": "sarcopenia-detection"}

# Tahmin Endpoint
@app.post("/api/predict")
def predict(data: dict):
    # app_test.py'den copy-paste yap
    # ... prediction logic ...
    return {
        "predicted_class": "1",
        "confidence": 0.65,
        "probability_class_0": 0.2,
        "probability_class_1": 0.65,
        "probability_class_2": 0.15,
        "recommendation": "Sarkopeni tespit edilmiştir.",
        "auxiliary_criteria": {}
    }

@functions_framework.http
def sarcopenia_api(request):
    """HTTP Cloud Function"""
    from fastapi.middleware.cors import CORSMiddleware
    
    return app(request)
```

### 3.4 Requirements Dosyasını Düzenle
`backend/functions/requirements.txt`:
```
fastapi==0.104.1
pydantic==2.5.0
scikit-learn==1.3.2
xgboost==2.0.2
numpy==1.24.3
pandas==2.1.3
```

### 3.5 Deploy Et
```powershell
firebase deploy --only functions
```

**Çıktı:**
```
✔ Deploy complete!

Function URL: https://us-central1-sarkopeni-detection.cloudfunctions.net/sarcopenia_api
```

---

## 🔗 Adım 4: Frontend'i Backend'e Bağla

### 4.1 Frontend `.env` Dosyası Oluştur
`frontend/.env`:
```
REACT_APP_API_URL=https://us-central1-sarkopeni-detection.cloudfunctions.net/sarcopenia_api
```

### 4.2 Frontend App.js'de Düzenle
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Tahmin API çağrısı
const response = await axios.post(`${API_URL}/api/predict`, formData);
```

### 4.3 Frontend'i Yeniden Build ve Deploy Et
```powershell
cd c:\Users\User\Desktop\sarkopeni\frontend
npm run build
firebase deploy --only hosting
```

---

## 📊 Adım 5: Database Seçeneği (İsteğe Bağlı)

### Seçenek A: Cloud Firestore (Kolay)
```powershell
firebase init firestore
```

### Seçenek B: PostgreSQL (Cloud SQL)
1. Firebase Console > **"Cloud SQL"**
2. **"Örnek Oluştur"** > PostgreSQL seç
3. Machine Type: `db-f1-micro` (ucuz)

**Bağlantı String:**
```
postgresql://user:password@ip:5432/sarkopeni
```

---

## ✅ Kontrol Listesi

| Adım | Tamamlandı? |
|------|-----------|
| Google Hesabı oluşturdum | ☐ |
| Firebase Projesi oluşturdum | ☐ |
| Firebase CLI kurdum | ☐ |
| Frontend build ettim | ☐ |
| Frontend deploy ettim | ☐ |
| Backend Functions kurdum | ☐ |
| Backend deploy ettim | ☐ |
| Frontend ve Backend bağladım | ☐ |

---

## 🌐 Son URL'ler

| Bileşen | URL |
|---------|-----|
| **Frontend** | `https://sarkopeni-detection.web.app` |
| **Backend** | `https://us-central1-sarkopeni-detection.cloudfunctions.net/sarcopenia_api` |
| **Firebase Console** | `https://console.firebase.google.com` |

---

## 💰 Maliyet Tahmini (Aylık)

| Hizmet | Spark Plan (Ücretsiz) | Blaze Plan |
|--------|----------------------|-----------|
| Hosting | ✅ Ücretsiz | ✅ ~$0.18/GB |
| Functions | ✅ 2M çağrı/ay | ✅ $0.40/M çağrı |
| Firestore | ✅ 1GB | ✅ $0.06/100K read |

**İlk 12 ay Google Cloud kredisi: $300 BEDAVA!**

---

## 🆘 Sorun Giderme

### ❌ "firebase command not found"
```powershell
npm install -g firebase-tools
```

### ❌ "Project not found"
Firebase Console'de doğru projeyi seçtiğini kontrol et

### ❌ "Build fails"
```powershell
npm install
npm run build
```

### ❌ "CORS error"
Backend'de CORS middleware'ini etkinleştir:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sarkopeni-detection.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📚 Faydalı Linkler

- Firebase Docs: https://firebase.google.com/docs
- Cloud Functions: https://cloud.google.com/functions/docs
- Firebase Hosting: https://firebase.google.com/docs/hosting
- Pricing Calculator: https://firebase.google.com/pricing

---

## 🎯 Özet

1. ✅ Google Hesabı ile Firebase Projesi oluştur
2. ✅ Frontend'i build et → Hosting'e yükle
3. ✅ Backend'i Cloud Functions'a yükle
4. ✅ Frontend ve Backend'i bağla
5. ✅ Türkiye'den erişim kontrol et

**Bittiğinde:** Proje 24/7 çalışacak, internet olan herkes erişebilecek! 🌍

---

**Sorular? İlk adımdan başla: Firebase Console'e git!** 🚀
