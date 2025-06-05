from flask import Flask, render_template, request, send_file, jsonify
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# Caminho da base consolidada (pode ser adaptado)
BASE_PATH = '../dados/processado/dados_ingresso_evasao_conclusao.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar-grafico', methods=['POST'])
def gerar_grafico():
    # Suporte para JSON ou Form
    if request.is_json:
        dados = request.get_json()
    else:
        dados = request.form

    curso = dados.get('curso', '').lower()
    ano = dados.get('ano', '')
    ies = dados.get('ies', '').lower()

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
        return render_template('index.html', erro="Nenhum dado encontrado.")

    # Validação: a IES precisa ter pelo menos dados entre 2009 e 2023
    anos_disponiveis = df['ano'].dropna().unique()
    anos_esperados = set(range(2009, 2024))
    if not anos_esperados.issubset(set(anos_disponiveis)):
        return render_template('index.html', erro="Dados incompletos para o período 2009–2023.")

    # Gerar gráfico sob demanda
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

    grafico_url = filepath
    return render_template('index.html', grafico_url=grafico_url)

if __name__ == '__main__':
    app.run(debug=True, port=8080)