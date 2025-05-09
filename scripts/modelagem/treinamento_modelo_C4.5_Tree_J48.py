# Script: treinamento_modelo_C4.5_Tree_J48.py
# Descrição: Treina modelos de regressão para prever a taxa de evasão acadêmica
# utilizando as variáveis 'taxa_ingresso' e 'vagas_totais' como preditoras.
# Avalia o desempenho de Regressão Linear e Random Forest, seleciona o melhor
# modelo com base no R², e salva o modelo e as métricas em arquivos apropriados.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os

print("Treinando modelos para taxa de evasão...")

# Carregar dados tratados
df = pd.read_csv('dados/processado/entrada_modelos.csv')

X = df[['taxa_ingresso', 'vagas_totais']]
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Regressão Linear
modelo_lr = LinearRegression()
modelo_lr.fit(X_train, y_train)
y_pred_lr = modelo_lr.predict(X_test)
mse_lr = mean_squared_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

# Random Forest
modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
modelo_rf.fit(X_train, y_train)
y_pred_rf = modelo_rf.predict(X_test)
mse_rf = mean_squared_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

# Escolher melhor modelo
melhor_modelo = modelo_lr if r2_lr > r2_rf else modelo_rf
melhor_nome = "Regressão Linear" if r2_lr > r2_rf else "Random Forest"

# Criar pastas
os.makedirs("modelos/modelos_salvos", exist_ok=True)
os.makedirs("modelos/resultados_modelos", exist_ok=True)

# Salvar melhor modelo
joblib.dump(melhor_modelo, 'modelos/modelos_salvos/modelo_melhor_evasao.pkl')

# Salvar métricas
with open("modelos/resultados_modelos/metricas_modelos.txt", "w") as f:
    f.write("Modelo: " + melhor_nome + "\n")
    f.write(f"MSE - Regressão Linear: {mse_lr:.4f}, R²: {r2_lr:.4f}\n")
    f.write(f"MSE - Random Forest: {mse_rf:.4f}, R²: {r2_rf:.4f}\n")
    f.write(f"Melhor Modelo Selecionado: {melhor_nome}\n")

print("Treinamento concluído. Melhor modelo para evasão:", melhor_nome)
print("Métricas salvas em: ./modelos/resultados_modelos")
print("Modelos salvos em: ./modelos/modelos_salvos")