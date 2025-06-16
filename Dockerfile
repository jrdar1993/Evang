# Imagen base oficial de Python 3.12
FROM python:3.12-slim

# Evitar que Python genere .pyc y usar salida sin buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar compiladores, cabeceras de Python y librerías nativas
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

# Directorio de trabajo en el contenedor
WORKDIR /app

# Copiar todo el proyecto
COPY . .

# Actualizar pip e instalar dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Iniciar con Gunicorn, ligando al puerto que Render asigne
CMD ["sh", "-c", "gunicorn wsgi:app --bind 0.0.0.0:${PORT}"]
