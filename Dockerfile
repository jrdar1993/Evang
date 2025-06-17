# Imagen base oficial de Python 3.12
FROM python:3.12-slim

# Evitar .pyc y usar salida sin buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar compiladores y librerías necesarias
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

# Directorio de trabajo
WORKDIR /app

# Primero copiamos solo requirements para cache correcto
COPY requirements.txt .

# Instalamos dependencias primero (mejor para el cache de Docker)
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt

# Luego copiamos el resto de los archivos
COPY . .

# Definimos el puerto por defecto 10000 (Render usa este)
ENV PORT 10000

# Comando de arranque de Gunicorn
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:10000"]
