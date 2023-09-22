from fastapi import FastAPI
from routers.lenguaje import lenguaje

app = FastAPI()

app.include_router(lenguaje)