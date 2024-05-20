import pandas as pd
import numpy as np
import datetime as dt

def parse_their_df(data: pd.DataFrame):
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

    data2 = data2.rename(columns={
        "Местное время в Санкт-Петербурге": "t",
        "Ff": "v",
        "ff10": "V10",
        "W1": "Weather"
    })

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
    return df