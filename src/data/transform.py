import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def group(df: pd.DataFrame):
    df = df.groupby('date').agg({
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
        "Holiday": 'max'
    }).reset_index()
    return df


def transform(df: pd.DataFrame):
    norm = ["rain", "snow", "snowstorm", "fog"]
    df[norm] = MinMaxScaler().fit_transform(df[norm])
    stand = ["T", "P", "U", "V"]
    df[stand] = StandardScaler().fit_transform(df[stand])
    neutral = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Z", "O", "V", "L", "Holiday"]
    df[neutral] = df[neutral]
    return df
