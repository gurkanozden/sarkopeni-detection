# 🚀 Render.com Deployment - GitHub Olmadan (En Kolay Yol)

## Adım 1: Render.com'da Web Service Oluştur

1. **https://render.com** aç
2. Dashboard'da **"New +"** → **"Web Service"**
3. **"Public Git Repository"** seçeneğini seç (Git Provider yerine)

## Adım 2: Repository URL Gir

**Public Git URL** alanına:
```
https://github.com/gurkanozden/sarkopeni.git
```

## Adım 3: Konfigüre Et

| Alan | Değer |
|------|-------|
| **Name** | `sarkopeni-backend` |
| **Region** | `Frankfurt (EU)` (Türkiye'ye yakın) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `cd backend && pip install -r requirements.txt` |
| **Start Command** | `cd backend && uvicorn app_test:app --host 0.0.0.0 --port $PORT` |
| **Plan** | `Free` |

## Adım 4: Environment Variables

**Environment Variables** bölümüne ekle:
```
PYTHONUNBUFFERED=true
```

## Adım 5: Deploy

**"Deploy"** tuşuna tıkla → 3-5 dakika bekle

## ✅ Backend URL'sini Al

Deploy tamamlandığında URL şu olacak:
```
https://sarkopeni-backend-xxxxx.onrender.com
```

## 🔄 Frontend'i Güncelle

**`frontend/.env`** dosyasında:
```
REACT_APP_API_URL=https://sarkopeni-backend-xxxxx.onrender.com
```

## 🚀 Frontend'i Yeniden Deploy Et

```powershell
cd c:\Users\User\Desktop\sarkopeni\frontend
npm run build
firebase deploy --only hosting
```

---

**TAMAMDI! Artık full-stack cloud'da çalışıyor!** 🎉

Frontend: https://sarkopeni-projesi.web.app  
Backend: https://sarkopeni-backend-xxxxx.onrender.com
