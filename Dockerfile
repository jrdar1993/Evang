# Imagen base oficial de Python 3.12
FROM python:3.12-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    libffi-dev \
    libpq-dev \
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

# Crear el directorio de trabajo
WORKDIR /app

# Copiar todo
COPY . .

# Instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Iniciar con Gunicorn
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:10000"]
