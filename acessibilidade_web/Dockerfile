# Path: Dockerfile
# Purpose (en): Build Flask app with scikit-learn and serve with Gunicorn on Render
# Propósito (pt-BR): Construir app Flask com scikit-learn e servir com Gunicorn no Render

# Use uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de dependências primeiro (para usar cache de camadas)
COPY requirements.txt requirements.txt

# Instala as dependências do projeto
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta que o Render vai acessar
EXPOSE 5000

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Comando para iniciar o app Flask usando gunicorn (melhor para produção)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]