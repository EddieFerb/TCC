# import os
# import pandas as pd
# import unicodedata
# import re
# from io import StringIO

# # ==========================================================================
# # CONFIGURAÇÕES GERAIS
# # ==========================================================================

# # Diretórios de entrada e saída (ajuste conforme sua estrutura)
# PASTA_BRUTO = "./dados/bruto"
# PASTA_PROCESSADO = "./dados/processado"

# # ==========================================================================
# # COLUNAS DE INTERESSE E MAPEAMENTOS
# # ==========================================================================

# # Exemplo de colunas relevantes para a base de IES, conforme dicionário do Censo 2023.
# COLUNAS_IES_RELEVANTES = [
#     "CO_IES",
#     "NO_IES",
#     # "TP_REDE",
#     "TP_CATEGORIA_ADMINISTRATIVA",
#     "QT_DOC_TOTAL",
#     "QT_DOC_EXE",
#     "QT_DOC_EX_FEMI",
#     "QT_DOC_EX_MASC"
#     # Adicione outras colunas se precisar (p. ex. QT_TEC_TOTAL, etc.)
# ]

# MAPPING_IES = {
#     "CO_IES": "id_ies",
#     "NO_IES": "nome_ies",
#     # "TP_REDE": "tipo_rede",     # 1 = pública, 2 = privada
#     "TP_CATEGORIA_ADMINISTRATIVA": "cat_adm",   # 1 = Fed, 2 = Est, etc.
#     "QT_DOC_TOTAL": "docentes_total",
#     "QT_DOC_EXE": "docentes_exercicio",
#     "QT_DOC_EX_FEMI": "docentes_feminino",
#     "QT_DOC_EX_MASC": "docentes_masculino"
# }

# # Exemplo de colunas relevantes para a base de Cursos, conforme dicionário do Censo 2023.
# COLUNAS_CURSOS_RELEVANTES = [
#     "CO_IES",
#     "CO_CURSO",
#     "NO_CURSO",
#     "TP_MODALIDADE_ENSINO",
#     "QT_CURSO",
#     "QT_VG_TOTAL",
#     "QT_INSCRITO_TOTAL",
#     "QT_ING",
#     "QT_MAT",
#     "QT_CONC",
#     "QT_DIPLOMADOS",
#     "QT_DIPLO"
#     # de 1995 a 2008 os concluíntes eram chamados de diplomados. Adicione outras colunas se quiser (e.g. QT_ING_FEM, QT_MAT_18_24, etc.)
# ]

# MAPPING_CURSOS = {
#     "CO_IES": "id_ies",
#     "CO_CURSO": "id_curso",
#     "NO_CURSO": "nome_curso",
#     "TP_MODALIDADE_ENSINO": "modalidade_ensino",    # 1=Presencial, 2=EAD
#     "QT_CURSO": "numero_cursos",
#     "QT_VG_TOTAL": "vagas_totais",
#     "QT_INSCRITO_TOTAL": "inscritos_totais",
#     "QT_ING": "ingressantes",
#     "QT_MAT": "matriculados",
#     "QT_CONC": "concluintes",
#     "QT_DIPLOMADOS": "concluintes",
#     "QT_DIPLO": "concluintes"
# }

# # # Os mapeamentos específicos para determinados anos (1995, 2000, 2008) são definidos
# # # como cópias do mapeamento geral para permitir, futuramente, ajustes pontuais nesses períodos.
# # MAPPING_IES_1995 = MAPPING_IES.copy()
# # COLUNAS_IES_RELEVANTES_1995 = COLUNAS_IES_RELEVANTES.copy()

# # MAPPING_CURSOS_1995 = MAPPING_CURSOS.copy()
# # COLUNAS_CURSOS_RELEVANTES_1995 = COLUNAS_CURSOS_RELEVANTES.copy()

# # MAPPING_IES_2000 = MAPPING_IES.copy()
# # COLUNAS_IES_RELEVANTES_2000 = COLUNAS_IES_RELEVANTES.copy()

# # MAPPING_CURSOS_2000 = MAPPING_CURSOS.copy()
# # COLUNAS_CURSOS_RELEVANTES_2000 = COLUNAS_CURSOS_RELEVANTES.copy()

