

from tensorflow.keras.models import Sequential
from keras.layers import Dense

# Создайте модель
model = Sequential()


model.add(Dense(32, input_dim=15, activation='tanh'))
model.add(Dense(32, activation='tanh'))
model.add(Dense(32))
model.add(Dense(1))
model.compile(loss="mean_squared_error", metrics=["mae"])

# Добавьте слои к модели

# Загрузите веса из файла weights.h5
model.load_weights('model_weights.weights.h5')
print(model.get_weights())
print("успешно")