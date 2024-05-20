import pandas as pd
import datetime as dt
import requests


def add_weekdays(df: pd.DataFrame):
    df["Mon"] = df['date'].apply(lambda x: 1 if x.weekday() == 0 else 0)
    df["Tue"] = df['date'].apply(lambda x: 1 if x.weekday() == 1 else 0)
    df["Wed"] = df['date'].apply(lambda x: 1 if x.weekday() == 2 else 0)
    df["Thu"] = df['date'].apply(lambda x: 1 if x.weekday() == 3 else 0)
    df["Fri"] = df['date'].apply(lambda x: 1 if x.weekday() == 4 else 0)
    df["Sat"] = df['date'].apply(lambda x: 1 if x.weekday() == 5 else 0)
    df["Sun"] = df['date'].apply(lambda x: 1 if x.weekday() == 6 else 0)
    return df

def add_season(df: pd.DataFrame):
    df["Z"] = df['date'].apply(lambda x: 1 if 1 <= x.month <= 2 or x.month == 12 else 0)
    df["O"] = df['date'].apply(lambda x: 1 if 9 <= x.month <= 11 else 0)
    df["V"] = df['date'].apply(lambda x: 1 if 3 <= x.month <= 5 else 0)
    df["L"] = df['date'].apply(lambda x: 1 if 6 <= x.month <= 8 else 0)
    return df


def load_holidays(year) -> list[int]:
    url = f'https://isdayoff.ru/api/getdata?year={year}'
    response = requests.get(url)
    return list(map(int, response.text))

def day_of_year(date):
    return (date - dt.date(date.year, 1, 1)).days

holidays = {}
def is_day_holiday(date: dt.date) -> int:
    year = date.year
    if year not in holidays:
        holidays[year] = load_holidays(year)
    return holidays[year][day_of_year(date)]


def add_holidays(df: pd.DataFrame):
    df["Holiday"] = df['date'].apply(lambda x: is_day_holiday(x))
    return df
