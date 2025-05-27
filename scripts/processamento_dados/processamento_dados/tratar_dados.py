<<<<<<< HEAD
=======
# tratar_dados.py
# Script responsável pelo carregamento, limpeza, tratamento, cálculo de taxas e consolidação de dados educacionais extraídos dos microdados do INEP/MEC.

>>>>>>> testing_and_validation
import os
import pandas as pd
from pathlib import Path
import re
<<<<<<< HEAD

def carregar_dados(caminho_entrada):
    """
    Carrega os dados de um arquivo CSV.
    """
=======
import glob
import numpy as np

# Defina a variável global para a pasta processada
PASTA_PROCESSADO = "./dados/processado"

def carregar_dados(caminho_entrada):
>>>>>>> testing_and_validation
    try:
        print(f"Carregando dados de: {caminho_entrada}")
        df = pd.read_csv(caminho_entrada, sep=';', encoding='utf-8', low_memory=False)
        print("Colunas disponíveis:", df.columns.tolist())
        return df
    except Exception as e:
        raise ValueError(f"Erro ao carregar os dados: {e}")

def tratar_dados(df, colunas_numericas=None):
<<<<<<< HEAD
    """
    Realiza a limpeza e o tratamento de dados no DataFrame.
      - Remove duplicatas
      - Descarta valores ausentes
      - Converte colunas numéricas (se fornecidas) para tipo numérico
      - Novamente remove eventuais linhas que fiquem inválidas
      - (Nesta versão, não faz filtragem por colunas específicas, pois os dados já foram pré-processados)
    """
    # Remove duplicatas
    df = df.drop_duplicates()

    # Descartar valores ausentes
    df = df.dropna()

    # Se houver colunas numéricas definidas, converter para tipo numérico
=======
    df = df.drop_duplicates()
    df = df.dropna()

>>>>>>> testing_and_validation
    if colunas_numericas:
        for col in colunas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
<<<<<<< HEAD
        # E descartar possíveis NaNs novamente
=======

        for col in ['ingressantes', 'concluintes', 'vagas_totais', 'matriculados', 'numero_cursos']:
            if col in df.columns:
                df = df[df[col] >= 0]

        if 'ingressantes' in df.columns:
            df = df[df['ingressantes'] > 0]

>>>>>>> testing_and_validation
        df = df.dropna()

    return df

def salvar_dados_tratados(df, caminho_saida):
<<<<<<< HEAD
    """
    Salva o DataFrame tratado em um novo arquivo CSV.
    """
=======
>>>>>>> testing_and_validation
    try:
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        df.to_csv(caminho_saida, index=False, sep=';', encoding='utf-8')
        print(f"Dados tratados salvos em: {caminho_saida}")
    except Exception as e:
        raise ValueError(f"Erro ao salvar os dados: {e}")

def pivotar_dados_cursos():
<<<<<<< HEAD
    """
    Consolida os dados de cursos tratados e os pivota por ano para análise agregada.
    """
    arquivos = sorted(Path("./dados/processado").glob("dados_cursos_tratado_*.csv"))
    dfs = []
    for arq in arquivos:
        ano_match = re.search(r"(\\d{4})", arq.name)
=======
    arquivos = sorted(Path("./dados/processado").glob("dados_cursos_tratado_*.csv"))
    dfs = []
    for arq in arquivos:
        ano_match = re.search(r"(\d{4})", arq.name)
>>>>>>> testing_and_validation
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

<<<<<<< HEAD
def main(year: int = 2024):
    """
    Faz a leitura dos arquivos já pré-processados (dados_ies.csv e dados_cursos.csv),
    aplica limpeza mínima e salva em formato 'tratado' em pastas adequadas.
    """
    # Definição de caminhos (ajuste conforme necessário)
    caminho_ies = f'./dados/processado/dados_ies_{year}.csv'
    caminho_cursos = f'./dados/processado/dados_cursos_{year}.csv'

    # Saídas
=======
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

>>>>>>> testing_and_validation
    caminho_ies_tratado = f'./dados/intermediario/dados_ies_tratado_{year}.csv'
    caminho_cursos_tratado = f'./dados/intermediario/dados_cursos_tratado_{year}.csv'

    caminho_ies_final = f'./dados/processado/dados_ies_tratado_{year}.csv'
    caminho_cursos_final = f'./dados/processado/dados_cursos_tratado_{year}.csv'

<<<<<<< HEAD
    # Exemplo de colunas numéricas, se quiser converter:
    # Para IES (docentes)
=======
>>>>>>> testing_and_validation
    colunas_numericas_ies = [
        'docentes_total',
        'docentes_exercicio',
        'docentes_feminino',
        'docentes_masculino'
    ]
<<<<<<< HEAD
    # Para Cursos (ingressantes, matriculados etc.)
=======
>>>>>>> testing_and_validation
    colunas_numericas_cursos = [
        'numero_cursos',
        'vagas_totais',
        'inscritos_totais',
        'ingressantes',
        'matriculados',
        'concluintes'
    ]

<<<<<<< HEAD
    # 1) Processar e tratar IES
=======
>>>>>>> testing_and_validation
    try:
        df_ies = carregar_dados(caminho_ies)
    except ValueError as e:
        print(e)
        df_ies = pd.DataFrame()

    if not df_ies.empty:
        try:
            df_ies_tratado = tratar_dados(df_ies, colunas_numericas=colunas_numericas_ies)
<<<<<<< HEAD
            # Salvar intermediário
            salvar_dados_tratados(df_ies_tratado, caminho_ies_tratado)
            # Salvar final
=======
            salvar_dados_tratados(df_ies_tratado, caminho_ies_tratado)
>>>>>>> testing_and_validation
            salvar_dados_tratados(df_ies_tratado, caminho_ies_final)
        except ValueError as e:
            print(f"Erro ao processar dados de IES: {e}")
    else:
        print("Nenhum dado de IES disponível para tratar.")

<<<<<<< HEAD
    # 2) Processar e tratar Cursos
=======
>>>>>>> testing_and_validation
    try:
        df_cursos = carregar_dados(caminho_cursos)
    except ValueError as e:
        print(e)
        df_cursos = pd.DataFrame()

    if not df_cursos.empty:
        try:
            df_cursos_tratado = tratar_dados(df_cursos, colunas_numericas=colunas_numericas_cursos)
<<<<<<< HEAD
            # Salvar intermediário
            salvar_dados_tratados(df_cursos_tratado, caminho_cursos_tratado)
            # Salvar final
=======
            salvar_dados_tratados(df_cursos_tratado, caminho_cursos_tratado)
>>>>>>> testing_and_validation
            salvar_dados_tratados(df_cursos_tratado, caminho_cursos_final)
        except ValueError as e:
            print(f"Ano de {year} Erro ao processar dados de Cursos: {e}")
    else:
        print("Nenhum dado de Cursos disponível para tratar.")

if __name__ == '__main__':
    for year in range(2024):
        print(f"\tProcessing year {year} ...")
        main(year)

<<<<<<< HEAD
    # Pivotar dados de cursos ao final do processamento
    pivotar_dados_cursos()
=======
    pivotar_dados_cursos()
    salvar_taxas_consolidadas()
    df_taxas = ler_taxas_consolidadas()
    print(df_taxas.head())

>>>>>>> testing_and_validation
