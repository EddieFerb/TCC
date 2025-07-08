# Path: acessibilidade_web/app.py
# Purpose (en): Main Flask application for visualizing and analyzing educational data.
# Propósito (pt-BR): Aplicação Flask principal para visualização e análise de dados

from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Caminho para base de dados processada
BASE_PATH = '../dados/processado/dados_ingresso_evasao_conclusao.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ajuda')
def ajuda():
    return render_template('ajuda/ajuda.html')

@app.route('/grafico-evasao')
def grafico_evasao():
    return render_template('grafico_evasao.html')

@app.route('/gerar-grafico', methods=['POST'])
def gerar_grafico():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    curso = data.get('curso', '').lower()
    ies = data.get('ies', '').lower()
    ano = data.get('ano', '').strip()

    df = pd.read_csv(BASE_PATH, sep=';')

    if curso:
        df = df[df['nome_curso'].str.lower().str.contains(curso)]
    if ies:
        try:
            df = df[df['id_ies'] == int(ies)]
        except ValueError:
            pass
    if ano:
        try:
            df = df[df['ano'] == int(ano)]
        except ValueError:
            pass

    if df.empty:
        return jsonify({'error': 'Nenhum dado encontrado.'})

    plt.figure(figsize=(10, 6))
    plt.plot(df['taxa_ingresso'], label='Taxa Ingresso')
    plt.plot(df['taxa_conclusao'], label='Taxa Conclusão')
    plt.plot(df['taxa_evasao'], label='Taxa Evasão')
    plt.title(f"Taxas - {curso.title() if curso else 'Todos'}")
    plt.xlabel("Registros")
    plt.ylabel("Taxa")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"grafico_{curso}_{ies}_{timestamp}.png"
    filepath = os.path.join('static', 'graficos', filename)
    plt.savefig(filepath)
    plt.close()

    grafico_url = f'static/graficos/{filename}'
    return jsonify({'grafico_url': grafico_url})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)