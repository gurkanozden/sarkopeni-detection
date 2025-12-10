# 🚀 DOCKER OLMADAN MANUEL KURULUM REHBERI

Docker Desktop yüklü değilse, **Manuel Kurulum** seçeneğini kullanabilirsiniz.

---

## 📋 KURULUM ADIMSU

### Adım 1: PostgreSQL Kurulumu

**Option A: Docker Kullanmadan PostgreSQL Kurulum**

1. **Windows üzerinde PostgreSQL indir**:
   - https://www.postgresql.org/download/windows/
   - En son sürümü indir (15+)

2. **Kurulum sırasında**:
   - Port: `5432` (default)
   - Username: `user`
   - Password: `password`
   - Database: `postgres` (oluşturulur)

3. **Kurulum bitince CMD/PowerShell açarak test et**:
   ```powershell
   psql -U postgres
   ```
   - Password: postgres (kurulum sırasında belirlediğin)
   - Giriş başarılı → `\q` ile çık

4. **Veritabanı oluştur**:
   ```sql
   psql -U postgres
   
   CREATE DATABASE sarcopenia_db;
   CREATE USER sarcopenia_user WITH PASSWORD 'sarcopenia_pass';
   ALTER ROLE sarcopenia_user SET client_encoding TO 'utf8';
   ALTER ROLE sarcopenia_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE sarcopenia_user SET default_transaction_deferrable TO on;
   ALTER ROLE sarcopenia_user SET default_transaction_read_only TO off;
   GRANT ALL PRIVILEGES ON DATABASE sarcopenia_db TO sarcopenia_user;
   \q
   ```

**Option B: Kolayca - SQL Server Express (Alternatif)**
- https://www.microsoft.com/en-us/sql-server/sql-server-downloads

---

### Adım 2: Backend Kurulum

**Terminal 1'i aç ve şu komutları çalıştır:**

```powershell
# 1. Backend klasörüne git
cd "c:\Users\User\Desktop\sarkopeni\backend"

# 2. Python virtual environment oluştur
python -m venv venv

# 3. Sanal ortamı aktifleştir
.\venv\Scripts\Activate

# 4. Bağımlılıkları yükle
pip install -r requirements.txt

# 5. .env dosyasını oluştur
copy .env.example .env
```

6. **.env dosyasını düzenle** (Notepad veya VS Code ile açar):
   ```
   DATABASE_URL=postgresql://sarcopenia_user:sarcopenia_pass@localhost:5432/sarcopenia_db
   SECRET_KEY=your-secret-key-change-me-12345
   DEBUG=True
   ENVIRONMENT=development
   ```

7. **Backend'i başlat**:
   ```powershell
   python -m uvicorn app:app --reload --port 8000
   ```

   ✅ Çıktıda şunu görmelisin:
   ```
   INFO:     Application startup complete
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

---

### Adım 3: Frontend Kurulum

**Terminal 2'yi aç (Terminal 1 çalışırken) ve şu komutları çalıştır:**

```powershell
# 1. Frontend klasörüne git
cd "c:\Users\User\Desktop\sarkopeni\frontend"

# 2. Node bağımlılıklarını yükle
npm install

# 3. Development sunucusu başlat
npm start
```

✅ Tarayıcı otomatik açılmalı: **http://localhost:3000**

---

### Adım 4: ML Model Eğitimi (Opsiyonel)

**Terminal 3'ü aç (diğerleri çalışırken) ve şu komutları çalıştır:**

```powershell
# 1. ML klasörüne git
cd "c:\Users\User\Desktop\sarkopeni\ml_models"

# 2. Python virtual environment oluştur
python -m venv venv

# 3. Sanal ortamı aktifleştir
.\venv\Scripts\Activate

# 4. Bağımlılıkları yükle
pip install -r requirements.txt

# 5. Örnek veri oluştur
python create_sample_data.py

