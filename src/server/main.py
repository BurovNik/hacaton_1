from fastapi import FastAPI

app = FastAPI(title="Беда & Baggins")

from src.server.setup import router as learn
from src.server.use import router as use

app.include_router(learn)
app.include_router(use)
