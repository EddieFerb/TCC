# Script para validação temporal simples de modelo preditivo.
# Realiza análise de correlação, separa treino/teste com shuffle,
# treina modelo LinearRegression e exibe avaliação via MSE e R².
# Também plota gráfico de linha com comparação entre valores reais e preditos.

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Carrega os dados
df = pd.read_csv('dados/processado/entrada_modelos.csv')

print("\n📌 Correlação das features com o target:")
print(df.corr(numeric_only=True))

# Adiciona coluna 'ano' sequencialmente, assumindo que cada linha representa um ano de 2009 a 2023
if 'ano' not in df.columns:
    anos = list(range(2009, 2024))
    df['ano'] = [anos[i % len(anos)] for i in range(len(df))]

from sklearn.model_selection import train_test_split
# Embaralha e divide o conjunto entre treino e teste
X = df[['taxa_ingresso', 'vagas_totais']]
y = df['target']
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=42, shuffle=True)

# Treina modelo
modelo = LinearRegression()
modelo.fit(X_treino, y_treino)

# Avalia
y_pred = modelo.predict(X_teste)
print("\n📊 Avaliação no conjunto de TESTE:")
print("MSE:", round(mean_squared_error(y_teste, y_pred), 4))
print("R²:", round(r2_score(y_teste, y_pred), 4))

import matplotlib.pyplot as plt

# Gráfico de linha: valores reais vs preditos
plt.figure(figsize=(10, 5))
plt.plot(range(len(y_teste)), y_teste.values, label='Real', marker='o')
plt.plot(range(len(y_pred)), y_pred, label='Previsto', marker='x')
plt.title('Comparação entre valores reais e previstos (teste)')
plt.xlabel('Amostras')
plt.ylabel('Taxa de Evasão (normalizada)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('resultados/validacao_temporal_comparacao.png')
plt.show()