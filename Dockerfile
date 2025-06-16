# Imagen base oficial de Python 3.12
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1️⃣ Instalamos build-essential (incluye gcc/g++/make), Python headers y librerías de sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    libffi-dev \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    liblcms2-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libpng-dev \
    libart-2.0-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# 2️⃣ Instalamos las deps de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 3️⃣ Arrancamos con Gunicorn
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:10000"]