# # MAPPING_IES_2008 = MAPPING_IES.copy()
# # COLUNAS_IES_RELEVANTES_2008 = COLUNAS_IES_RELEVANTES.copy()
# # MAPPING_CURSOS_2008 = MAPPING_CURSOS.copy()
# # COLUNAS_CURSOS_RELEVANTES_2008 = COLUNAS_CURSOS_RELEVANTES.copy()

# # ==========================================================================
# # FUNÇÕES DE APOIO
# # ==========================================================================

# def normalizar_conteudo_pipe(conteudo):
#     """
#     Remove repetições de delimitadores, espaços desnecessários e caracteres indesejados
#     para uniformizar o uso do pipe ("|") como delimitador.
#     """
#     conteudo = re.sub(r"\|{2,}", "|", conteudo)
#     conteudo = re.sub(r'\s*\|\s*', '|', conteudo)
#     conteudo = conteudo.replace('\r\n', '\n').replace('\r', '\n')
#     conteudo = conteudo.replace('"', '')
#     return conteudo

# def registrar_problemas(arquivo, erro):
#     """
#     Registra problemas de leitura em um log.
#     """
#     with open("log_erros.txt", "a", encoding="utf-8") as log:
#         log.write(f"Arquivo: {arquivo}, Erro: {erro}\n")

# def carregar_csv(caminho_arquivo, sep=";", encoding="latin1", year=None):
#     """
#     Carrega um CSV, tratando parsing e erros.
#     Carrega um arquivo CSV a partir de um caminho, tratando a normalização dos delimitadores.
    
#     Se o ano for menor ou igual a 2008 e o conteúdo apresentar o delimitador "|", tenta
#     normalizar repetições de delimitadores (por exemplo, '||' ou '|||') para que os dados sejam 
#     lidos corretamente. Se mesmo assim o DataFrame resultar em apenas uma coluna, poderá ser necessário
#     separar manualmente essa coluna.
#     """
#     try:
#         print(f"Lendo arquivo: {caminho_arquivo}")
#         with open(caminho_arquivo, encoding=encoding) as f:
#             conteudo = f.read()

#         if year is not None and year <= 2008 and "|" in conteudo:
#             print(f"⚠️ Detecção de separadores múltiplos para ano {year}. Normalizando...")
#             conteudo = normalizar_conteudo_pipe(conteudo)
#             df = pd.read_csv(StringIO(conteudo), sep="|", header=0, engine="python", on_bad_lines='skip')
#             if df.shape[1] == 1:
#                 # Se restar somente uma coluna, tenta separar manualmente essa coluna usando o delimitador "|"
#                 print("⚠️ Apenas uma coluna detectada após normalização. Tentando separar manualmente...")
#                 df = df.iloc[:, 0].str.split("|", expand=True)
#                 # Assume-se que a primeira linha são os cabeçalhos
#                 df.columns = df.iloc[0]
#                 df = df[1:]
#             return df
#         else:
#             return pd.read_csv(StringIO(conteudo), sep=sep, header=0, engine="python", on_bad_lines='skip')
#     except Exception as e:
#         print(f"Erro ao carregar {caminho_arquivo}: {e}")
#         registrar_problemas(caminho_arquivo, e)
#         return pd.DataFrame()

# def filtrar_renomear(df, colunas_relevantes, mapping):
#     """
#     Seleciona apenas as colunas relevantes contidas no DataFrame e as renomeia conforme
#     o dicionário de mapeamento fornecido.
#     """
#     # Identifica somente colunas que existam no df
#     existentes = [c for c in colunas_relevantes if c in df.columns]
#     df_filtrado = df[existentes].copy()
#         # Renomeia 
#     return df_filtrado.rename(columns=mapping)

# def corrigir_nome_pasta(caminho_base, ano):
#     """
#     Corrige possíveis problemas com caracteres especiais nos nomes das pastas extraídas,
#     retornando o caminho completo da pasta que contenha a string "microdados".
#     """
#     caminho_esperado = os.path.join(caminho_base, f"INEP_{ano}-MICRODADOS-CENSO")
#     if os.path.exists(caminho_esperado):
#         for pasta in os.listdir(caminho_esperado):
#             pasta_corrigida = unicodedata.normalize("NFKD", pasta).encode("ASCII", "ignore").decode("ASCII")
#             pasta_corrigida = re.sub(r'[^a-zA-Z0-9_\- ]', '', pasta_corrigida)
#             if "microdados" in pasta_corrigida.lower():
#                 return os.path.join(caminho_esperado, pasta)
#     print(f"Aviso: Nenhuma pasta de microdados encontrada para {ano}")
#     return None

