# 🎯 SARKOPENI SİSTEMİ - EKSIK BAĞIMLILIKLARINI KURULUM REHBERİ

## ❌ ŞU ANDA KURULANMIŞ OLANLAR

✅ Python 3.10
❌ Node.js (Frontend için gerekli)
❌ PostgreSQL (Veritabanı için gerekli)
❌ Docker (Containerization için)

---

## 📥 GEREKLİ YAZILIMLARI KURA

### 1. Node.js Kurulumu (Frontend için)

**Node.js İndir:**
- https://nodejs.org/en/
- **LTS sürümünü** indir (18+ veya 20+)

**Windows Kurulum:**
1. İndirilen `.msi` dosyasını çift tıkla
2. "Installer" penceresinde "Next" tıkla
3. Lisans koşullarını kabul et → "Next"
4. Kurulum konumunu kabul et → "Next"
5. Opsiyonları varsayılan bırak → "Next"
6. "Install" tuşuna tıkla → "Finish"

**Kontrol Et:**
```powershell
node --version
npm --version
```

Çıktı:
```
v18.19.0
9.6.4
```

---

### 2. PostgreSQL Kurulumu (Veritabanı için)

**PostgreSQL İndir:**
- https://www.postgresql.org/download/windows/

**Windows Kurulum:**
1. `postgresql-15-setup-windows-x64.exe` çalıştır
2. **Kurulum konumu** → "Next" (varsayılan C:\Program Files\PostgreSQL\15)
3. **Bileşenleri seç** → pgAdmin, Stack Builder hepsini seç
4. **Data Directory** → "Next" (varsayılan)
5. **Superuser Password** → `postgres` (not et!)
6. **Port** → `5432` (varsayılan)
7. **Locale** → "Turkish, Turkey" seç
8. **Install** → Bitmeyi bekle (~5 dakika)
9. **Stack Builder** → "Finish" (opsiyonel)

**Kontrol Et:**
```powershell
psql --version
```

Çıktı:
```
psql (PostgreSQL) 15.x
```

---

### 3. Docker Desktop Kurulumu (Opsiyonel ama Önerilen)

**Docker Desktop İndir:**
- https://www.docker.com/products/docker-desktop/

**Windows Kurulum (WSL2 Required):**
1. Installer'ı çalıştır
2. "Use WSL 2 instead of Hyper-V" seç
3. WSL kurulmasını izin ver
4. "Install" → Bilgisayarı yeniden başlat
5. Docker Desktop uygulamasını aç

**Kontrol Et:**
```powershell
docker --version
docker run hello-world
```

---

## 🚀 KURULUM TAMAMLANDIKTAN SONRA

### Adım 1: PostgreSQL Veritabanı Oluştur

**Terminal açarak:**

```powershell
# PostgreSQL'e bağlan
psql -U postgres

# Şifreni gir: postgres

# Komutları çalıştır
CREATE DATABASE sarcopenia_db;
CREATE USER sarcopenia_user WITH PASSWORD 'sarcopenia_pass';
ALTER ROLE sarcopenia_user SET client_encoding TO 'utf8';
ALTER ROLE sarcopenia_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE sarcopenia_user SET default_transaction_deferrable TO on;
ALTER ROLE sarcopenia_user SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE sarcopenia_db TO sarcopenia_user;
\q
```

---

### Adım 2: Backend Başlat

**Terminal 1:**

```cmd
cd c:\Users\User\Desktop\sarkopeni\backend

REM Virtual environment'i aktifleştir
venv\Scripts\activate.bat

REM .env dosyasını güncelle (DATABASE_URL'yi ayarla)
REM .env dosyasını düzenle ve şuna değiştir:
REM DATABASE_URL=postgresql://sarcopenia_user:sarcopenia_pass@localhost:5432/sarcopenia_db

REM Backend'i başlat (ana app.py ile - PostgreSQL desteği ile)
python -m uvicorn app:app --reload --port 8000
```