# 6. Model eğit
python train.py --data sample_training_data.csv --output models/
```

✅ Eğitilmiş modeller `models/` klasörüne kaydedilecek

---

## 🎯 KURULUM TAMAMLANDIKTAN SONRA

### Terminal Durumu:
```
Terminal 1: Backend (http://localhost:8000) ✅ Çalışıyor
Terminal 2: Frontend (http://localhost:3000) ✅ Çalışıyor
Terminal 3: ML (opsiyonel) ✅ Tamam
```

### Erişim Noktaları:

| Servis | URL | Durum |
|--------|-----|-------|
| Frontend | http://localhost:3000 | Web Uygulaması |
| Backend API | http://localhost:8000 | REST API |
| Swagger Docs | http://localhost:8000/docs | API Dokümantasyon |
| ReDoc | http://localhost:8000/redoc | Alternative Docs |

---

## 📝 KULLANIM ÖRNEĞI

### 1. Frontend'e Eriş
```
http://localhost:3000
```

### 2. Hastanın Bilgilerini Gir
- Yaş: 72
- Cinsiyet: Erkek (M)
- BMI: 26.5
- Kavrama Gücü: 25.3 kg
- ASM: 22.5 kg
- ASMI: 8.2 kg/m²
- Yürüyüş Hızı: 0.8 m/s
- SPPB Skoru: 7
- SARC-F: 4
- Düşme: 1
- Aktivite: Moderate
- Komorbidite: 2

### 3. "Tahmini Yap" Tuşuna Tıkla

### 4. Sonucu Görüntüle
```
TAHMIN: Sarkopeni (Sınıf 1)
Güven: 55%
Olasılıklar:
- Normal (0): 25%
- Sarkopeni (1): 55%
- Şiddetli (2): 20%
```

---

## 🔧 SORUN GIDERME

### Sorun 1: "pip: command not found"
```powershell
# Çözüm: Virtual environment'i aktifleştir
cd backend
.\venv\Scripts\Activate

# Veya tam yol
C:\Users\User\Desktop\sarkopeni\backend\venv\Scripts\Activate.ps1
```

### Sorun 2: PostgreSQL Bağlantı Hatası
```
Error: could not connect to server
```
**Çözüm:**
```powershell
# PostgreSQL servisinin çalışıp çalışmadığını kontrol et
Get-Service postgresql-x64-15  # veya sürümüne göre

# Eğer durduysa başlat
Start-Service postgresql-x64-15
```

### Sorun 3: Port Zaten Kullanılıyor
```
Address already in use
```
**Çözüm:**
```powershell
# Hangi process portu kullanıyor bulundoğu
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess

# Port değiştir
python -m uvicorn app:app --reload --port 8001
```

### Sorun 4: npm install Hatası
```powershell
# npm cache temizle
npm cache clean --force

# Tekrar yükle
npm install
```

### Sorun 5: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'fastapi'
```
**Çözüm:**
```powershell
# Virtual environment aktif mi kontrol et
(venv) C:\...> 

# Değilse aktifleştir
.\venv\Scripts\Activate

# Tekrar yükle
pip install -r requirements.txt
```

---

## 📚 API TEST ETME (cURL / Python)

### Option 1: PowerShell ile Test

```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:8000/health"

# Tahmin yap
$body = @{
    age = 72
    sex = "M"
    bmi = 26.5
    grip_strength_max = 25.3
    gait_speed_m_s = 0.8
    sppb_score = 7
    asm_kg = 22.5
    asmi_kg_m2 = 8.2
    sarc_f_score = 4
    falls_last_year = 1
    physical_activity_level = "moderate"
    comorbidity_count = 2
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/predict" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body
```

### Option 2: Python ile Test

```python
import requests
import json

# Tahmin yap
data = {
    "age": 72,
    "sex": "M",
    "bmi": 26.5,
    "grip_strength_max": 25.3,
    "gait_speed_m_s": 0.8,
    "sppb_score": 7,
    "asm_kg": 22.5,
    "asmi_kg_m2": 8.2,
    "sarc_f_score": 4,
    "falls_last_year": 1,
    "physical_activity_level": "moderate",
    "comorbidity_count": 2
}

response = requests.post(
    "http://localhost:8000/api/predict",
    json=data
)

print(json.dumps(response.json(), indent=2))
```

---

## 🛑 UYGULAMAYI DURDURMA

### Terminal'de Ctrl+C tuşuna basın:
```
^C
KeyboardInterrupt
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete
```

### Tüm Terminalları Kapat:
```
Terminal 1: Backend - Ctrl+C
Terminal 2: Frontend - Ctrl+C
Terminal 3: ML - (zaten bitmişti)
```

### PostgreSQL'i Durdur:
```powershell
Stop-Service postgresql-x64-15
```

---

## 💾 VERİTABANINI YEDEKLE

```powershell
# Backup al
pg_dump -U sarcopenia_user -d sarcopenia_db -f backup.sql

# Geri yükle
psql -U sarcopenia_user -d sarcopenia_db -f backup.sql
```

---

## ✅ BAŞARILI KURULUM GÖSTERGELERI

- ✅ Backend Terminal'de "Application startup complete" mesajı
- ✅ Frontend otomatik tarayıcıda açıldı (http://localhost:3000)
- ✅ http://localhost:8000/docs Swagger UI açılıyor
- ✅ Form formu görüntüleniyor ve interaktif
- ✅ Tahmin yapabiliyorsun
- ✅ Sonuç grafikle gösteriliyor

---

## 📞 İLETİŞİM

Sorunlar için:
- Terminal hata mesajı kopyala
- Dokümantasyonu kontrol et: `GETTING_STARTED.md`
- API docs: `http://localhost:8000/docs`

---

**🎉 Kurulum Tamamlandı! Uygulamayı Kullanmaya Başla!**

Tarih: 2024-12-05
