import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

data = pd.read_excel("Архив погоды.xls")

data2 = data[[
    "Местное время в Санкт-Петербурге",
    "T",
    "P",
    "U",
    "Ff",
    "ff10",
    # "ff3",
    "W1"
]]

data2['Местное время в Санкт-Петербурге'] = pd.to_datetime(data2['Местное время в Санкт-Петербурге'])
print(data2.info())

data2 = data2.rename(columns={
    "Местное время в Санкт-Петербурге": "t",
    "Ff": "v",
    "ff10": "V10",
    "W1": "Weather"
})
print(data2)

df = data2.copy()
df["Weather"].unique()

df["rain"] = df["Weather"]
map1 = {
    np.NAN: 0,
    "Морось.": 1,
    "Дождь.": 2,
    "Гроза (грозы) с осадками или без них.": 3,
    "Ливень (ливни).": 3
}
df['rain'] = df['rain'].apply(lambda w: map1[w] if w in map1 else 0).astype('int')
df['rain!'] = (df["Weather"] == "Ливень (ливни).").astype('int')
df['snow'] = (df['Weather'] == 'Снег или дождь со снегом.').astype('int')
df['fog'] = (df['Weather'] == 'Туман или ледяной туман или сильная мгла.').astype('int')
df['snowstorm'] = (df['Weather'] == 'Песчаная или пыльная буря или снежная низовая метель.').astype('int')


df['date'] = df['t'].dt.date


df = df.drop(df[df['t'].dt.time < dt.time(8)].index)


import requests

year = 2023

def get_holidays() -> list[int]:
    url = f'https://isdayoff.ru/api/getdata?year={year}'
    response = requests.get(url)
    return list(map(int, response.text))

def day_of_year(date):
  return (date - dt.date(year, 1, 1)).days

holidays = get_holidays()
def is_day_holiday(date) -> int:
  return holidays[day_of_year(date)]

import requests
import datetime as dt
from bs4 import BeautifulSoup

url = "https://concertinfo.ru/past/2022/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

arr = soup.find_all('a')
brr = [a for a in arr if a.get('data-id')]
crr = [b for b in brr if b.find_all(class_='buttonicon')]
dates = []

for c in crr:
    name = c.find('img').get('alt')
    d = c.find(class_='date').find('time').get('content')
    date = dt.datetime.strptime(d[:10], "%Y-%m-%d")
    city = c.find(class_='place').find('img').get('alt')
    if city == "Петербург":
      dates.append(date.date())

df["conc"] = df['date'].apply(lambda d: d in dates).astype('int')
print(df)

df["Mon"] = df['date'].apply(lambda x: 1 if x.weekday() == 0 else 0)
df["Tue"] = df['date'].apply(lambda x: 1 if x.weekday() == 1 else 0)
df["Wed"] = df['date'].apply(lambda x: 1 if x.weekday() == 2 else 0)
df["Thu"] = df['date'].apply(lambda x: 1 if x.weekday() == 3 else 0)
df["Fri"] = df['date'].apply(lambda x: 1 if x.weekday() == 4 else 0)
df["Sat"] = df['date'].apply(lambda x: 1 if x.weekday() == 5 else 0)
df["Sun"] = df['date'].apply(lambda x: 1 if x.weekday() == 6 else 0)
df["Z"] = df['date'].apply(lambda x: 1 if 1 <= x.month <= 2 or x.month == 12 else 0)
df["O"] = df['date'].apply(lambda x: 1 if 9 <= x.month <= 11 else 0)
df["V"] = df['date'].apply(lambda x: 1 if 3 <= x.month <= 5 else 0)
df["L"] = df['date'].apply(lambda x: 1 if 6 <= x.month <= 8 else 0)
df["Holiday"] = df['date'].apply(lambda x: is_day_holiday(x))


print(df)

df2 = df.groupby('date').agg({
    'T' : 'mean',
    'P' : 'mean',
    'U' : 'mean',
    'v' : 'mean',
    'rain': 'max',
    'snow': 'max',
    'fog': 'max',
    'snowstorm': 'max',
    'Mon': 'max',
    'Tue': 'max',
    'Wed': 'max',
    'Thu': 'max',
    'Fri': 'max',
    'Sat': 'max',
    'Sun': 'max',
    'Z': 'max',
    'O': 'max',
    'V': 'max',
    'L': 'max',
    "Holiday": 'max',
    'conc': 'max'
}).reset_index()
print(df2)

from sklearn.preprocessing import MinMaxScaler, StandardScaler

df0 = df2.copy()
norm = ["rain", "snow", "snowstorm", "fog"]
df0[norm] = MinMaxScaler().fit_transform(df2[norm])
stand = ["T", "P", "U", "V"]
df0[stand] = StandardScaler().fit_transform(df2[stand])
neutral = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Z", "O", "V", "L", "Holiday", "conc"]
df0[neutral] = df2[neutral]
print(df0)
print("145")