# def corrigir_nome_arquivo(nome_arquivo):
#     """
#     Corrige caracteres especiais no nome dos arquivos, removendo aqueles inválidos.
#     """
#     return re.sub(r'[^a-zA-Z0-9_\-\. ]', '', nome_arquivo)

# # ==========================================================================
# # PROCESSAMENTO PRINCIPAL
# # ==========================================================================

# def main(year: int = 2024):
#     arquivos_disponiveis = []
#     caminho_base_ano = corrigir_nome_pasta(PASTA_BRUTO, year)
#     caminho_dados = os.path.join(caminho_base_ano, "dados")

#     if os.path.isdir(caminho_dados):
#         arquivos_disponiveis = os.listdir(caminho_dados)

#     if year < 2009:
#         # Renomeia arquivos com padrões diferentes de nomenclatura para padronizá-los
#         for arq in arquivos_disponiveis:
#             if "INSTITUICAO" in arq.upper():
#                 os.rename(
#                     os.path.join(caminho_dados, arq),
#                     os.path.join(caminho_dados, f"MICRODADOS_ED_SUP_IES_{year}.CSV")
#                 )
#             elif "GRADUACAO_PRESENCIAL" in arq.upper():
#                 os.rename(
#                     os.path.join(caminho_dados, arq),
#                     os.path.join(caminho_dados, f"MICRODADOS_CADASTRO_CURSOS_{year}.CSV")
#                 )
#         arquivos_disponiveis = os.listdir(caminho_dados)

#     ARQUIVO_IES = f"MICRODADOS_ED_SUP_IES_{year}.CSV"
#     ARQUIVO_CURSOS = f"MICRODADOS_CADASTRO_CURSOS_{year}.CSV"

#     caminho_ies = None
#     for arquivo in arquivos_disponiveis:
#         nome_normalizado = corrigir_nome_arquivo(arquivo).upper()
#         if nome_normalizado.startswith(f"MICRODADOS_ED_SUP_IES_{year}") and nome_normalizado.endswith(".CSV"):
#             caminho_ies = os.path.join(caminho_dados, arquivo)
#             break

#     # Fallback para nome padrão, se não encontrar com sufixo
#     if caminho_ies is None:
#         caminho_ies = os.path.join(caminho_dados, f"MICRODADOS_ED_SUP_IES_{year}.CSV")

#     print(f"Arquivos encontrados em {caminho_dados}: {arquivos_disponiveis}")
#     print(f"Arquivo IES esperado: {ARQUIVO_IES}")
#     print(f"Arquivo IES identificado: {caminho_ies if os.path.exists(caminho_ies) else 'NÃO ENCONTRADO'}")

#     df_ies_final = pd.DataFrame()
#     df_cursos_final = pd.DataFrame()

#     # ----------------------------------------------------------------------
#     # Carregar e processar MICRODADOS_ED_SUP_IES_{year}.CSV
#     # ----------------------------------------------------------------------
#     if os.path.isfile(caminho_ies):
#         df_ies = carregar_csv(caminho_ies, year=year)
#         if not df_ies.empty:
#             df_ies_final = filtrar_renomear(df_ies, COLUNAS_IES_RELEVANTES, MAPPING_IES)
#         else:
#             print(f"Aviso: {ARQUIVO_IES} está vazio ou não pôde ser processado.")
#     else:
#         print(f"Aviso: Arquivo {ARQUIVO_IES} não encontrado em {caminho_ies}.")

#     # ----------------------------------------------------------------------
#     # Carregar e processar MICRODADOS_CADASTRO_CURSOS_{year}.CSV
#     # ----------------------------------------------------------------------
#     caminho_cursos = os.path.join(caminho_dados, corrigir_nome_arquivo(ARQUIVO_CURSOS))
#     if os.path.isfile(caminho_cursos):
#         df_cursos = carregar_csv(caminho_cursos, year=year)
#         if not df_cursos.empty:
#             df_cursos_final = filtrar_renomear(df_cursos, COLUNAS_CURSOS_RELEVANTES, MAPPING_CURSOS)
#         else:
#             print(f"Aviso: {ARQUIVO_CURSOS} está vazio ou não pôde ser processado.")
#     else:
#         print(f"Aviso: Arquivo {ARQUIVO_CURSOS} não encontrado em {caminho_cursos}.")

