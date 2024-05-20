import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

import src.data as parser

data = pd.read_excel("Архив погоды.xls")

df = parser.parse_their_df(data)

df = parser.add_weekdays(df)
df = parser.add_season(df)
df = parser.add_holidays(df)

df = parser.group(df)
df = parser.transform(df)

print(df)


from sklearn.model_selection import train_test_split

# X = df11.drop(["y1", "y2", "date", 'v', 'T', 'Mon', "Tue", "Wed", "Thu", "Fri", "Z", "O", "V", "L"], axis=1)
# X = df11[["Holiday", "Sun", "Sat", "U", "Mon", "L", "conc", "rain", "snow", "fog", "v"]]
print(X_train)
print("164")


# history = model.fit(X_train, y_train, epochs = 80, validation_data=(X_test, y_test))

print(model.evaluate(X_test, y_test)[1])

print(model.get_weights())
print(183)

model.save_weights('model_weights.weights.h5')

print("-------------------------------------------")

from tensorflow.keras.models import Sequential

# Создайте модель
model = Sequential()
# Добавьте слои к модели

# Загрузите веса из файла weights.h5
model.load_weights('model_weights.weights.h5')

print(model.get_weights())
print("успешно")

y_pred = model.predict(X_test).T[0]
print(y_pred)

df_test = pd.DataFrame(data=X_test.copy())
df_test.insert(0, "y1", y_test)

df_pred = pd.DataFrame(data=X_test.copy())
df_pred.insert(0, "y1", y_pred)

table = {
    "Actual": round(df_test["y1"]),
    "Predicted": round(df_pred["y1"]),
    "Diff": abs(round(df_test["y1"] - df_pred["y1"])),
    "Diff(%)": abs(round((df_test["y1"] - df_pred["y1"]) / df_test["y1"] * 100)),
}
table = pd.DataFrame(table)
table.head(n=15)

ooh = table.loc[table['Diff(%)'] > 30, :]
error = df0.loc[ooh.index]
error["actual"] = table['Actual']
error["pred"] = table['Predicted']
error["diff"] = table['Diff']
print(error)

import matplotlib.pyplot as plt

plt.scatter(df_test.index, df_test.y1, marker='.')
plt.scatter(df_pred.index, df_pred.y1, marker='.')
plt.legend(["test", "pred"])
plt.show()

plt.figure(figsize=(7,6))
plt.plot(history.history['mae'], label='mae')
plt.plot(history.history['val_mae'], label = 'val_mae')
plt.xlabel('Epoch')
plt.ylabel('MAE')
plt.legend(loc='upper right')
plt.grid()