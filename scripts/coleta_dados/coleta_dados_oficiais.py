# scripts/coleta_dados/coleta_dados_oficiais.py
# Este script realiza a coleta e processamento de microdados oficiais do INEP e MEC.

import os
import requests
import pandas as pd
from zipfile import ZipFile

def baixar_arquivo(url, destino):
    """
    Faz o download de um arquivo a partir de uma URL e salva no destino especificado.
    """
    try:
        resposta = requests.get(url, stream=True)
        resposta.raise_for_status()  # Verifica se houve erro na resposta
        with open(destino, 'wb') as arquivo:
            for chunk in resposta.iter_content(chunk_size=8192):
                arquivo.write(chunk)
        print(f'Download concluído: {destino}')
    except requests.RequestException as e:
        print(f'Erro ao baixar {url}: {e}')

def extrair_arquivo(zip_caminho, destino_pasta):
    """
    Extrai um arquivo ZIP para o destino especificado e ajusta estrutura se necessário.
    """
    try:
        with ZipFile(zip_caminho, 'r') as zip_ref:
            zip_ref.extractall(destino_pasta)
        print(f'Arquivos extraídos para: {destino_pasta}')

        # Verificar estrutura do diretório após extração
        for root, dirs, files in os.walk(destino_pasta):
            print(f'Conteúdo de {root}: {dirs}, {files}')
            break  # Apenas primeiro nível para não poluir o log

    except Exception as e:
        print(f'Erro ao extrair {zip_caminho}: {e}')

def normalizar_nomes_arquivos(caminho_pasta, ano):
    """
    Renomeia os arquivos de IES para seguir o formato esperado: MICRODADOS_ED_SUP_IES_YEAR.CSV.
    """
    for root, _, arquivos in os.walk(caminho_pasta):
        for arquivo in arquivos:
            if "CADASTRO_IES" in arquivo.upper() and arquivo.upper().endswith('.CSV'):
                caminho_antigo = os.path.join(root, arquivo)
                caminho_novo = os.path.join(root, f"MICRODADOS_ED_SUP_IES_{ano}.CSV")
                os.rename(caminho_antigo, caminho_novo)
                print(f'Renomeado: {caminho_antigo} -> {caminho_novo}')

def processar_microdados(caminho_pasta):
    """
    Processa os arquivos de microdados e retorna um DataFrame consolidado.
    """
    # Normaliza os nomes dos arquivos de IES antes de processar
    # Extraindo o ano a partir do nome da pasta (assumindo que a pasta contenha o ano)
    ano = os.path.basename(caminho_pasta).split('_')[1] if '_' in os.path.basename(caminho_pasta) else 'NA'
    normalizar_nomes_arquivos(caminho_pasta, ano)
    arquivos_csv = [os.path.join(caminho_pasta, f) for f in os.listdir(caminho_pasta) if f.upper().endswith('.CSV')]
    df_lista = []
    for arquivo in arquivos_csv:
        try:
            df = pd.read_csv(arquivo, sep=';', encoding='latin1')
            df_lista.append(df)
        except Exception as e:
            print(f'Erro ao processar {arquivo}: {e}')
    if df_lista:
        return pd.concat(df_lista, ignore_index=True)
    else:
        print('Nenhum dado processado.')
        return pd.DataFrame()

def main():
    # URLs reais dos microdados
    urls = {
        'INEP_2023-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2023.zip',
        'INEP_2022-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2022.zip',
        'INEP_2021-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2021.zip',
        'INEP_2020-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2020.zip',
        'INEP_2019-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2019.zip',
        'INEP_2018-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2018.zip',
        'INEP_2017-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2017.zip',
        'INEP_2016-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2016.zip',
        'INEP_2015-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2015.zip',
        'INEP_2014-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2014.zip',
        'INEP_2013-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2013.zip',
        'INEP_2012-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2012.zip',
        'INEP_2011-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2011.zip',
        'INEP_2010-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2010.zip',
        'INEP_2009-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2009.zip',
        # 'INEP_2008-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2008.zip',
        # 'INEP_2007-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2007.zip',
        # 'INEP_2006-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2006.zip',
        # 'INEP_2005-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2005.zip',
        # 'INEP_2004-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2004.zip',
        # 'INEP_2003-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2003.zip',
        # 'INEP_2002-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2002.zip',
        # 'INEP_2001-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2001.zip',
        # 'INEP_2000-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_2000.zip',
        # 'INEP_1999-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_1999.zip',
        # 'INEP_1998-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_1998.zip',
        # 'INEP_1997-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_1997.zip',
        # 'INEP_1996-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_1996.zip',
        # 'INEP_1995-MICRODADOS-CENSO': 'https://download.inep.gov.br/microdados/microdados_censo_da_educacao_superior_1995.zip'
    }
    
    # Caminho para salvar os dados
    pasta_dados = './dados/bruto'
    os.makedirs(pasta_dados, exist_ok=True)
    
    for fonte, url in urls.items():
        zip_caminho = os.path.join(pasta_dados, f'{fonte}.zip')
        pasta_extracao = os.path.join(pasta_dados, fonte)
        os.makedirs(pasta_extracao, exist_ok=True)
        
        # Baixar o arquivo
        print(f'Baixando dados da fonte: {fonte}')
        baixar_arquivo(url, zip_caminho)
        
        # Extrair o arquivo
        print(f'Extraindo dados da fonte: {fonte}')
        extrair_arquivo(zip_caminho, pasta_extracao)
        
        # Processar os dados
        print(f'Processando dados da fonte: {fonte}')
        df = processar_microdados(pasta_extracao)
        
        # Salvar o DataFrame consolidado
        if not df.empty:
            df.to_csv(os.path.join(pasta_dados, f'{fonte}_dados_brutos.csv'), index=False)
            print(f'Dados processados e salvos em: {os.path.join(pasta_dados, f"{fonte}_dados_brutos.csv")}')
        else:
            print(f'Nenhum dado válido processado para {fonte}.')

if __name__ == '__main__':
    main()