from models import engine, Base

from fastapi import FastAPI
from routers import fields


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Marketease", description="Marketease API", version="0.0.1")

app.include_router(fields.router)


@app.get("/app")
async def read_main():
    return {"message": "Hello World"}
