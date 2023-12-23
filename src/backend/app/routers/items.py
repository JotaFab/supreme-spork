import time
import re
import json

import redis
from redis.commands.json.path import Path

from typing import Annotated
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

router = APIRouter(prefix="/api/v1", tags=["Items"])

db: redis.Redis = redis.Redis(host='localhost', port=6379, password="jota123")

@router.get("/items")
async def get_items(description: str | None = None):
    """
    Get items from Redis based on description.

    Args:
        description (str | None): Optional description to filter items.

    Returns:
        dict: Dictionary containing item names and their URLs.
    """
    response = None

    if not description:
        response = db.ft("idx:items_json").search("*")
    else:
        response = db.ft("idx:items_json").search("*" + description + "*")

    try:
        if response.total == 0:
            return {"message": "No items found"}
        else:
            doc_list: list[dict] = response.docs
            ans: dict = {}

            for doc in doc_list:
                data = json.loads(doc.json)
                item_name = data["item_name"]

                ans[f"name : {item_name}"] = f"http://localhost:8000/item/{doc.id}"

            return ans
    except Exception as e:
        print(e)
        

@router.get("/item/{item_id}")
async def get_item(item_id: str):
    """
    Get item from Redis based on item ID.

    Args:
        item_id (str): ID of the item.

    Returns:
        dict: Dictionary containing the item details.
    """
    return db.json().get(item_id)


class Item(BaseModel):
    """
    Item model.
    """
    item_code: int = Field(gt=1000000, lt=10000000)
    item_name: str = Field(min_length=1, max_length=70)
    description: str | None = Field(default=None, max_length=300)
    price: float


@router.put("/item/{id}")
def update_item(id: str, item: Annotated[Item, Body(embed=True)] ):
    """
    Update an item in Redis.

    Args:
        id (str): ID of the item to update.
        item (Item): Updated item details.

    Returns:
        dict: Dictionary containing the ID of the updated item and the updated item details.
    """
    return {"id": id, "item": item.model_dump()}


@router.post("/item/")
async def create_item(item: Annotated[Item, Body(embed=True)]):
    """
    Create a new item.

    Args:
        item (Item): Item details.

    Returns:
        json : JSON containing the details of the created item.
    """
    item_id = f"{time.time()}{item.item_code}"
    item_id = "".join(re.findall(r"\d+", item_id))

    db.json().set(f"item:{item_id}", Path.root_path(), obj=jsonable_encoder(item))
    db.expire(f"item:{item_id}", 3600)
    return db.json().get(f"item:{item_id}")