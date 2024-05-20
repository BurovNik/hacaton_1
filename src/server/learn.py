from fastapi import UploadFile
from fastapi.routing import APIRouter
import pandas as pd

from src.data import parse
from src.model import create_empty, learn_model
import src.globals as g

router = APIRouter(
    prefix="/learn"
)

router.post("/learn")
def learn(
    weather: UploadFile,
    target: UploadFile,
):
    with open(f"data/{weather.filename}", "wb") as buffer:
        buffer.write(weather.file.read())
    with open(f"data/{target.filename}", "wb") as buffer:
        buffer.write(target.file.read())

    df_x = pd.read_excel(f"data/{weather.filename}")
    df_y = pd.read_excel(f"data/{target.filename}")

    df = parse(df_x)
    model1, model2 = create_empty(), create_empty()
    learn_model(model1, df_x, df_y, "y1")
    learn_model(model2, df_x, df_y, "y2")
    g.model1 = model1
    g.model2 = model2

