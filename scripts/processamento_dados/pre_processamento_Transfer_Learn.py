# scripts/processamento_dados/pre_processamento_Transfer_Learn.py
# Este script prepara um CSV limpo e padronizado para uso nos modelos de Transfer Learning e Fine-tuning

import pandas as pd
import os

def preprocessar_transfer_learning(caminho_entrada, caminho_saida):
    df = pd.read_csv(caminho_entrada, sep=None, engine='python')

    # Seleciona apenas as colunas de interesse e renomeia se necessário
    colunas_validas = ['taxa_ingresso', 'vagas_totais', 'taxa_evasao']
    df = df[[col for col in colunas_validas if col in df.columns]]

    # Remove linhas com valores ausentes ou inválidos
    df = df.dropna()

    # Garante que todas as colunas estão em float
    df = df.astype(float)

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    df.to_csv(caminho_saida, index=False)
    print(f"Base processada salva em: {caminho_saida}")


if __name__ == '__main__':
    entrada = './dados/processado/dados_transfer_learning.csv'
    saida = './dados/processado/dados_transfer_learning_clean.csv'
    preprocessar_transfer_learning(entrada, saida)
