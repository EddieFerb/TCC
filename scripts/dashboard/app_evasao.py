# app_evasao.py
# Dashboard interativo com análise de evasão usando Streamlit

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, '..', '..', 'dados', 'processado', 'dados_ingresso_evasao_conclusao.csv')
df = pd.read_csv(csv_path, sep=';')

st.set_page_config(page_title="Dashboard Evasão IES", layout="wide")

# Título
st.title("📊 Dashboard - Taxas de Ingresso, Conclusão e Evasão")

# Filtro por curso
cursos = df['nome_curso'].unique()
curso_selecionado = st.selectbox("Selecione um curso:", sorted(cursos))

# Filtrar
df_filtrado = df[df['nome_curso'] == curso_selecionado]

# Métricas rápidas
col1, col2, col3 = st.columns(3)
col1.metric("Taxa de Ingresso (média)", f"{df_filtrado['taxa_ingresso'].mean():.2f}")
col2.metric("Taxa de Conclusão (média)", f"{df_filtrado['taxa_conclusao'].mean():.2f}")
col3.metric("Taxa de Evasão (média)", f"{df_filtrado['taxa_evasao'].mean():.2f}")

# Gráfico de linha
st.subheader("📈 Evolução das Taxas")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=df_filtrado[['taxa_ingresso', 'taxa_conclusao', 'taxa_evasao']])
st.pyplot(fig)

# Salvar gráfico como imagem PNG
output_dir = os.path.join(BASE_DIR, '..', '..', 'acessibilidade_web', 'graficos')
os.makedirs(output_dir, exist_ok=True)
fig.savefig(os.path.join(output_dir, 'grafico_taxas.png'))