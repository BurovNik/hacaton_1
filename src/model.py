import pandas as pd
from keras.models import Sequential, load_model
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

test_size = 0.25

def init():
    global model
    model = Sequential()
    model.add(Dense(32, input_dim=X.shape[1], activation='tanh'))
    model.add(Dense(32, activation='tanh'))
    model.add(Dense(32))
    model.add(Dense(1))
    model.compile(loss="mean_squared_error", metrics=["mae"])


def learn(df_x: pd.DataFrame, Y: pd.DataFrame, var="y1"):
    Y = Y.rename(columns={"Дата": "date", "Кол-во заказов": "y1", "Товарооборот": "y2"})
    Y['date'] = pd.to_datetime(Y['date']).dt.date
    X = df_x.join(Y.set_index('date'), on='date', how="inner")

    X = X.dropna()
    X.info()
    X = X[["Holiday", "Sun", "Sat", "U", "Mon"]]
    Y = Y[[var]]

    ss = StandardScaler()
    ss.fit(Y[:])
    Ys = Y.copy()
    Ys[:] = ss.transform(Y[:])

    X_train, X_test, y_train, y_test = train_test_split(X, Ys, test_size=test_size, shuffle=False)
    history = model.fit(X_train, y_train, epochs = 80, validation_data=(X_test, y_test))


def predict():
    ...