Y = pd.read_excel("Данные кофеен.xlsx")
Y = Y.rename(columns={"Дата": "date", "Кол-во заказов": "y1", "Товарооборот": "y2"})
Y['date'] = pd.to_datetime(Y['date']).dt.date
df1 = df0.join(Y.set_index('date'), on='date', how="inner")

df11 = df1.dropna()
df11.info()

from sklearn.model_selection import train_test_split

# X = df11.drop(["y1", "y2", "date", 'v', 'T', 'Mon', "Tue", "Wed", "Thu", "Fri", "Z", "O", "V", "L"], axis=1)
# X = df11[["Holiday", "Sun", "Sat", "U", "Mon", "L", "conc", "rain", "snow", "fog", "v"]]
X = df11[["Holiday", "Sun", "Sat", "conc", "Mon", "Tue", "Wed", "Thu", "Fri", "T", "U", "rain", "fog", "snow", "v"]]
# X = df11[["Holiday", "Sun", "Sat", "U", "Mon", "T"]]
y = df11["y1"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=False)
print(X_train)
print("164")

from keras.models import Sequential, load_model
from keras.layers import Dense

model = Sequential()

model.add(Dense(32, input_dim=X.shape[1], activation='tanh'))
model.add(Dense(32, activation='tanh'))
model.add(Dense(32))
model.add(Dense(1))
model.compile(loss="mean_squared_error", metrics=["mae"])


history = model.fit(X_train, y_train, epochs = 80, validation_data=(X_test, y_test))

print(model.evaluate(X_test, y_test)[1])

print(model.get_weights())
print(183)

model.save_weights('model_weights.weights.h5')
weights = model.get_weights()

# Запись весов в CSV файл
df = pd.DataFrame(weights)
df.to_csv('model_weights.csv', index=False)

# Загрузка весов из CSV файла
df = pd.read_csv('model_weights.csv')
weights = df.values.tolist()

# Создание новой модели
model = Sequential()
model.add(Dense(...)) # Добавьте слои как в вашей оригинальной модели

# Установка весов в новую модель
model.set_weights(weights)

#
# from itertools import *
#
# base = ["Holiday", "Sun", "Sat", "U", "Mon"]
# opt = ["conc", "rain", "fog", "snow", "L"]
# Xs = []
# # for n in range(1, len(opt)):
# #for n in range(2, len(opt)):
# #  for xs in combinations(opt, n):
# #    Xs.append(xs)
#
# #Xs = list(map(list, Xs))
# #print(Xs)
#
# def learn(xs):
#   X = df11[base + xs]
#   y = df11["y1"]
#   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=False)
#   model = Sequential()
#   model.add(Dense(32, activation='tanh', input_dim=X.shape[1]))
#   model.add(Dense(32, activation='tanh'))
#   model.add(Dense(32))
#   model.add(Dense(1))
#   model.compile(loss="mean_squared_error", metrics=["mae"])
#   model.fit(X_train, y_train, epochs = 80, validation_data=(X_test, y_test))
#   return model.evaluate(X_test, y_test)[1]
#
# result = {}
# for xs in Xs:
#   result[tuple(xs)] = learn(xs)
#
# for r in result:
#   print(r, result[r])
#
# y_pred = model.predict(X_test).T[0]
# print(y_pred)
#
# df_test = pd.DataFrame(data=X_test.copy())
# df_test.insert(0, "y1", y_test)
#
# df_pred = pd.DataFrame(data=X_test.copy())
# df_pred.insert(0, "y1", y_pred)
#
# table = {
#     "Actual": round(df_test["y1"]),
#     "Predicted": round(df_pred["y1"]),
#     "Diff": abs(round(df_test["y1"] - df_pred["y1"])),
#     "Diff(%)": abs(round((df_test["y1"] - df_pred["y1"]) / df_test["y1"] * 100)),
# }
# table = pd.DataFrame(table)
# table.head(n=15)
#
# ooh = table.loc[table['Diff(%)'] > 30, :]
# error = df0.loc[ooh.index]
# error["actual"] = table['Actual']
# error["pred"] = table['Predicted']
# error["diff"] = table['Diff']
# print(error)
#
# import matplotlib.pyplot as plt
#
# plt.scatter(df_test.index, df_test.y1, marker='.')
# plt.scatter(df_pred.index, df_pred.y1, marker='.')
# plt.legend(["test", "pred"])
# plt.show()
#
# plt.figure(figsize=(7,6))
# plt.plot(history.history['mae'], label='mae')
# plt.plot(history.history['val_mae'], label = 'val_mae')
# plt.xlabel('Epoch')
# plt.ylabel('MAE')
# plt.legend(loc='upper right')
# plt.grid()