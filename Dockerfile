FROM python:3.11-slim

# Instala dependências do sistema necessárias para dlib e face-recognition
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopencv-dev \
    libboost-all-dev \
    libx11-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Atualiza pip
RUN pip install --upgrade pip setuptools wheel

# Copia requirements do backend
COPY backend/requirements.txt .

# Instala dependências Python (instala numpy primeiro, depois dlib, depois o resto)
RUN pip install --no-cache-dir numpy==1.26.3 && \
    pip install --no-cache-dir dlib==19.24.2 && \
    pip install --no-cache-dir -r requirements.txt

# Copia aplicação do backend
COPY backend/ .

# Cria diretórios necessários
RUN mkdir -p uploads/faces /tmp

# Expõe porta
EXPOSE 8000

# Comando padrão
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
