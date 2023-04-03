import models

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import fields, products, product_fields, types
import os


app = FastAPI(title="Marketease", description="Marketease API", version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fields.router)
app.include_router(products.router)
app.include_router(product_fields.router)
app.include_router(types.router)


@app.get("/app")
async def read_main():
    return {"message": "Hello World"}
