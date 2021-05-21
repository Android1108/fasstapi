from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

import uvicorn

app = FastAPI()


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


if __name__ == "__main__":
  uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
