# 🚀 BAŞLANGAÇ KILAVUZU - Sarkopeni Tespiti Sistemi

## 📋 İçindekiler

1. [Sistem Genel Bakış](#sistem-genel-bakış)
2. [Kurulum Seçenekleri](#kurulum-seçenekleri)
3. [Hızlı Başlangıç](#hızlı-başlangıç)
4. [Kullanım Rehberi](#kullanım-rehberi)
5. [Geliştirme Rehberi](#geliştirme-rehberi)

---

## 🏥 Sistem Genel Bakış

### Amaç
EWGSOP2 (European Working Group on Sarcopenia in Older People 2) kriterlerine dayalı yapay öğrenme kullanarak yaşlı hastalarda sarkopeni otomatik teşhis yapan kapsamlı web uygulaması.

### Sarkopeni Nedir?
Sarkopeni, yaşla ilişkili kas kütlesi ve gücünün kaybı sonucu ortaya çıkan bir bozukluktur. Mobility, kütlük, düşme riski ve yaşam kalitesinde olumsuz etkilere yol açar.

### Sistem Özellikleri
✅ İkili Sınıflandırma (Sarkopeni var/yok)
✅ Çok Sınıflı Sınıflandırma (Normal/Sarkopeni/Şiddetli)
✅ Yardımcı Modeller (Alt kriterlerin ayrı tahmini)
✅ Web Arayüzü (Kullanıcı dostu hasta veri girişi)
✅ REST API (Entegrasyon için)
✅ Veritabanı (Hasta ve test verilerini saklama)

---

## 💾 Kurulum Seçenekleri

### Seçenek 1: Docker Compose (Önerilen - 3 dakika)

**Gereksinimler:**
- Docker Desktop
- 4GB RAM
- İnternet bağlantısı

**Adımlar:**

```bash
# 1. Proje klasörüne git
cd c:\Users\User\Desktop\sarkopeni

# 2. Docker container'ları başlat
cd docker
docker-compose up -d

# 3. Bekle (ilk kez ~2-3 dakika sürer)
# Terminal'de "sarcopenia_backend | Application startup complete" görmek için bekle

# 4. Uygulamaya eriş
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
# PgAdmin: http://localhost:5050

# 5. İşini bitirince kapat
docker-compose down
```

**PgAdmin Giriş:**
- Email: admin@admin.com
- Şifre: admin

---

### Seçenek 2: Manual Kurulum (Geliştiriciler için)

#### 2.1 PostgreSQL Yükle

**Windows:**
```
https://www.postgresql.org/download/windows/
```

**Kurulum sonrası:**
```bash
# PostgreSQL CLI açılır
psql -U postgres

# Veritabanı oluştur
CREATE DATABASE sarcopenia_db;
CREATE USER user WITH PASSWORD 'password';
ALTER ROLE user SET client_encoding TO 'utf8';
ALTER ROLE user SET default_transaction_isolation TO 'read committed';
ALTER ROLE user SET default_transaction_deferrable TO on;
ALTER ROLE user SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE sarcopenia_db TO user;
\q
```

#### 2.2 Backend Kurulum

```bash
cd backend

# Python sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktifleştir
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyası oluştur ve yapılandır
copy .env.example .env
# .env dosyasını düzenle (metin editör ile açarak DATABASE_URL vs. ayarla)

# Backend'i çalıştır
python -m uvicorn app:app --reload --port 8000
```

#### 2.3 Frontend Kurulum

**Başka bir terminal açın:**

```bash
cd frontend

# Bağımlılıkları yükle
npm install

# Development sunucusu başlat
npm start
# Otomatik olarak http://localhost:3000 açılır
```

#### 2.4 ML Model Eğitimi (Opsiyonel)

**Üçüncü bir terminal açın:**

```bash
cd ml_models

# Python sanal ortam oluştur
python -m venv venv
venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Örnek veri oluştur
python create_sample_data.py

# Model eğit
python train.py --data sample_training_data.csv --output models/

# Eğitilmiş modeller models/ klasörüne kaydedilir
```

---

## 🎯 Hızlı Başlangıç

### Adım 1: Sistemi Başlat

```bash
# Docker ile
cd docker && docker-compose up -d

# VEYA manuel kurulum yapıldıysa üç terminal de:
# Terminal 1: Backend
cd backend && python -m uvicorn app:app --reload

# Terminal 2: Frontend
cd frontend && npm start

# Terminal 3: ML (opsiyonel)
cd ml_models && python create_sample_data.py
```

### Adım 2: Frontend'e Eriş

```
http://localhost:3000
```

Ekran açılmalı:
- Sol tarafta hasta bilgileri formu
- Sağ tarafta tahmin sonuçları

### Adım 3: Örnek Hasta Veri Gir

Form'u doldur (örnek değerler zaten doldur olabilir):
```
Yaş: 72
Cinsiyet: Erkek
BMI: 26.5
Kavrama Gücü: 25.3 kg
ASM: 22.5 kg
...
```

### Adım 4: Tahmin Yap

"🔍 Tahmini Yap" düğmesine tıkla

### Adım 5: Sonucu Görüntüle

Sayfanın sağ tarafında tahmin sonucu görüntülenecek:
```
TAHMINI SONUÇ: Normal / Sarkopeni / Şiddetli Sarkopeni
Güven Skoru: %55
SINIF OLASILIKLARI: [Grafik]
ALT KRİTERLER: Düşük kas gücü, kütlesi vb.
```

---

## 📖 Kullanım Rehberi

### Arayüz Bölümleri

#### 1. Sol Panel - Hasta Bilgileri Formu

**Demografik Bilgiler:**
- Yaş (yıl)
- Cinsiyet (M/F)
- BMI (kg/m²) - Oto hesaplama: weight / (height/100)²

**Kas Gücü:**
- Kavrama gücü (kg) - Sağ/sol el, max alınır
- Sandalyeden Kalma (saniye) - 5 kez tekrar süresi

**Kas Kütlesi (BIA ile ölçülen):**
- ASM: Appendiküler kas kütlesi (kg)
- ASMI: ASM / boy² (kg/m²)

**Fiziksel Performans:**
- Yürüyüş Hızı (m/s) - 4m yürüyüş testinden
- TUG: Timed Up and Go (saniye)
- SPPB: Short Physical Performance Battery (0-12)

**Ek Bilgiler:**
- SARC-F Skoru (0-10)
- Düşme (son 1 yılda kaç kez)
- Fiziksel Aktivite (Düşük/Orta/Yüksek)
- Komorbidite Sayısı

#### 2. Sağ Panel - Tahmin Sonuçları

**Ana Sonuç:**
- Sınıflandırma (Normal/Sarkopeni/Şiddetli)
- Güven Skoru (%)
- Klinik Rekomendasyonu

**Olasılık Dağılımı:**
- Normal: 0-40% (Yeşil)
- Sarkopeni: 40-60% (Turuncu)
- Şiddetli: 60-100% (Kırmızı)

**Alt Kriterler:**
- Düşük Kas Gücü: ✓ VAR / ✗ YOK
- Düşük Kas Kütlesi: ✓ VAR / ✗ YOK
- Düşük Fiziksel Performans: ✓ VAR / ✗ YOK

### EWGSOP2 Algoritması Özeti

```
Sarkopeni Yok
└─ Düşük kas gücü VEYA düşük performans YOK

Sarcopenia (Ön-tanı olarak tanıdı)
└─ Düşük kas gücü VEYA düşük performans VAR
   (Kas kütlesi ölçülemedi)

Sarcopen
└─ Düşük kas kütlesi
   VE
   (Düşük kas gücü VEYA düşük performans)

Şiddetli Sarcopenia
└─ Düşük kas kütlesi
   VE
   Düşük kas gücü
   VE
   Düşük fiziksel performans
```

---

## 🛠️ Geliştirme Rehberi

### Proje Yapısı

```
sarkopeni/
├── backend/                    # FastAPI Python uygulaması
│   ├── app.py                 # Ana uygulama (routes mount)
│   ├── models.py              # SQLAlchemy DB modelleri
│   ├── schemas.py             # Pydantic I/O şemaları
│   ├── database.py            # DB connection
│   ├── ml_service.py          # ML model inference
│   ├── routes/
│   │   ├── patients.py        # CRUD endpoints
│   │   ├── tests.py           # Test CRUD
│   │   ├── clinical.py        # Klinik veri CRUD
│   │   └── predictions.py     # ML tahmin endpoints
│   └── requirements.txt
│
├── frontend/                   # React + Material-UI
│   ├── src/
│   │   ├── App.js             # Ana component
│   │   ├── index.js           # Entry point
│   │   └── index.css
│   ├── public/
│   │   └── index.html
│   └── package.json
│
├── ml_models/                  # Model eğitimi
│   ├── train.py               # Eğitim scripti
│   ├── create_sample_data.py  # Veri oluşturma
│   ├── feature_engineering.py # Feature rehberi
│   ├── models/                # Eğitilmiş modeller (pkl)
│   └── requirements.txt
│
├── docker/
│   ├── docker-compose.yml     # Multi-container orchestration
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
│
├── README.md
└── API_DOCUMENTATION.md       # Kapsamlı API rehberi
```

### Yeni Özellik Ekleme Örneği

#### Senaryo: "Ultrason Ölçümleri" Eklemek

**1. Backend - models.py'e sütun ekle:**
```python
class SarcopeniaTest(Base):
    # ... existing fields ...
    ultrasound_muscle_thickness = Column(Float, nullable=True)
    ultrasound_echo_intensity = Column(Float, nullable=True)
```

**2. Backend - schemas.py güncelle:**
```python
class SarcopeniaTestBase(BaseModel):
    # ... existing fields ...
    ultrasound_muscle_thickness: Optional[float] = None
    ultrasound_echo_intensity: Optional[float] = None
```

**3. Frontend - form alanı ekle:**
```jsx
<TextField
  label="Ultrason Kas Kalınlığı (mm)"
  name="ultrasound_muscle_thickness"
  value={formData.ultrasound_muscle_thickness}
  onChange={handleInputChange}
/>
```

**4. ML - feature engineer'da kullan:**
```python
def prepare_features(self, df):
    # ... existing code ...
    features.append(data.get('ultrasound_muscle_thickness', 0))
    # ... rest of code ...
```

### Veritabanı Migrasyonu

Database şeması değişirse:

```bash
# Alembic ile migration oluştur (ileride)
alembic revision --autogenerate -m "Add ultrasound fields"
alembic upgrade head
```

Şimdilik otomatik migration yapılıyor (SQLAlchemy metadata.create_all())

### Modeli Yeniden Eğit

```bash
cd ml_models

# Yeni veri ile model eğit
python train.py --data new_training_data.csv --output models/

# Backend'i yeniden başlat (otomatik olarak yeni modeli yükler)
# Devam eden API çağrıları yeni model ile tahmin yapacak
```

### API Test Etme

#### FastAPI Otomatik Dokümantasyon:
```
http://localhost:8000/docs
```

Açılacak Swagger UI'da tüm endpoint'leri görebilir ve test edebilirsin.

#### cURL ile Test:
```bash
# Health check
curl http://localhost:8000/health

# Tahmin yap
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 75, "sex": "M", ...}'
```

#### Python Requests ile Test:
```python
import requests

response = requests.post(
    'http://localhost:8000/api/predict',
    json={
        'age': 75,
        'sex': 'M',
        'bmi': 26.5,
        # ... diğer alanlar ...
    }
)
print(response.json())
```

---

## 📊 Veriler

### Eğitim Veri Format

CSV olarak:
```csv
age,sex,bmi,grip_strength_max,...,sarcopenia_status
72,M,26.5,25.3,...,1
68,F,24.2,18.5,...,0
...
```

Veya JSON olarak:
```json
[
  {"age": 72, "sex": "M", "bmi": 26.5, ..., "sarcopenia_status": 1},
  {"age": 68, "sex": "F", "bmi": 24.2, ..., "sarcopenia_status": 0}
]
```

### Örnek Veri İndirmek

```bash
cd ml_models
python create_sample_data.py

# sample_training_data.csv oluşturulacak
```

---

## 🔍 Loglama ve Debug

### Backend Loglama

```python
# app.py'de
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Kullanım
logger.info("Tahmin yapıldı: " + str(prediction))
logger.error("Hata oluştu: " + str(error))
```

### Frontend Console

Tarayıcı F12 → Console sekmesinde hataları görüntüle

```javascript
// App.js'de
console.log("Tahmin sonucu:", prediction);
```

---

## 📝 Yapılacaklar (TODO)

- [ ] Kullanıcı kimlik doğrulaması (JWT)
- [ ] Çok dilli arayüz (İngilizce)
- [ ] Grafik ve raporlar (PDF export)
- [ ] Batch tahmin (CSV upload)
- [ ] Model performans dashboard'u
- [ ] Hasta portalı (kendi verilerini görmek)
- [ ] SMS/Email notifications
- [ ] Azure/AWS deployment
- [ ] Mobile uygulaması

---

## ❓ Sık Sorulan Sorular

**S: Model neden 55% confidence gösteriyor?**
C: Modelin eğitim veri kalitesine bağlı. Daha fazla etiketli veri ile iyileşebilir.

**S: Gerçek hastalarda kullanabilir miyim?**
C: Araştırma ve eğitim amacıyla. Klinik karar için uzman değerlendirmesi gerekli.

**S: Yeni veriler eklediğim halde tahmin sonuçları aynı kalıyor?**
C: Model cache'lenmiş. Backend'i yeniden başlat.

**S: PostgreSQL başlamıyor**
C: Port 5432 başka uygulama tarafından kullanıyor olabilir. 
```bash
docker-compose logs postgres
```

---

## 📞 Destek

- 📄 Dokümantasyon: API_DOCUMENTATION.md
- 🐛 Bug raporu: GitHub Issues
- 💬 Soru: Discussions

---

**Başarılar! 🚀**

Son güncelleme: 2024-12-05
