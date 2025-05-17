from fastapi import FastAPI
from app.api import auth, plant

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(plant.router, prefix="/api", tags=["plant"])
