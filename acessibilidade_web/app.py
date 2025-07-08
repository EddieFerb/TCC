# Path: acessibilidade_web/app.py
# Purpose (en): Flask web server for accessible dashboard with dynamic graph generation using IA, ready for Render deployment.
# Propósito (pt-BR): Servidor web Flask para dashboard acessível com geração dinâmica de gráficos usando IA, pronto para deploy no Render.

from flask import Flask, render_template, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

app = Flask(__name__)

# Caminho para base de dados processada
BASE_PATH = '../dados/processado/dados_ingresso_evasao_conclusao.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ajuda')
def ajuda():
    return render_template('ajuda/ajuda.html')

@app.route('/gerar-grafico', methods=['POST'])
def gerar_grafico():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    curso = data.get('curso', '').lower()
    ano = data.get('ano', '')
    ies = data.get('ies', '').lower()

    df = pd.read_csv(BASE_PATH)

    if curso:
        df = df[df['nome_curso'].str.lower().str.contains(curso)]
    if ano:
        try:
            df = df[df['ano'] == int(ano)]
        except ValueError:
            pass
    if ies:
        df = df[df['nome_ies'].str.lower().str.contains(ies)]

    if df.empty:
        return jsonify({'error': 'Nenhum dado encontrado.'})

    plt.figure(figsize=(10, 6))
    plt.plot(df['ano'], df['ingressantes'], label='Ingressantes')
    plt.plot(df['ano'], df['concluintes'], label='Concluintes')
    plt.plot(df['ano'], df['evasao'], label='Evasão')
    plt.title(f"Evolução - {curso.title() if curso else 'Todos'}")
    plt.xlabel("Ano")
    plt.ylabel("Total")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"grafico_{curso}_{ies}_{ano}_{timestamp}.png"
    filepath = os.path.join('static', 'graficos', filename)
    plt.savefig(filepath)
    plt.close()

    grafico_url = f'static/graficos/{filename}'
    return jsonify({'grafico_url': grafico_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)