#     # ----------------------------------------------------------------------
#     # Salvando resultados (IES e Cursos) na pasta "processado"
#     # ----------------------------------------------------------------------
#     if not df_ies_final.empty:
#         saida_ies = os.path.join(PASTA_PROCESSADO, f"dados_ies_{year}.csv")
#         os.makedirs(os.path.dirname(saida_ies), exist_ok=True)
#         df_ies_final.to_csv(saida_ies, sep=";", index=False, encoding="utf-8")
#         print(f"[OK] dados_ies gerado em: {saida_ies}")
#     else:
#         print("Nenhum dado de IES para salvar.")

#     if not df_cursos_final.empty:
#         saida_cursos = os.path.join(PASTA_PROCESSADO, f"dados_cursos_{year}.csv")
#         os.makedirs(os.path.dirname(saida_cursos), exist_ok=True)
#         df_cursos_final.to_csv(saida_cursos, sep=";", index=False, encoding="utf-8")
#         print(f"[OK] dados_cursos gerado em: {saida_cursos}")
#     else:
#         print("Nenhum dado de Cursos para salvar.")

# if __name__ == "__main__":
#     # Processa todos os anos de 2009 a 2023.
#     for year in range(2009, 2024):
#         print(f"\tProcessing year {year} ...")
#         main(year)
import os
import pandas as pd
import unicodedata
import re
<<<<<<< Updated upstream
import numpy as np  # Import necessário para a conversão e para usar np.nan
=======
import numpy as np
>>>>>>> Stashed changes
from io import StringIO
import glob

# ==========================================================================
# CONFIGURAÇÕES GERAIS
# ==========================================================================

PASTA_BRUTO = "./dados/bruto"
PASTA_PROCESSADO = "./dados/processado"

# ==========================================================================
# COLUNAS DE INTERESSE E MAPEAMENTOS
# ==========================================================================

COLUNAS_IES_RELEVANTES = [
    "CO_IES",
    "NO_IES",
    "TP_CATEGORIA_ADMINISTRATIVA",
    "QT_DOC_TOTAL",
    "QT_DOC_EXE",
    "QT_DOC_EX_FEMI",
    "QT_DOC_EX_MASC"
]

MAPPING_IES = {
    "CO_IES": "id_ies",
    "NO_IES": "nome_ies",
<<<<<<< Updated upstream
    # "TP_REDE": "tipo_rede",  # comentado pois não está presente a partir de 2023
=======
>>>>>>> Stashed changes
    "TP_CATEGORIA_ADMINISTRATIVA": "cat_adm",
    "QT_DOC_TOTAL": "docentes_total",
    "QT_DOC_EXE": "docentes_exercicio",
    "QT_DOC_EX_FEMI": "docentes_feminino",
    "QT_DOC_EX_MASC": "docentes_masculino"
}

<<<<<<< Updated upstream
# Exemplo de colunas relevantes para a base de Cursos
=======
>>>>>>> Stashed changes
COLUNAS_CURSOS_RELEVANTES = [
    "CO_IES",
    "CO_CURSO",
    "NO_CURSO",
    "TP_MODALIDADE_ENSINO",
    "QT_CURSO",
    "QT_VG_TOTAL",
    "QT_INSCRITO_TOTAL",
    "QT_ING",
    "QT_MAT",
    "QT_CONC",
    "QT_DIPLOMADOS",
    "QT_DIPLO"
]

MAPPING_CURSOS = {
    "CO_IES": "id_ies",
    "CO_CURSO": "id_curso",
    "NO_CURSO": "nome_curso",
    "TP_MODALIDADE_ENSINO": "modalidade_ensino",  # 1 = Presencial, 2 = EAD
    "QT_CURSO": "numero_cursos",
    "QT_VG_TOTAL": "vagas_totais",
    "QT_INSCRITO_TOTAL": "inscritos_totais",
    "QT_ING": "ingressantes",
    "QT_MAT": "matriculados",
    "QT_CONC": "concluintes",
    "QT_DIPLOMADOS": "concluintes",
    "QT_DIPLO": "concluintes"
}

# ==========================================================================
# FUNÇÕES DE APOIO
# ==========================================================================

