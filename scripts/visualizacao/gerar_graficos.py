# scripts/visualizacao/gerar_graficos.py
# Este script gera gráficos para visualizar os resultados da análise.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import unicodedata

def main():
    df = pd.read_csv('dados/processado/dados_ingresso_evasao_conclusao.csv', sep=';', on_bad_lines='skip')
    
    # Gráfico de distribuição da taxa de evasão
    plt.figure(figsize=(10,6))
    sns.histplot(df['taxa_evasao'], bins=20, kde=True, color='blue')
    plt.title('Distribuição da Taxa de Evasão')
    plt.xlabel('Taxa de Evasão (%)')
    plt.ylabel('Frequência')
    plt.savefig('relatorios/figuras/distribuicao_taxa_evasao.png')
    plt.close()
    
    # Gráfico de distribuição da taxa de conclusão
    plt.figure(figsize=(10,6))
    sns.histplot(df['taxa_conclusao'], bins=20, kde=True, color='green')
    plt.title('Distribuição da Taxa de Conclusão')
    plt.xlabel('Taxa de Conclusão (%)')
    plt.ylabel('Frequência')
    plt.savefig('relatorios/figuras/grafico_taxa_conclusao.png')
    plt.close()

    # Gráfico de distribuição da taxa de ingresso
    plt.figure(figsize=(10,6))
    sns.histplot(df['taxa_ingresso'], bins=20, kde=True, color='orange')
    plt.title('Distribuição da Taxa de Ingresso')
    plt.xlabel('Taxa de Ingresso (%)')
    plt.ylabel('Frequência')
    plt.savefig('relatorios/figuras/grafico_taxa_ingresso.png')
    plt.close()

    # Gráfico de dispersão entre ingressantes e concluintes
    plt.figure(figsize=(10,6))
    sns.scatterplot(x='ingressantes', y='concluintes', data=df)
    plt.title('Correlação entre Ingressantes e Concluintes')
    plt.xlabel('Ingressantes')
    plt.ylabel('Concluintes')
    plt.savefig('relatorios/figuras/grafico_ingressantes_vs_concluintes.png')
    plt.close()

    # Gráfico de barras por modalidade de ensino (taxa de evasão média)
    if 'modalidade_ensino' in df.columns:
        plt.figure(figsize=(10,6))
        sns.barplot(x='modalidade_ensino', y='taxa_evasao', data=df)
        plt.title('Taxa de Evasão Média por Modalidade de Ensino')
        plt.xlabel('Modalidade de Ensino')
        plt.ylabel('Taxa de Evasão (%)')
        plt.savefig('relatorios/figuras/grafico_taxa_evasao_modalidade.png')
        plt.close()

    # Heatmap de correlação
    plt.figure(figsize=(12,10))
    sns.heatmap(df[['taxa_ingresso', 'taxa_conclusao', 'taxa_evasao', 'ingressantes', 'concluintes']].corr(), annot=True, cmap='coolwarm')
    plt.title('Mapa de Calor das Correlações')
    plt.savefig('relatorios/figuras/grafico_mapa_calor_correlacoes.png')
    plt.close()

    print('Gráficos gerados e salvos em relatorios/figuras/')

if __name__ == '__main__':
    main()