from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger
from telegram_bot.routers import webhook,cron
import uvicorn

app = FastAPI()
app.include_router(webhook.router)
app.include_router(cron.router)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/item")
def update_item(item: Item):
    return {"item_name": item.price}


@app.on_event("startup")
async def startup_event():
    logger.info("Starting...")


if __name__ == "__main__":
    uvicorn.run("telegram_bot.app:app", host="127.0.0.1", port=8000, reload=True)
