# Este script prepara os dados de entrada para o treinamento de modelos preditivos.
# Ele lê a base tratada sem vazamento de dados, verifica se as colunas esperadas estão presentes,
# seleciona as features relevantes ('taxa_ingresso' e 'vagas_totais') e, se disponível,
# inclui a coluna 'taxa_evasao' como target. O resultado é salvo como CSV pronto para modelagem.
import pandas as pd
import os

# Caminho de entrada e saída
caminho_entrada = 'dados/processado/dados_transfer_learning_clean.csv'
caminho_saida = 'dados/processado/entrada_modelos.csv'

print("📥 Lendo base tratada para preparar entrada dos modelos...")
try:
    df = pd.read_csv(caminho_entrada)
    print(df.columns.tolist())
    print("📋 Colunas disponíveis:", df.columns.tolist())

    colunas_entrada = ['taxa_ingresso', 'vagas_totais']

    if not all(col in df.columns for col in colunas_entrada):
        raise ValueError(f"❌ Colunas necessárias não encontradas: {colunas_entrada}")

    # Seleciona apenas features
    df_modelo = df[colunas_entrada].copy()
    # df_modelo.columns = ['feature1', 'feature2']

    if 'taxa_evasao' in df.columns:
        df_modelo['target'] = df['taxa_evasao']
    else:
        raise ValueError("❌ Coluna 'taxa_evasao' não encontrada para definir como target.")

    # Salva em CSV
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    df_modelo.to_csv(caminho_saida, index=False)
    print(f"✅ Arquivo de entrada para os modelos salvo em: {caminho_saida}")

except Exception as e:
    print(f"❌ Erro ao preparar entrada dos modelos: {e}")