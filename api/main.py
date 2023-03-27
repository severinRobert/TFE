import models

from fastapi import FastAPI
from routers import fields, products


app = FastAPI(title="Marketease", description="Marketease API", version="0.0.1")

app.include_router(fields.router)
app.include_router(products.router)


@app.get("/app")
async def read_main():
    return {"message": "Hello World"}
