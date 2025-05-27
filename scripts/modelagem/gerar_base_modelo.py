# scripts/modelagem/gerar_base_modelo.py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanAbsoluteError

model = Sequential([
    Input(shape=(2,)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1, activation='linear')
])

model.compile(optimizer='adam', loss=MeanSquaredError(), metrics=[MeanAbsoluteError()])
model.save('modelos/base_modelo_neural.h5')