def normalizar_conteudo_pipe(conteudo):
    conteudo = re.sub(r"\|{2,}", "|", conteudo)
    conteudo = re.sub(r'\s*\|\s*', '|', conteudo)
    conteudo = conteudo.replace('\r\n', '\n').replace('\r', '\n')
    conteudo = conteudo.replace('"', '')
    return conteudo

def registrar_problemas(arquivo, erro):
    with open("log_erros.txt", "a", encoding="utf-8") as log:
        log.write(f"Arquivo: {arquivo}, Erro: {erro}\n")

def carregar_csv(caminho_arquivo, sep=";", encoding="latin1", year=None):
<<<<<<< Updated upstream
    """
    Carrega um CSV, tratando parsing e erros.
    """
=======
>>>>>>> Stashed changes
    try:
        print(f"Lendo arquivo: {caminho_arquivo}")
        with open(caminho_arquivo, encoding=encoding) as f:
            conteudo = f.read()
        if year is not None and year <= 2008 and "|" in conteudo:
            print(f"⚠️ Detecção de separadores múltiplos para ano {year}. Normalizando...")
            conteudo = normalizar_conteudo_pipe(conteudo)
            df = pd.read_csv(StringIO(conteudo), sep="|", header=0, engine="python", on_bad_lines='skip')
            if df.shape[1] == 1:
                print("⚠️ Apenas uma coluna detectada após normalização. Tentando separar manualmente...")
                df = df.iloc[:, 0].str.split("|", expand=True)
                df.columns = df.iloc[0]
                df = df[1:]
            return df
        else:
            return pd.read_csv(StringIO(conteudo), sep=sep, header=0, engine="python", on_bad_lines='skip')
    except Exception as e:
        print(f"Erro ao carregar {caminho_arquivo}: {e}")
        registrar_problemas(caminho_arquivo, e)
        return pd.DataFrame()

def filtrar_renomear(df, colunas_relevantes, mapping):
<<<<<<< Updated upstream
    """
    Seleciona apenas as colunas relevantes contidas no DataFrame e as renomeia conforme
    o dicionário de mapeamento fornecido.
    """
=======
>>>>>>> Stashed changes
    existentes = [c for c in colunas_relevantes if c in df.columns]
    df_filtrado = df[existentes].copy()
    return df_filtrado.rename(columns=mapping)

def corrigir_nome_pasta(caminho_base, ano):
    caminho_esperado = os.path.join(caminho_base, f"INEP_{ano}-MICRODADOS-CENSO")
    if os.path.exists(caminho_esperado):
        for pasta in os.listdir(caminho_esperado):
            pasta_corrigida = unicodedata.normalize("NFKD", pasta).encode("ASCII", "ignore").decode("ASCII")
            pasta_corrigida = re.sub(r'[^a-zA-Z0-9_\- ]', '', pasta_corrigida)
            if "microdados" in pasta_corrigida.lower():
                return os.path.join(caminho_esperado, pasta)
    print(f"Aviso: Nenhuma pasta de microdados encontrada para {ano}")
    return None

def corrigir_nome_arquivo(nome_arquivo):
    return re.sub(r'[^a-zA-Z0-9_\-\. ]', '', nome_arquivo)

def converter_tipos(df, colunas):
<<<<<<< Updated upstream
    """
    Converte as colunas especificadas para tipo numérico (usando pd.to_numeric com errors='coerce').
    """
=======
>>>>>>> Stashed changes
    for col in colunas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def tratar_continuidade(df, curso, duracao, start_year=2009, end_year=2024):
<<<<<<< Updated upstream
    """
    Garante a continuidade dos dados para o curso, garantindo que as colunas referentes aos anos críticos
    existam. Se faltar alguma coluna (como "ingressantes_XXXX" ou "concluintes_XXXX"), cria-a com np.nan.
    Pode ser aplicada sobre um DataFrame que já está no formato wide.
    """
    # Para cada ano crítico (para este curso), verifique as colunas esperadas:
=======
>>>>>>> Stashed changes
    for ano in range(start_year + duracao, end_year):
        col_ing = f"ingressantes_{ano - duracao}"
        col_con = f"concluintes_{ano}"
        if col_ing not in df.columns:
            df[col_ing] = np.nan
        else:
            df[col_ing] = pd.to_numeric(df[col_ing], errors='coerce')
        if col_con not in df.columns:
            df[col_con] = np.nan
        else:
            df[col_con] = pd.to_numeric(df[col_con], errors='coerce')
