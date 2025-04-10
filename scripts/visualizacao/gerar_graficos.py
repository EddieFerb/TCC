# scripts/visualizacao/gerar_graficos.py
# Este script gera gráficos para visualizar os resultados da análise.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    df = pd.read_csv('dados/processado/ies_dados_limpos.csv')
    
    # Gráfico de distribuição da taxa de evasão
    plt.figure(figsize=(10,6))
    sns.histplot(df['taxa_evasao'], bins=20, kde=True, color='blue')
    plt.title('Distribuição da Taxa de Evasão')
    plt.xlabel('Taxa de Evasão (%)')
    plt.ylabel('Frequência')
    plt.savefig('relatorios/figuras/distribuicao_taxa_evasao.png')
    plt.close()
    
    # Gráfico de taxa de evasão por estado
    plt.figure(figsize=(12,8))
    sns.boxplot(x='estado', y='taxa_evasao', data=df)
    plt.title('Taxa de Evasão por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Taxa de Evasão (%)')
    plt.savefig('relatorios/figuras/taxa_evasao_por_estado.png')
    plt.close()
    
    print('Gráficos gerados e salvos em relatorios/figuras/')

if __name__ == '__main__':
    main()