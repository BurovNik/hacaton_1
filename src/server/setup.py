from fastapi import UploadFile
from fastapi.routing import APIRouter
import pandas as pd

import src.model
from src.data import parse
from src.model import create_empty, learn_model
from joblib import load as load_ss
import src.globals as g

router = APIRouter(
    prefix='/setup',
    tags=["Настойка"]
)

@router.post("/learn")
def learn(
    weather: UploadFile,
    target: UploadFile,
):
    with open(f"data/{weather.filename}", "wb") as buffer:
        buffer.write(weather.file.read())
    with open(f"data/{target.filename}", "wb") as buffer:
        buffer.write(target.file.read())

    df_x = pd.read_excel(f"data/{weather.filename}")
    df_x = parse(df_x)
    df_y = pd.read_excel(f"data/{target.filename}")

    model1, model2 = create_empty(), create_empty()
    learn_model(model1, df_x, df_y, "y1")
    learn_model(model2, df_x, df_y, "y2")
    g.model1 = model1
    g.model2 = model2
    return {"code": 200}


@router.post("/load")
def load():
    g.model1 = src.model.create_empty()
    g.model2 = src.model.create_empty()
    g.model1.load_weights('data/model1_weights.weights.h5')
    g.model2.load_weights('data/model2_weights.weights.h5')
    g.ss["y1"] = load_ss('ssy1.bin')
    g.ss["y2"] = load_ss('ssy2.bin')
    return {"code": 200}

@router.post("/save")
def save():
    g.model1.save_weights('data/model1_weights.weights.h5')
    g.model2.save_weights('data/model2_weights.weights.h5')
    return {"code": 200}
