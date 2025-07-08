# Path: scripts/db/models.py
# Purpose (en): Define database models for the Flask application using SQLAlchemy.
# Propósito (pt-BR): Define modelos de banco de dados para a aplicação Flask usando


from flask_sqlalchemy import SQLAlchemy
from acessibilidade_web.app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Resultado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer)
    indicador = db.Column(db.String(50))
    valor = db.Column(db.Float)