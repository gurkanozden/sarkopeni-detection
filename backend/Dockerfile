FROM python:3.10-slim

WORKDIR /app

# Requirements'ı kopyala
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# Backend kodunu kopyala
COPY . .

# Port'u expose et
EXPOSE 8000

# Uvicorn'u çalıştır
CMD ["uvicorn", "app_test:app", "--host", "0.0.0.0", "--port", "8000"]
