# Usamos una imagen base más reciente con soporte ARM64
FROM python:2.7.18-slim

WORKDIR /app

# Actualizar las fuentes de paquetes a una versión que aún esté disponible
RUN echo "deb http://archive.debian.org/debian/ buster main" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security/ buster/updates main" >> /etc/apt/sources.list

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    python-dev \
    zlib1g-dev \
    libjpeg-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python-tk \
    && rm -rf /var/lib/apt/lists/*

# Instalar pip y dependencias de Python
COPY requirements_fiscal.txt .
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org -r requirements_fiscal.txt

# Copiar el resto de la aplicación
COPY . .

EXPOSE 12000

CMD ["python", "server.py"]   