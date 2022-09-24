from fastapi import FastAPI
from pydantic import BaseModel

from functions.surface import surfaceFct

app = FastAPI()

# run 'make dev' to test the application


@app.get("/")
def welcome():
    return {"message": "Welcome to AMENDIS API"}


# BaseModel for surfaceFct params
class SurfaceParams(BaseModel):
    list_des_x: list
    list_des_y: list


@app.post("/fct/surface")
def surface(params: SurfaceParams):
    s = surfaceFct(params.list_des_x, params.list_des_y)
    return {"La surface": s}
