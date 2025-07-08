# Path: Dockerfile
# Purpose (en): Build Flask app with scikit-learn and serve with Gunicorn on Render
# Propósito (pt-BR): Construir app Flask com scikit-learn e servir com Gunicorn no Render

FROM python:3.11-slim

# Instala dependências de build para Cython e extensões C
RUN apt-get update && \
    apt-get install -y build-essential gcc g++ python3-dev && \
    pip install --upgrade pip && \
    pip install cython

WORKDIR /app

COPY . /app

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta Flask
EXPOSE 5000

# Usa Gunicorn para produção
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]