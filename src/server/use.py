import pandas as pd
from fastapi.routing import APIRouter
from pydantic import BaseModel
import datetime as dt

import src.globals as g
from src.data.celendar import is_day_holiday

router = APIRouter(
    prefix="/use",
    tags = ["Предсказания"]
)

@router.get("predict_one")
def predict_one(
    date: dt.date,
    humidity: float
):
    # ["Holiday", "Sun", "Sat", "U", "Mon"
    df = pd.DataFrame(data={
        "Holiday": [is_day_holiday(date)],
        "Sun": [date.weekday() == 6],
        "Sat": [date.weekday() == 5],
        "U": [humidity],
        "Mon": [date.weekday() == 0]
    })
    result1 = g.model1.predict(df[:])
    result2 = g.model2.predict(df[:])

    result1[:] = g.ss["y1"].inverse_transform(result1[:])
    result2[:] = g.ss["y2"].inverse_transform(result2[:])

    result1 = str(result1[0][0])
    result2 = str(result2[0][0])
    return f"{result1} {result2}"


class Input(BaseModel):
    date: dt.date
    humidity: float


@router.get("predict_many")
def predict_many(
    data: list[Input]
):
    # ["Holiday", "Sun", "Sat", "U", "Mon"
    df = pd.DataFrame(data={
        "Holiday": [is_day_holiday(d.date) for d in data],
        "Sun": [d.date.weekday() == 6 for d in data],
        "Sat": [d.date.weekday() == 5 for d in data],
        "U": [d.humidity for d in data],
        "Mon": [d.date.weekday() == 0 for d in data]
    })
    result1 = g.model1.predict(df[:])
    result2 = g.model2.predict(df[:])
    return {
        "y1": result1,
        "y2": result2
    }

