# Path: create_db.py
# Purpose (en): Script to create the database for the Flask application using SQLAlchemy.
# Propósito (pt-BR): Script para criar o banco de dados para a aplicação Flask

from acessibilidade_web.app import app, db
import scripts.db.models  # para registrar as tabelas

def create_database():
    with app.app_context():
        db.create_all()
        print("✔️ Banco de dados criado com sucesso!")

if __name__ == "__main__":
    create_database()