<<<<<<< Updated upstream
    # Aplicar interpolação linear se necessário:
=======
>>>>>>> Stashed changes
    col_list = [f"ingressantes_{year - duracao}" for year in range(start_year+duracao, end_year)] + \
               [f"concluintes_{year}" for year in range(start_year+duracao, end_year)]
    df[col_list] = df[col_list].apply(lambda row: row.interpolate(method='linear', limit_direction='both'), axis=1)
    return df

<<<<<<< Updated upstream
=======
# ==========================================================================
# FUNÇÃO NOVA: CÁLCULO E SALVAR TAXAS
# ==========================================================================

def calcular_taxas(df):
    """
    Calcula as taxas de ingresso, conclusão e evasão.
    Suponha que o DataFrame possua as seguintes colunas:
        - 'ingressantes': número de alunos que ingressaram
        - 'concluintes': número de alunos que concluíram
        - 'vagas_totais': número de vagas ofertadas (pode ser usado para taxa de ingresso)
    As taxas são calculadas como:
        - taxa_ingresso = ingressantes / vagas_totais
        - taxa_conclusao = concluintes / ingressantes
        - taxa_evasao = 1 - taxa_conclusao
    Caso haja divisão por zero, o resultado será NaN.
    """
    df = df.copy()
    for coluna in ['ingressantes', 'concluintes', 'vagas_totais']:
        if coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
    df['taxa_ingresso'] = df['ingressantes'] / df['vagas_totais'].replace(0, pd.NA)
    df['taxa_conclusao'] = df['concluintes'] / df['ingressantes'].replace(0, pd.NA)
    df['taxa_evasao'] = 1 - df['taxa_conclusao']
    return df

def salvar_taxas_consolidadas():
    """
    Consolida todos os arquivos de dados de cursos tratados (dados_cursos_tratado_*.csv)
    localizados na pasta de processados, calcula as taxas e salva o DataFrame resultante
    como 'dados_ingresso_evasao_conclusao.csv' na pasta dados/processado.
    """
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
    df_consolidado.to_csv(caminho_saida, sep=";", index=False, encoding="utf-8")
    print(f"[OK] Dados consolidados e taxas salvos em: {caminho_saida}")

>>>>>>> Stashed changes
# ==========================================================================
# PROCESSAMENTO PRINCIPAL
# ==========================================================================

