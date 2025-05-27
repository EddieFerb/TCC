# Script: tratar_dados_Transfer_Learn.py
# Finalidade: Este script realiza o pré-processamento de dados para técnicas de Transfer Learning.
# Ele lê a base limpa `dados_transfer_learning_clean.csv`, verifica colunas essenciais, remove dados ausentes/duplicados
# e gera dois arquivos com transformações diferentes: normalização MinMax e padronização Z-Score.
# Saídas: `dados_transfer_normalizado.csv` e `dados_transfer_padronizado.csv` no diretório `dados/processado/`.
# Etapa do pipeline: 2ª etapa (após pre_processamento_Transfer_Learn.py e antes do treino dos modelos).
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Caminho de entrada e saída
caminho_entrada = './dados/processado/dados_transfer_learning_clean.csv'
caminho_saida = './dados/processado/'

def main():
    print("🔍 Lendo arquivo de entrada...")
    df = pd.read_csv(caminho_entrada)

    print("🔧 Verificando colunas necessárias...")
    colunas_esperadas = ['taxa_ingresso', 'vagas_totais', 'taxa_evasao']
    for col in colunas_esperadas:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória ausente: {col}")

    print("🧼 Removendo linhas com valores ausentes ou duplicadas...")
    df = df[colunas_esperadas].dropna().drop_duplicates()

    # ===== Normalização Min-Max =====
    print("📉 Aplicando normalização MinMaxScaler...")
    scaler_minmax = MinMaxScaler()
    df_minmax = pd.DataFrame(scaler_minmax.fit_transform(df), columns=colunas_esperadas)
    df_minmax.to_csv(os.path.join(caminho_saida, 'dados_transfer_normalizado.csv'), index=False)

    # ===== Padronização Z-Score =====
    print("📊 Aplicando padronização StandardScaler...")
    scaler_zscore = StandardScaler()
    df_zscore = pd.DataFrame(scaler_zscore.fit_transform(df), columns=colunas_esperadas)
    df_zscore.to_csv(os.path.join(caminho_saida, 'dados_transfer_padronizado.csv'), index=False)

    print("✅ Arquivos gerados com sucesso:")
    print(f" - {os.path.join(caminho_saida, 'dados_transfer_normalizado.csv')}")
    print(f" - {os.path.join(caminho_saida, 'dados_transfer_padronizado.csv')}")

if __name__ == '__main__':
    main()