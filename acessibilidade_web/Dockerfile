# Path: Dockerfile
# Purpose (en): Build and run Flask app with accessible dashboard and dynamic graphs on Render.
# Propósito (pt-BR): Construir e rodar aplicação Flask com dashboard acessível e gráficos dinâmicos no Render.

# Use imagem oficial Python
FROM python:3.11-slim

# Instale build tools necessários para dependências como scikit-learn
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Defina diretório de trabalho
WORKDIR /app

# Copie os arquivos para o contêiner
COPY . .

# Instale dependências Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Exponha porta Flask
EXPOSE 5000

# Use Gunicorn como servidor WSGI de produção
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
