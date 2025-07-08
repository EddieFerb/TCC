# Path: Dockerfile
# Purpose (en): Build and run Flask app with accessible dashboard and dynamic graphs on Render.
# Propósito (pt-BR): Construir e rodar aplicação Flask com dashboard acessível e gráficos dinâmicos no Render.

# Use imagem oficial Python
FROM python:3.11-slim

# Defina diretório de trabalho
WORKDIR /app

# Copie tudo
COPY . /app

# Instale dependências
RUN pip install --no-cache-dir -r requirements.txt

# Exponha porta Flask
EXPOSE 5000

# Execute o app
CMD ["python", "acessibilidade_web/app.py"]
