# Script: analises.py
# Objetivo: Analisar dados de cursos e calcular/visualizar as taxas de conclusão e evasão por curso e ano

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from glob import glob

# Define o mapeamento de cores: verde para "Taxa de Conclusão" e vermelho para "Taxa de Evasão"
color_map = {"Taxa de Conclusão": "green", "Taxa de Evasão": "red"}

# =============================================================================
# Leitura dos dados de cursos para os anos de 2009 a 2023
# =============================================================================
anos = range(2009, 2024)
lista_cursos = []

# Lista de colunas que devem ser numéricas
numeric_cols = ["numero_cursos", "vagas_totais", "ingressantes", "concluintes", "inscritos_totais"]

for ano in anos:
    caminho = f"dados/processado/dados_cursos_tratado_{ano}.csv"
    if os.path.exists(caminho):
        df = pd.read_csv(caminho, sep=";", dtype=str)  # Ler tudo inicialmente como string
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        df["ano"] = ano
        lista_cursos.append(df)
    else:
        print(f"Arquivo não encontrado: {caminho}")

dados_cursos_tratado = pd.concat(lista_cursos, ignore_index=True)

# =============================================================================
# Leitura dos dados de universidades (IES) – utilizando a base do ano 2023
# =============================================================================
ies_path = "dados/processado/dados_ies_tratado_2023.csv"
dados_ies_tratado = pd.read_csv(ies_path, sep=";", dtype=str)

# =============================================================================
# Unindo os dados de cursos e universidades
# =============================================================================
all_data = pd.merge(dados_cursos_tratado, dados_ies_tratado, on="id_ies", how="left")
all_data = all_data[(all_data["numero_cursos"].astype(float) > 0) & (all_data["nome_ies"].notnull())]
all_data["nome_curso"] = all_data["nome_curso"].str.upper()
all_data["nome_ies"] = all_data["nome_ies"].str.upper()

for col in ["concluintes", "ingressantes", "inscritos_totais", "vagas_totais"]:
    if col in all_data.columns:
        all_data[col] = all_data[col].astype("Int64")

# Removemos a variável 'tipo_rede' pois só aparece explicitamente a partir de 2023
all_data["cat_adm"] = all_data["cat_adm"].replace({"1": "Federal", "2": "Estadual"}).fillna("Outro")
all_data["modalidade_ensino"] = all_data["modalidade_ensino"].replace({"1": "Presencial", "2": "EAD"}).fillna("Outro")

# =============================================================================
# Agrupamento e pivot dos dados para calcular taxas de conclusão e evasão
# =============================================================================
ingress = (all_data[["nome_curso", "modalidade_ensino", "ingressantes", "ano", "concluintes"]]
           .groupby(["nome_curso", "modalidade_ensino", "ano"], as_index=False)
           .agg({"ingressantes": "sum", "concluintes": "sum"}))

# Pivotar os dados para 'ingressantes' e 'concluintes'
pivot_ing = ingress.pivot_table(index=["nome_curso", "modalidade_ensino"], columns="ano", values="ingressantes")
pivot_con = ingress.pivot_table(index=["nome_curso", "modalidade_ensino"], columns="ano", values="concluintes")

# Renomeia as colunas com o padrão "ingressantes_{ano}" e "concluintes_{ano}"
pivot_ing.columns = [f"ingressantes_{ano}" for ano in pivot_ing.columns]
pivot_con.columns = [f"concluintes_{ano}" for ano in pivot_con.columns]

ingress_wide = pivot_ing.join(pivot_con).reset_index()

# Filtra somente os cursos de interesse
cursos_interesse = ["ENGENHARIA CIVIL", "MEDICINA", "DIREITO", "ADMINISTRAÇÃO"]
ingress_wide = ingress_wide[ingress_wide["nome_curso"].isin(cursos_interesse)]

# =============================================================================
# Cálculo das taxas de conclusão e evasão por curso
# =============================================================================
# Fórmulas:
#   Taxa de Conclusão = concluintes_{ano} / ingressantes_{ano - D}
#   Taxa de Evasão = 1 - Taxa de Conclusão
duracoes = {
    "ENGENHARIA CIVIL": 5,
    "MEDICINA": 6,
    "DIREITO": 5,
    "ADMINISTRAÇÃO": 4
}

