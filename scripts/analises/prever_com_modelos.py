import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# Carregar modelo .pkl (Scikit-Learn)
modelo_pkl = joblib.load('modelos/modelos_salvos/modelo_melhor_evasao.pkl')

# Entrada de exemplo: taxa_ingresso, taxa_conclusao
entrada = np.array([[0.45, 0.52]])

# Previsão com modelo .pkl
pred_pkl = modelo_pkl.predict(entrada)
print(f"Predição modelo .pkl: {pred_pkl[0]:.4f}")

# Carregar modelo .h5 (Keras)
modelo_h5 = load_model('modelos/modelo_finetuned_tcc.h5')

# Ajustar entrada para 3 colunas esperadas: media_geral (dummy), taxa_ingresso, taxa_conclusao
entrada_nn = np.array([[0.0, entrada[0][0], entrada[0][1]]])

# Previsão com modelo .h5
pred_h5 = modelo_h5.predict(entrada_nn, verbose=0)
print(f"Predição modelo .h5: {pred_h5[0][0]:.4f}")