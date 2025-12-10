# 🚀 Backend'i Render.com'a Deploy Et (Kolay Alternatif)

Firebase Cloud Functions yerine **Render.com** kullan (ücretsiz + basit).

---

## 🎯 Adım 1: Render.com'a Kaydol

### 1.1 Siteye Git
```
https://render.com
```

### 1.2 GitHub ile Kaydol
1. **"Sign up"** tıkla
2. **"Continue with GitHub"** seç
3. Hesap oluştur veya bağla
4. Başarılı!

---

## 🎯 Adım 2: Backend Dosyalarını Hazırla

### 2.1 Backend Klasöründe `render.yaml` Oluştur

**Dosya**: `c:\Users\User\Desktop\sarkopeni\backend\render.yaml`

```yaml
services:
  - type: web
    name: sarkopeni-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app_test:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHONUNBUFFERED
        value: true
```

### 2.2 `requirements.txt` Kontrol Et

**Dosya**: `c:\Users\User\Desktop\sarkopeni\backend\requirements.txt`

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
scikit-learn==1.3.2
xgboost==2.0.2
numpy==1.24.3
pandas==2.1.3
python-multipart==0.0.6
```

### 2.3 `.gitignore` Oluştur

**Dosya**: `c:\Users\User\Desktop\sarkopeni\backend\.gitignore`

```
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
venv/
.env
.DS_Store
*.db
```

---

## 🎯 Adım 3: GitHub'a Yükle

### 3.1 GitHub Hesabını Aç
```
https://github.com
```

### 3.2 Yeni Repository Oluştur
1. **"New"** tıkla
2. **Repository name**: `sarkopeni-detection`
3. **Public** seç
4. **Create repository** tıkla

### 3.3 Bilgisayarında Git Yap

```powershell
cd c:\Users\User\Desktop\sarkopeni

# Git başlat
git init

# GitHub URL'sini ekle (HTTPS)
git remote add origin https://github.com/YOUR_USERNAME/sarkopeni-detection.git

# Dosyaları ekle
git add .

# Commit yap
git commit -m "Initial commit: Sarcopenia detection app"

# Push et
git branch -M main
git push -u origin main
```

⚠️ **GitHub kullanıcı adı ve tokeni iste:**
- GitHub Settings > Developer settings > Personal access tokens
- Token oluştur
- Terminal'de token'ı şifre olarak gir

---

## 🎯 Adım 4: Render.com'da Deploy Et

### 4.1 Render Dashboard'a Git
```
https://dashboard.render.com
```

### 4.2 Yeni Web Service Oluştur
1. **"New +"** tıkla
2. **"Web Service"** seç
3. **GitHub repository**'ni seç: `sarkopeni-detection`
4. **Connect** tıkla

### 4.3 Konfigürasyon

**Name**: `sarkopeni-backend`

**Runtime**: `Python 3.10`

**Build Command**:
```
pip install -r backend/requirements.txt
```

**Start Command**:
```
cd backend && uvicorn app_test:app --host 0.0.0.0 --port $PORT
```

**Plan**: Free ✅

### 4.4 Deploy Et
**"Deploy"** tuşuna tıkla

**Bekleme süresi**: 3-5 dakika

---

## ✅ Backend URL'sini Al

Deploy tamamlandıktan sonra:

```
https://sarkopeni-backend-xxxx.onrender.com
```

Bu URL'i not et!

---

## 🎯 Adım 5: Frontend'i Backend'e Bağla

### 5.1 Frontend `.env` Dosyası Oluştur

**Dosya**: `c:\Users\User\Desktop\sarkopeni\frontend\.env`

```
REACT_APP_API_URL=https://sarkopeni-backend-xxxx.onrender.com
```

(xxxx yerine Render'dan aldığın URL'i koy)

### 5.2 Frontend App.js'i Düzenle

**Dosya**: `c:\Users\User\Desktop\sarkopeni\frontend\src\App.js`

```javascript
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// API çağrısı örneği
const handlePredict = async (formData) => {
  try {
    const response = await axios.post(`${API_URL}/api/predict`, formData);
    console.log('Tahmin:', response.data);
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
  }
};
```

### 5.3 Frontend'i Yeniden Build ve Deploy Et

```powershell
cd c:\Users\User\Desktop\sarkopeni\frontend

# Build
npm run build

# Firebase'e deploy
firebase deploy --only hosting
```

---

## 🌐 Son URL'ler

| Bileşen | URL |
|---------|-----|
| **Frontend** | https://sarkopeni-projesi.web.app |
| **Backend** | https://sarkopeni-backend-xxxx.onrender.com |
| **API Docs** | https://sarkopeni-backend-xxxx.onrender.com/docs |

---

## ✅ Kontrol Listesi

- [ ] Render.com'a kaydol
- [ ] GitHub'a repository oluştur
- [ ] Backend dosyalarını GitHub'a push et
- [ ] Render.com'da Web Service oluştur
- [ ] Backend URL'sini al
- [ ] Frontend `.env` dosyasını oluştur
- [ ] Frontend'i build ve deploy et

---

## 🎉 Tamamlandı!

Full-stack uygulaman şimdi tamamen **Cloud'da** çalışıyor:

✅ Frontend: Firebase Hosting  
✅ Backend: Render.com  
✅ Database: Test Mode (isteğe bağlı)

---

## 💡 İpuçları

- Render.com free plan 15 dakika inaktif kalırsa uyku moduna giriyor
  - Çözüm: Upgrade et veya cron job ile ping'le
- Backend logs Render Dashboard'da görülür
- GitHub push -> Render otomatik deploy eder

---

## 🆘 Sorun Giderme

### Build fails
```powershell
pip install -r backend/requirements.txt
python -m uvicorn app_test:app --host 0.0.0.0 --port 8000
```

### CORS error
Backend'de kodu kontrol et:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sarkopeni-projesi.web.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### GitHub push fails
```powershell
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git push
```

**Başarılı deployments! 🚀**
