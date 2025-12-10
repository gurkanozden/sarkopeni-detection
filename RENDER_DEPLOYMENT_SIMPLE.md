# 🚀 Backend Deployment (Render.com - Doğrudan Upload)

## 📦 Adım 1: Backend Klasörü Hazırla

Dosyaların var olduğunu kontrol et:
- `backend/app_test.py` ✅
- `backend/requirements.txt` ✅
- `backend/render.yaml` ✅
- `backend/.gitignore` ✅

## 🌐 Adım 2: Render.com'a Kaydol

1. Git: https://render.com
2. **"Sign Up"** → GitHub ile yapabilir
3. Dashboard açılacak

## 🚀 Adım 3: Web Service Oluştur (Manual Deployment)

### 3.1 Render Dashboard'da

1. **"New +"** tuşuna tıkla
2. **"Web Service"** seç
3. **"Deploy from a Git repository"** yerine **"Use existing Git repository"** seç

### 3.2 Ayarları Doldur

**Name**: `sarkopeni-backend`

**Runtime**: `Python 3.10`

**Build Command**:
```
pip install -r requirements.txt
```

**Start Command**:
```
uvicorn app_test:app --host 0.0.0.0 --port $PORT
```

**Environment Variables**:
```
PYTHONUNBUFFERED=true
```

**Plan**: `Free` ✅

### 3.3 Deploy Et

**"Deploy"** tuşuna tıkla (3-5 dakika bekle)

## ✅ Backend URL'sini Al

Deploy tamamlandığında:
```
https://sarkopeni-backend.onrender.com
```

## 🔧 Alt Plan: Glitch.com (Çok Kolay)

Render.com sorun verirse:

1. https://glitch.com
2. **"Create a New Project"** → **"Clone from Git"**
3. Repository: `https://github.com/gurkanozden/sarkopeni.git`
4. Otomatik deploy

## 📝 Frontend'i Güncellemeliyiz

**`frontend/.env`** dosyasında:

```
REACT_APP_API_URL=https://sarkopeni-backend.onrender.com
```

Sonra yeniden build ve deploy:
```powershell
npm run build
firebase deploy --only hosting
```

---

**Hızlı Özet**: Render.com'da Web Service oluştur → Backend URL'sini al → Frontend'e ekle → Deploy et! 🚀
