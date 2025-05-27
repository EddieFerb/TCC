from tensorflow.keras.models import load_model

# Carregar modelo
modelo = load_model('modelos/modelo_finetuned_tcc.h5')

# Exibir arquitetura
modelo.summary()