def calcular_metricas(df, curso, duracao):
    df_course = df[df["nome_curso"] == curso].copy()
    for ano in range(2009 + duracao, 2024):
        col_ing = f"ingressantes_{ano - duracao}"
        col_con = f"concluintes_{ano}"
        col_conclusao = f"taxa_conclusao_{ano}"
        col_evasao = f"taxa_evasao_{ano}"
        if col_ing in df_course.columns and col_con in df_course.columns:
            # Evitar divisão por zero e valores não definidos:
            df_course[col_conclusao] = df_course[col_con] / df_course[col_ing]
            df_course[col_evasao] = 1 - df_course[col_conclusao]
        else:
            df_course[col_conclusao] = np.nan
            df_course[col_evasao] = np.nan
    return df_course

df_eng = calcular_metricas(ingress_wide, "ENGENHARIA CIVIL", duracoes["ENGENHARIA CIVIL"])
df_dir = calcular_metricas(ingress_wide, "DIREITO", duracoes["DIREITO"])
df_med = calcular_metricas(ingress_wide, "MEDICINA", duracoes["MEDICINA"])
df_adm = calcular_metricas(ingress_wide, "ADMINISTRAÇÃO", duracoes["ADMINISTRAÇÃO"])

# Função para converter data frame wide em long para um dado prefixo e rótulo
def pivot_long_metric(df, prefix, label):
    metric_cols = [col for col in df.columns if col.startswith(prefix)]
    df_long = df.melt(id_vars=["nome_curso", "modalidade_ensino"],
                      value_vars=metric_cols,
                      var_name="ano", value_name="taxa")
    df_long["ano"] = df_long["ano"].str.extract(r"(\d{4})")
    df_long["tipo"] = label
    return df_long

# Criando data frames long para cada curso e para cada métrica
eng_long_conclusao = pivot_long_metric(df_eng, "taxa_conclusao_", "Taxa de Conclusão")
eng_long_evasao = pivot_long_metric(df_eng, "taxa_evasao_", "Taxa de Evasão")
eng_civil_long = pd.concat([eng_long_conclusao, eng_long_evasao])

dir_long_conclusao = pivot_long_metric(df_dir, "taxa_conclusao_", "Taxa de Conclusão")
dir_long_evasao = pivot_long_metric(df_dir, "taxa_evasao_", "Taxa de Evasão")
direito_long = pd.concat([dir_long_conclusao, dir_long_evasao])

med_long_conclusao = pivot_long_metric(df_med, "taxa_conclusao_", "Taxa de Conclusão")
med_long_evasao = pivot_long_metric(df_med, "taxa_evasao_", "Taxa de Evasão")
medicina_long = pd.concat([med_long_conclusao, med_long_evasao])

adm_long_conclusao = pivot_long_metric(df_adm, "taxa_conclusao_", "Taxa de Conclusão")
adm_long_evasao = pivot_long_metric(df_adm, "taxa_evasao_", "Taxa de Evasão")
administracao_long = pd.concat([adm_long_conclusao, adm_long_evasao])

# =============================================================================
# Plotagem com Plotly – duas linhas: uma para "Taxa de Conclusão" (verde) e outra para "Taxa de Evasão" (vermelha)
# =============================================================================
def plot_taxa(df_long, curso):
    fig = px.line(
        df_long,
        x="ano",
        y="taxa",
        color="tipo",
        markers=True,
        title=f"Taxa de Evasão e Conclusão ao longo dos anos - Curso de {curso}",
        labels={"ano": "Ano de Ingresso", "taxa": "Taxa"},
        color_discrete_map=color_map
    )
    fig.update_yaxes(tickformat=".0%")
    fig.update_layout(legend=dict(orientation="v", title=dict(text="Métrica")))
    fig.show()

plot_taxa(eng_civil_long, "Engenharia Civil")
plot_taxa(direito_long, "Direito")
plot_taxa(medicina_long, "Medicina")
plot_taxa(administracao_long, "Administração")

# =============================================================================
# Exportação dos dados processados
# =============================================================================
ingress_wide.to_csv("dados/processado/final_ingressantes.csv", index=False, sep=";")
df_eng.to_csv("dados/processado/final_eng_civil.csv", index=False, sep=";")
df_dir.to_csv("dados/processado/final_direito.csv", index=False, sep=";")
df_med.to_csv("dados/processado/final_medicina.csv", index=False, sep=";")
df_adm.to_csv("dados/processado/final_administracao.csv", index=False, sep=";")