✅ Çıktı: `Application startup complete`

---

### Adım 3: Frontend Başlat

**Terminal 2 (Terminal 1 çalışırken):**

```cmd
cd c:\Users\User\Desktop\sarkopeni\frontend

REM Bağımlılıkları yükle (ilk kez 2-3 dakika sürer)
npm install

REM Development sunucusunu başlat
npm start
```

✅ Tarayıcı otomatik açılacak: `http://localhost:3000`

---

### Adım 4: ML Model (Opsiyonel)

**Terminal 3:**

```cmd
cd c:\Users\User\Desktop\sarkopeni\ml_models

REM Virtual environment
python -m venv venv
venv\Scripts\activate.bat

REM Bağımlılıklar
pip install -r requirements.txt

REM Örnek veri oluştur
python create_sample_data.py

REM Model eğit (5-10 dakika)
python train.py --data sample_training_data.csv --output models/
```

✅ Eğitilmiş modeller `models/` klasörüne kaydedilecek

---

## ✅ KURULUM KONTROL LİSTESİ

- [ ] Node.js kurulu ve çalışıyor (`node --version`)
- [ ] npm kurulu ve çalışıyor (`npm --version`)
- [ ] PostgreSQL kurulu ve çalışıyor (`psql --version`)
- [ ] Backend virtual environment oluşturuldu
- [ ] Backend bağımlılıkları yüklendi (`pip install -r requirements.txt`)
- [ ] Frontend bağımlılıkları yüklendi (`npm install`)
- [ ] `.env` dosyası DatabaseURL ile güncellendi
- [ ] PostgreSQL veritabanı oluşturuldu

---

## 🎯 TEST ET

Hepsi hazırlandıktan sonra:

### 1. Backend Health Check
```
http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "sarcopenia-detection",
  "database": "connected"
}
```

### 2. API Swagger
```
http://localhost:8000/docs
```

### 3. Frontend
```
http://localhost:3000
```

Frontend'de:
- Form doldur
- "Tahmini Yap" tuşuna tıkla
- Sonuç görüntüle

---

## 📊 FULL STACK DURUM

```
✅ Python 3.10 - Backend geliştirme
✅ Node.js 18+ - Frontend build/serve
✅ PostgreSQL 15 - Veritabanı
⏳ Docker (opsiyonel) - Containerization

SONRA ÇALIŞACAKLAR:
✅ Backend (FastAPI) - Port 8000
✅ Frontend (React) - Port 3000
✅ Database (PostgreSQL) - Port 5432
✅ ML Models - sklearn, XGBoost
```

---

## 🆘 SORUN GIDERME

### `npm: command not found`
- Node.js'i yeniden kur
- Bilgisayarı yeniden başlat
- PATH environment variable'ı kontrol et

### `psql: command not found`
- PostgreSQL'i yeniden kur
- PATH environment variable'ı kontrol et
- `C:\Program Files\PostgreSQL\15\bin` PATH'e ekle

### `pip: command not found`
- Python'u yeniden kur
- "Add Python to PATH" seç

### Database Connection Error
```
could not connect to server: Connection refused
```
- PostgreSQL servisinin çalışıp çalışmadığını kontrol et
- Windows Hizmetler: `postgresql-x64-15`'i ara ve başlat

---

## 🎉 BAŞARILI KURULUM GÖSTERGELERI

1. **Terminal 1 - Backend:**
   ```
   INFO:     Application startup complete
   ```

2. **Terminal 2 - Frontend:**
   ```
   Compiled successfully!
   ```
   Tarayıcı `http://localhost:3000` açılır

3. **Swagger UI:**
   `http://localhost:8000/docs` açılır ve endpoint'ler görüntülenir

4. **Form Çalışır:**
   Hasta verilerini girip tahmin yapabilirsin

---

**Kurulum tamamlandı! Uygulamayı kullanmaya başla! 🚀**
