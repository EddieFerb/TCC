# tratar_dados.py
# Script responsável pelo carregamento, limpeza, tratamento, cálculo de taxas e consolidação de dados educacionais extraídos dos microdados do INEP/MEC.

import os
import pandas as pd
from pathlib import Path
import re
import glob
import numpy as np

# Defina a variável global para a pasta processada
PASTA_PROCESSADO = "./dados/processado"

def carregar_dados(caminho_entrada):
    try:
        print(f"Carregando dados de: {caminho_entrada}")
        df = pd.read_csv(caminho_entrada, sep=';', encoding='utf-8', low_memory=False)
        print("Colunas disponíveis:", df.columns.tolist())
        return df
    except Exception as e:
        raise ValueError(f"Erro ao carregar os dados: {e}")

def tratar_dados(df, colunas_numericas=None):
    df = df.drop_duplicates()
    df = df.dropna()

    if colunas_numericas:
        for col in colunas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        for col in ['ingressantes', 'concluintes', 'vagas_totais', 'matriculados', 'numero_cursos']:
            if col in df.columns:
                df = df[df[col] >= 0]

        if 'ingressantes' in df.columns:
            df = df[df['ingressantes'] > 0]

        df = df.dropna()

    return df

def salvar_dados_tratados(df, caminho_saida):
    try:
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        df.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8')
        print(f"Dados tratados salvos em: {caminho_saida}")
    except Exception as e:
        raise ValueError(f"Erro ao salvar os dados: {e}")

def pivotar_dados_cursos():
    arquivos = sorted(Path("./dados/processado").glob("dados_cursos_tratado_*.csv"))
    dfs = []
    for arq in arquivos:
        ano_match = re.search(r"(\d{4})", arq.name)
        if not ano_match:
            continue
        ano = int(ano_match.group(1))
        df = pd.read_csv(arq, sep=';', encoding='utf-8')
        df['ano'] = ano
        dfs.append(df)

    if not dfs:
        return

    df_geral = pd.concat(dfs, ignore_index=True)

    id_cols = ["id_curso", "nome_curso", "modalidade_ensino", "id_ies"]
    id_cols = [col for col in id_cols if col in df_geral.columns]

    df_pivot = pd.DataFrame()
    for var in ["ingressantes", "concluintes", "matriculados", "vagas_totais", "inscritos_totais"]:
        if var in df_geral.columns:
            tabela = df_geral.pivot_table(index=id_cols, columns="ano", values=var)
            tabela.columns = [f"{var}_{int(col)}" for col in tabela.columns]
            df_pivot = pd.concat([df_pivot, tabela], axis=1)

    df_final = df_geral[id_cols].drop_duplicates().set_index(id_cols)
    df_final = df_final.join(df_pivot).reset_index()

    salvar_dados_tratados(df_final, "./dados/processado/dados_cursos_serie_temporal.csv")

def calcular_taxas(df):
    df = df.copy()
    for coluna in ['ingressantes', 'concluintes', 'vagas_totais']:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')

    df = df[(df['ingressantes'] > 0) & (df['vagas_totais'] > 0)]
    df['taxa_ingresso'] = df['ingressantes'] / df['vagas_totais']
    df['taxa_conclusao'] = df['concluintes'] / df['ingressantes']
    df['taxa_evasao'] = 1 - df['taxa_conclusao']

    for col in ['taxa_ingresso', 'taxa_conclusao', 'taxa_evasao']:
        df = df[(df[col] >= 0) & (df[col] <= 1)]

    return df

def salvar_taxas_consolidadas():
    pattern = os.path.join(PASTA_PROCESSADO, "dados_cursos_tratado_*.csv")
    files = glob.glob(pattern)
    if not files:
        print("Nenhum arquivo de cursos tratado foi encontrado para consolidar.")
        return
    list_df = []
    for f in files:
        try:
            df_temp = pd.read_csv(f, sep=";", encoding="utf-8")
            list_df.append(df_temp)
        except Exception as e:
            print(f"Erro ao ler o arquivo {f}: {e}")
    if not list_df:
        print("Nenhum dado foi carregado para consolidação.")
        return
    df_consolidado = pd.concat(list_df, ignore_index=True)
    df_consolidado = calcular_taxas(df_consolidado)
    caminho_saida = os.path.join(PASTA_PROCESSADO, "dados_ingresso_evasao_conclusao.csv")
    salvar_dados_tratados(df_consolidado, caminho_saida)
    print(f"[OK] Dados consolidados e taxas salvos em: {caminho_saida}")

def ler_taxas_consolidadas():
    caminho = os.path.join(PASTA_PROCESSADO, "dados_ingresso_evasao_conclusao.csv")
    try:
        df = pd.read_csv(caminho, sep=";", encoding="utf-8")
        print("Dados consolidados lidos com sucesso.")
        return df
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo de taxas consolidadas: {e}")

def main(year: int = 2024):
    caminho_ies = f'./dados/processado/dados_ies_{year}.csv'
    caminho_cursos = f'./dados/processado/dados_cursos_{year}.csv'

    caminho_ies_tratado = f'./dados/intermediario/dados_ies_tratado_{year}.csv'
    caminho_cursos_tratado = f'./dados/intermediario/dados_cursos_tratado_{year}.csv'

    caminho_ies_final = f'./dados/processado/dados_ies_tratado_{year}.csv'
    caminho_cursos_final = f'./dados/processado/dados_cursos_tratado_{year}.csv'

    colunas_numericas_ies = [
        'docentes_total',
        'docentes_exercicio',
        'docentes_feminino',
        'docentes_masculino'
    ]
    colunas_numericas_cursos = [
        'numero_cursos',
        'vagas_totais',
        'inscritos_totais',
        'ingressantes',
        'matriculados',
        'concluintes'
    ]

    try:
        df_ies = carregar_dados(caminho_ies)
    except ValueError as e:
        print(e)
        df_ies = pd.DataFrame()

    if not df_ies.empty:
        try:
            df_ies_tratado = tratar_dados(df_ies, colunas_numericas=colunas_numericas_ies)
            salvar_dados_tratados(df_ies_tratado, caminho_ies_tratado)
            salvar_dados_tratados(df_ies_tratado, caminho_ies_final)
        except ValueError as e:
            print(f"Erro ao processar dados de IES: {e}")
    else:
        print("Nenhum dado de IES disponível para tratar.")

    try:
        df_cursos = carregar_dados(caminho_cursos)
    except ValueError as e:
        print(e)
        df_cursos = pd.DataFrame()

    if not df_cursos.empty:
        try:
            df_cursos_tratado = tratar_dados(df_cursos, colunas_numericas=colunas_numericas_cursos)
            salvar_dados_tratados(df_cursos_tratado, caminho_cursos_tratado)
            salvar_dados_tratados(df_cursos_tratado, caminho_cursos_final)
        except ValueError as e:
            print(f"Ano de {year} Erro ao processar dados de Cursos: {e}")
    else:
        print("Nenhum dado de Cursos disponível para tratar.")

if __name__ == '__main__':
    for year in range(2024):
        print(f"\tProcessing year {year} ...")
        main(year)

    pivotar_dados_cursos()
    salvar_taxas_consolidadas()
    df_taxas = ler_taxas_consolidadas()
    print(df_taxas.head())

