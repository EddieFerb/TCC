# Script: comparar_modelos.py
# Objetivo: Comparar dois modelos preditivos (.pkl e .h5) usando o dataset de entrada
# 'entrada_modelos.csv', que deve conter as colunas ['taxa_ingresso', 'vagas_totais', 'target'].
# O script gera métricas (MSE e R²) e gráficos comparativos de linha e dispersão,
# que são salvos na pasta 'resultados/'.

import pandas as pd
import os
os.makedirs("resultados", exist_ok=True)

# Carregar o arquivo de entrada
df = pd.read_csv('dados/processado/entrada_modelos.csv')

# Verificar e exibir as colunas disponíveis
colunas_disponiveis = df.columns.tolist()
print(f"📋 Colunas disponíveis: {colunas_disponiveis}")

# Verificar se todas as colunas necessárias estão presentes
colunas_necessarias = ['taxa_ingresso', 'vagas_totais', 'target']
if all(col in colunas_disponiveis for col in colunas_necessarias):
    df_modelo = df[colunas_necessarias].copy()
    print("✅ Dados carregados e prontos para comparação de modelos.")

    import matplotlib.pyplot as plt
    import joblib
    from tensorflow.keras.models import load_model
    from sklearn.metrics import mean_squared_error, r2_score

    # Separar variáveis
    X = df_modelo[['taxa_ingresso', 'vagas_totais']]
    y_true = df_modelo['target']

    # Carregar modelos
    modelo_pkl = joblib.load('modelos/modelos_salvos/modelo_melhor_evasao.pkl')
    modelo_h5 = load_model('modelos/modelos_salvos/modelo_finetuned_tcc.h5', compile=False)

    # Fazer previsões
    y_pred_pkl = modelo_pkl.predict(X)
    y_pred_h5 = modelo_h5.predict(X).flatten()

    # Avaliar modelos
    mse_pkl = mean_squared_error(y_true, y_pred_pkl)
    r2_pkl = r2_score(y_true, y_pred_pkl)

    mse_h5 = mean_squared_error(y_true, y_pred_h5)
    r2_h5 = r2_score(y_true, y_pred_h5)

    print("\nModelo .pkl")
    print(f"MSE: {mse_pkl:.4f}")
    print(f"R²: {r2_pkl:.4f}")

    print("\nModelo .h5")
    print(f"MSE: {mse_h5:.4f}")
    print(f"R²: {r2_h5:.4f}")

    # Gráfico comparativo
    plt.figure(figsize=(10, 5))
    plt.plot(y_true.values, label='Real', marker='o')
    plt.plot(y_pred_pkl, label='Predição .pkl', marker='x')
    plt.plot(y_pred_h5, label='Predição .h5', marker='s')
    plt.title('Comparação entre valores reais e predições dos modelos')
    plt.xlabel('Amostra')
    plt.ylabel('Taxa de evasão')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # A pasta 'resultados/' deve existir manualmente para evitar erros ao salvar os arquivos.
    plt.savefig('resultados/comparacao_modelos_linha.png')
    plt.savefig("resultados/comparacao_modelos_linha.png")
    plt.close()

    # Gráfico de dispersão
    plt.figure(figsize=(6, 6))
    plt.scatter(y_true, y_pred_pkl, label='Modelo .pkl', alpha=0.7)
    plt.scatter(y_true, y_pred_h5, label='Modelo .h5', alpha=0.7)
    plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'k--', lw=2)
    plt.title('Dispersão: Real vs Predito')
    plt.xlabel('Real')
    plt.ylabel('Predito')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # A pasta 'resultados/' deve existir manualmente para evitar erros ao salvar os arquivos.
    plt.savefig('resultados/comparacao_modelos_dispersao.png')
    plt.savefig("resultados/comparacao_modelos_dispersao.png")
    plt.close()

else:
    faltando = list(set(colunas_necessarias) - set(colunas_disponiveis))
    raise ValueError(f"❌ Colunas necessárias não encontradas: {faltando}")
