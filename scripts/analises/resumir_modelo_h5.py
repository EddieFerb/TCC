# Path: scripts/analises/resumir_modelo_h5.py
# Purpose (en): <write English purpose here>
# Propósito (pt-BR): <escreva em Português aqui>

from tensorflow.keras.models import load_model

# Carregar modelo
modelo = load_model('modelos/modelo_finetuned_tcc.h5')

# Exibir arquitetura
modelo.summary()