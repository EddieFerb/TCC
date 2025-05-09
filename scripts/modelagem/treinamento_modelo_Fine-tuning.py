# /scripts/modelagem/treinamento_modelo.py
# Script unificado para treinamento de modelos tradicionais e fine-tuning com rede neural

import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, confusion_matrix
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras import Model


def treinar_modelos_basicos(df, caminho_modelo, caminho_metricas):
    # Treinamento para prever ingressantes e concluintes
    if all(col in df.columns for col in ['numero_cursos', 'vagas', 'inscritos', 'docentes', 'ingressantes', 'concluintes']):
        print("Treinando modelos para ingressantes e concluintes...")

        X = df[['numero_cursos', 'vagas', 'inscritos', 'docentes']]
        y_ing = df['ingressantes']
        y_conc = df['concluintes']

        X_train_i, X_test_i, y_train_i, y_test_i = train_test_split(X, y_ing, test_size=0.2, random_state=42)
        X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_conc, test_size=0.2, random_state=42)

        modelo_i = RandomForestRegressor(random_state=42)
        modelo_c = RandomForestRegressor(random_state=42)
        modelo_i.fit(X_train_i, y_train_i)
        modelo_c.fit(X_train_c, y_train_c)

        joblib.dump(modelo_i, os.path.join(caminho_modelo, 'modelo_ingressantes.pkl'))
        joblib.dump(modelo_c, os.path.join(caminho_modelo, 'modelo_concluintes.pkl'))

        print(f"Score ingressantes: {modelo_i.score(X_test_i, y_test_i):.4f}")
        print(f"Score concluintes: {modelo_c.score(X_test_c, y_test_c):.4f}")

    # Treinamento para evasão com modelos tradicionais
    print("Treinando modelos para taxa de evasão...")
    df = df[['taxa_ingresso', 'taxa_conclusao', 'taxa_evasao']].dropna()
    X = df[['taxa_ingresso', 'taxa_conclusao']]
    y = df['taxa_evasao']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo_lr = LinearRegression()
    modelo_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo_lr.fit(X_train, y_train)
    modelo_rf.fit(X_train, y_train)

    r2_lr = r2_score(y_test, modelo_lr.predict(X_test))
    r2_rf = r2_score(y_test, modelo_rf.predict(X_test))
    melhor_modelo = modelo_rf if r2_rf > r2_lr else modelo_lr
    nome_melhor = 'Random Forest' if r2_rf > r2_lr else 'Regressão Linear'
    joblib.dump(melhor_modelo, os.path.join(caminho_modelo, 'modelo_melhor_evasao.pkl'))

    with open(os.path.join(caminho_metricas, 'metricas_modelos.txt'), 'w') as f:
        f.write(f"Modelo: {nome_melhor}\n")
        f.write(f"R² Linear: {r2_lr:.4f}\n")
        f.write(f"R² RF: {r2_rf:.4f}\n")
        f.write(f"Melhor modelo: {nome_melhor}\n")

    y_pred_class = (melhor_modelo.predict(X_test) >= 0.5).astype(int)
    y_test_class = (y_test >= 0.5).astype(int)
    cm = confusion_matrix(y_test_class, y_pred_class)
    plt.figure(figsize=(6, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f"Matriz de Confusão - {nome_melhor}")
    plt.xlabel("Predito")
    plt.ylabel("Verdadeiro")
    plt.savefig(os.path.join(caminho_metricas, 'matriz_confusao.png'))
    plt.close()


def fine_tune_modelo_transfer(df, caminho_modelo):
    print("Iniciando Fine-Tuning com modelo neural pré-treinado...")
    esperadas = ['taxa_ingresso', 'taxa_conclusao']
    faltando = [col for col in ['taxa_ingresso', 'taxa_conclusao'] if col not in df.columns]
    if faltando:
        raise ValueError(f"Colunas ausentes para fine-tuning: {faltando}")
    X = df[['taxa_ingresso', 'taxa_conclusao']].values
    y = df['taxa_evasao'].values

    from tensorflow.keras import Input

    base_model = load_model('modelos/base_modelo_neural.h5')

    entrada = Input(shape=(X.shape[1],), name='entrada_transfer')
    x = base_model(entrada, training=False)
    saida = Dense(1, activation='linear', name='saida_finetune')(x)
    model_finetuned = Model(inputs=entrada, outputs=saida)

    model_finetuned.compile(optimizer='adam', loss='mse', metrics=['mae'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model_finetuned.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

    model_finetuned.save(os.path.join(caminho_modelo, 'modelo_finetuned_tcc.h5'))
    print("Fine-Tuning concluído e modelo salvo.")


def main():
    caminho_modelo = './modelos/modelos_salvos'
    caminho_metricas = './modelos/resultados_modelos'
    os.makedirs(caminho_modelo, exist_ok=True)
    os.makedirs(caminho_metricas, exist_ok=True)

    df_principal = pd.read_csv('./dados/processado/dados_ingresso_evasao_conclusao.csv', sep=';', encoding='utf-8')
    treinar_modelos_basicos(df_principal, caminho_modelo, caminho_metricas)

    # Validação e limpeza prévia do CSV de transferência
    caminho_transfer = './dados/processado/dados_transfer_learning.csv'
    try:
        df_transfer = pd.read_csv(caminho_transfer, sep=';', encoding='utf-8')
    except pd.errors.ParserError:
        print("Erro ao ler CSV com separador ';'. Tentando com ','...")
        try:
            df_transfer = pd.read_csv(caminho_transfer, sep=',', encoding='utf-8')
        except pd.errors.ParserError:
            print("Erro persistente na leitura do CSV. Tentando leitura manual e correção...")

            # Correção linha a linha
            with open(caminho_transfer, 'r', encoding='utf-8') as f:
                linhas_validas = []
                for linha in f:
                    if linha.count(',') == 3 or linha.count(';') == 3:  # Espera-se 4 colunas
                        linhas_validas.append(linha)

            # Salva um novo CSV limpo
            caminho_corrigido = './dados/processado/dados_transfer_learning_corrigido.csv'
            with open(caminho_corrigido, 'w', encoding='utf-8') as f_out:
                f_out.writelines(linhas_validas)
            print(f"Arquivo corrigido salvo em: {caminho_corrigido}")
            df_transfer = pd.read_csv(caminho_corrigido, sep=',', encoding='utf-8', on_bad_lines='skip')

    # Já carregado acima após correção automatizada

    print("Colunas disponíveis em df_transfer:", df_transfer.columns.tolist())

    fine_tune_modelo_transfer(df_transfer, caminho_modelo)


if __name__ == '__main__':
    main()