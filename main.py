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

import src.model as m

model = m.model
m.learn_model(df, pd.read_excel('data/"Данные кофеен.xlsx"'))



print(model.get_weights())
print(183)

model.save_weights('model_weights.weights.h5')

print("-------------------------------------------")


# Создайте модель
# Добавьте слои к модели

# Загрузите веса из файла weights.h5
