import pandas as pd
import src.data as parser

def parse(df: pd.DataFrame):

    df = parser.parse_their_df(df)

    df = parser.add_weekdays(df)
    df = parser.add_season(df)
    df = parser.add_holidays(df)

    df = parser.group(df)
    df = parser.transform(df)
    return df