def main(year: int = 2024):
    arquivos_disponiveis = []
    caminho_base_ano = corrigir_nome_pasta(PASTA_BRUTO, year)
    if caminho_base_ano is None:
        print(f"Nenhum diretório encontrado para o ano {year}")
        return
    caminho_dados = os.path.join(caminho_base_ano, "dados")
    if os.path.isdir(caminho_dados):
        arquivos_disponiveis = os.listdir(caminho_dados)
    if year < 2009:
        for arq in arquivos_disponiveis:
            if "INSTITUICAO" in arq.upper():
                os.rename(
                    os.path.join(caminho_dados, arq),
                    os.path.join(caminho_dados, f"MICRODADOS_ED_SUP_IES_{year}.CSV")
                )
            elif "GRADUACAO_PRESENCIAL" in arq.upper():
                os.rename(
                    os.path.join(caminho_dados, arq),
                    os.path.join(caminho_dados, f"MICRODADOS_CADASTRO_CURSOS_{year}.CSV")
                )
        arquivos_disponiveis = os.listdir(caminho_dados)
    ARQUIVO_IES = f"MICRODADOS_ED_SUP_IES_{year}.CSV"
    ARQUIVO_CURSOS = f"MICRODADOS_CADASTRO_CURSOS_{year}.CSV"
    caminho_ies = None
    for arquivo in arquivos_disponiveis:
        nome_normalizado = corrigir_nome_arquivo(arquivo).upper()
        if nome_normalizado.startswith(f"MICRODADOS_ED_SUP_IES_{year}") and nome_normalizado.endswith(".CSV"):
            caminho_ies = os.path.join(caminho_dados, arquivo)
            break
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
    if caminho_ies is None:
        caminho_ies = os.path.join(caminho_dados, f"MICRODADOS_ED_SUP_IES_{year}.CSV")
    print(f"Arquivos encontrados em {caminho_dados}: {arquivos_disponiveis}")
    print(f"Arquivo IES esperado: {ARQUIVO_IES}")
    print(f"Arquivo IES identificado: {caminho_ies if os.path.exists(caminho_ies) else 'NÃO ENCONTRADO'}")
    df_ies_final = pd.DataFrame()
    df_cursos_final = pd.DataFrame()
    if os.path.isfile(caminho_ies):
        df_ies = carregar_csv(caminho_ies, year=year)
        if not df_ies.empty:
            df_ies_final = filtrar_renomear(df_ies, COLUNAS_IES_RELEVANTES, MAPPING_IES)
            col_numeric_ies = ["docentes_total", "docentes_exercicio", "docentes_feminino", "docentes_masculino"]
            df_ies_final = converter_tipos(df_ies_final, col_numeric_ies)
        else:
            print(f"Aviso: {ARQUIVO_IES} está vazio ou não pôde ser processado.")
    else:
        print(f"Aviso: Arquivo {ARQUIVO_IES} não encontrado em {caminho_ies}.")
    caminho_cursos = os.path.join(caminho_dados, corrigir_nome_arquivo(ARQUIVO_CURSOS))
    if os.path.isfile(caminho_cursos):
        df_cursos = carregar_csv(caminho_cursos, year=year)
        if not df_cursos.empty:
            df_cursos_final = filtrar_renomear(df_cursos, COLUNAS_CURSOS_RELEVANTES, MAPPING_CURSOS)
            col_numeric_cursos = ["numero_cursos", "vagas_totais", "inscritos_totais", "ingressantes", "matriculados", "concluintes"]
            df_cursos_final = converter_tipos(df_cursos_final, col_numeric_cursos)
        else:
            print(f"Aviso: {ARQUIVO_CURSOS} está vazio ou não pôde ser processado.")
    else:
        print(f"Aviso: Arquivo {ARQUIVO_CURSOS} não encontrado em {caminho_cursos}.")
<<<<<<< Updated upstream

# Caso queira aplicar ainda um tratamento de continuidade (útil quando os dados serão consolidados
    # em um formato wide para o cálculo de métricas de evasão)
    # Exemplo de uso para um curso com duração definida:
    # cursos_interesse = {"ENGENHARIA CIVIL": 5, "MEDICINA": 6, "DIREITO": 5, "ADMINISTRAÇÃO": 4}
    # Aqui, a função tratar_continuidade seria aplicada sobre um DataFrame já pivotado (wide), por exemplo:
    # df_wide = pivot_wide(dados_consolidados)
    # for curso, duracao in cursos_interesse.items():
    #     df_wide.loc[df_wide["nome_curso"] == curso] = tratar_continuidade(df_wide[df_wide["nome_curso"] == curso], curso, duracao)
    # Porém, como o pré‑processamento trata os anos individualmente, esta etapa pode ser realizada
    # posteriormente no fluxo de análises.
    
    # ----------------------------------------------------------------------
    # Salvando resultados (IES e Cursos) na pasta "processado"
    # ----------------------------------------------------------------------
=======
>>>>>>> Stashed changes
    if not df_ies_final.empty:
        saida_ies = os.path.join(PASTA_PROCESSADO, f"dados_ies_{year}.csv")
        os.makedirs(os.path.dirname(saida_ies), exist_ok=True)
        df_ies_final.to_csv(saida_ies, sep=";", index=False, encoding="utf-8")
        print(f"[OK] dados_ies gerado em: {saida_ies}")
    else:
        print("Nenhum dado de IES para salvar.")
    if not df_cursos_final.empty:
        saida_cursos = os.path.join(PASTA_PROCESSADO, f"dados_cursos_{year}.csv")
        os.makedirs(os.path.dirname(saida_cursos), exist_ok=True)
        df_cursos_final.to_csv(saida_cursos, sep=";", index=False, encoding="utf-8")
        print(f"[OK] dados_cursos gerado em: {saida_cursos}")
    else:
        print("Nenhum dado de Cursos para salvar.")

if __name__ == "__main__":
    for year in range(2009, 2024):
        print(f"\tProcessing year {year} ...")
<<<<<<< Updated upstream
        main(year)
=======
        main(year)
    # Após processar todos os anos, consolida os dados dos cursos tratados e salva as taxas:
    salvar_taxas_consolidadas()
>>>>>>> Stashed changes
