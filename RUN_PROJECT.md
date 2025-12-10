# 🚀 SARKOPENI SİSTEMİ - HEMEN BAŞLAMA REHBERİ

## 🎯 MİNİMUM SETUP (15 dakika)

### ✅ Durum
- ✅ Python 3.10 - Kurulu
- ✅ Backend bağımlılıkları - Kurulu
- ❌ Node.js - **GEREKLI**
- ❌ PostgreSQL - Opsiyonel (test modu var)

---

## 📥 Node.js Kurulumu (5 dakika)

### Windows'ta Kurulum Adımları:

**1. Node.js İndir:**
- https://nodejs.org/en/
- **LTS sürümünü** indir (18+ veya 20+)
- `.msi` dosyasını indirdin

**2. Kurulum Sihirbazını Çalıştır:**
- `.msi` dosyasına çift tıkla
- **Next** → **Kabul Et** → **Next** → **Next** → **Next** → **Install** → **Finish**
- Bilgisayarı yeniden başlatmasını belirtirse başlat

**3. Doğrula (PowerShell açarak):**
```powershell
node --version
npm --version
```

Çıktı:
```
v18.19.0
9.6.4
```

✅ **Node.js Kurulu!**

---

## 🚀 PROJE BAŞLAT (3 Terminal Açarak)

### Terminal 1: Backend (Port 8000)

```cmd
cd c:\Users\User\Desktop\sarkopeni\backend

REM Virtual environment'i aktifleştir
venv\Scripts\activate.bat

REM Backend'i başlat
python -m uvicorn app_test:app --reload --port 8000
```

**Beklediğin çıktı:**
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

✅ Backend çalışıyor: **http://localhost:8000**

---

### Terminal 2: Frontend (Port 3000)

**Terminal 1 çalışırken, yeni bir Terminal aç:**

```cmd
cd c:\Users\User\Desktop\sarkopeni\frontend

REM npm bağımlılıklarını yükle (ilk kez ~2-3 dakika)
npm install

REM Frontend'i başlat
npm start
```

**Beklediğin çıktı:**
```
webpack compiled successfully
Compiled successfully!
```

Tarayıcı otomatik açılmalı: **http://localhost:3000**

✅ Frontend çalışıyor!

---

### Terminal 3: (Opsiyonel) ML Models

**Eğitilmiş ML modelleri yoksa:**

```cmd
cd c:\Users\User\Desktop\sarkopeni\ml_models

python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt

REM Örnek veri oluştur
python create_sample_data.py

REM Model eğit (5-10 dakika)
python train.py --data sample_training_data.csv --output models/
```

---

## 🌐 UYGULAMAYA ERIŞIM

| Servis | URL | Açıklama |
|--------|-----|----------|
| **Frontend** | http://localhost:3000 | Web Uygulaması |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger Dokümantasyon |

---

## 📝 İLK TEST

### 1. Frontend Açılmışsa (http://localhost:3000):
   - Hasta bilgileri formu görüntülenecek
   - Input alanları otomatik dolu olabilir

### 2. Test Verisi Gir:
```
Yaş: 72
Cinsiyet: M
BMI: 26.5
Kavrama Gücü: 25.3 kg
ASM: 22.5 kg
...
```

### 3. "Tahmini Yap" Tuşuna Tıkla

### 4. Sonuç Göreceksin:
```
TAHMIN: Sarkopeni (Sınıf 1)
Güven: 55%
Olasılıklar:
- Normal (0): 30%
- Sarkopeni (1): 50%
- Şiddetli (2): 20%
```

---

## ✅ BAŞARILI ÇALIŞMA GÖSTERGELERI

Terminal 1 (Backend):
```
✅ INFO:     Application startup complete
```

Terminal 2 (Frontend):
```
✅ Compiled successfully!
✅ Tarayıcıda http://localhost:3000 açılır
```

Frontend:
```
✅ Form görüntüleniyor
✅ Input alanları aktif
✅ "Tahmini Yap" tuşu çalışıyor
```

---

## 🆘 SORUN GIDERME

### Sorun 1: "npm: command not found"
- Node.js yüklediğin?
- Bilgisayarı yeniden başlat
- Tekrar denetle: `node --version`

### Sorun 2: Frontend compile error
```cmd
cd frontend
npm cache clean --force
npm install
npm start
```

### Sorun 3: Port zaten kullanılıyor
- Port değiştir:
  - Backend: `python -m uvicorn app_test:app --reload --port 8001`
  - Frontend: `DANGEROUSLY_DISABLE_HOST_CHECK=true PORT=3001 npm start`

### Sorun 4: Backend çökme
```cmd
cd backend
venv\Scripts\activate.bat
pip install -r requirements.txt --force-reinstall
python -m uvicorn app_test:app --reload --port 8000
```

---

## 🛑 UYGULAMAYI KAPAT

Her Terminal'de **Ctrl+C** tuşuna bas:

```
^C
INFO:     Shutdown complete
```

---

## 📚 DAHA FAZLA DETAY

| Konu | Dosya |
|------|-------|
| Kurulum Sorunları | `INSTALLATION_REQUIREMENTS.md` |
| Manual Kurulum | `MANUAL_INSTALLATION.md` |
| API Referansı | `API_DOCUMENTATION.md` |
| Tam Dokümantasyon | `GETTING_STARTED.md` |

---

## 🎉 BAŞARILI KURULUM!

Node.js yüklü olunca, Terminal 1, 2, 3'de sırasıyla bu komutları çalıştır:

```cmd
# Terminal 1
cd c:\Users\User\Desktop\sarkopeni\backend && venv\Scripts\activate.bat && python -m uvicorn app_test:app --reload --port 8000

# Terminal 2
cd c:\Users\User\Desktop\sarkopeni\frontend && npm install && npm start

# Terminal 3 (opsiyonel)
cd c:\Users\User\Desktop\sarkopeni\ml_models && python -m venv venv && venv\Scripts\activate.bat && pip install -r requirements.txt && python create_sample_data.py && python train.py --data sample_training_data.csv --output models/
```

**Erişim:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs

---

**Kullanmaya başla! 🚀**
