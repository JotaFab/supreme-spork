import time
import re
import json

from redis.commands.json.path import Path

from typing import Annotated
from fastapi import APIRouter, Body, File, UploadFile
from fastapi.encoders import jsonable_encoder
from redis.commands.search.field import TextField, TagField, NumericField 

from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from ..models import Item
from ..db import db, create_idx
router = APIRouter(prefix="/api/v1", tags=["Items"])



@router.get("/items")
async def get_items(description: str | None = None)-> dict:
    """
    Get items from Redis based on description.

    Args:
        -**description** (str | None): Optional description to filter items.

    Returns:
        -**dict**: Dictionary containing item names and their URLs.
    """
    response = None
    schema = (
            NumericField("item_code"),
            TextField("item_name"),
            TextField("description"),
            TagField("tag"),
            NumericField("price"),
            NumericField("quantity"),
        )
    create_idx("idx:items_json", "item:", schema)
    
    if description:
        response = db.ft("idx:items_json").search("*" + description + "*")
    else:
        response = db.ft("idx:items_json").search("*")
    try:
        if response.total == 0:
            print(response)
            return {"message": "No items found"}
        else:
            item_list = response.docs
            print(item_list)
            ans: dict = {}
            for item in item_list:
                data = json.loads(item.json)
                item_name = data["item_name"]
                item_id = item.id.split(":")[1]
                ans[f"/home/item/{item_id}"] = data
            return ans
    except Exception as e:
        print(e)
    
    
        

    
@router.get("/item/{item_id}")
async def get_item(item_id: str) -> Item:
    """
    Get item from Redis based on item ID.

    Args:
        item_id (str): ID of the item.

    Returns:
        dict: Dictionary containing the item details.
    """
    prefix = "item:"
    item_id = prefix + item_id
    
    return db.json().get(item_id)


@router.put("/item/{id}")
def update_item(id: str, item: Annotated[Item, Body(embed=True)]) -> Item:
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
async def create_item(item: Annotated[Item, Body(embed=True)]) -> Item:
    """
    Create a new item.

    Args:
    - **item_code** (int): Item code.
    - **item_name** (str): Item name.
    - **tag** (list[str] | None): List of tags.
    - **description** (str | None): Item description.
    - **price** (float): Price of the item.
    - **quantity** (int): Quantity of the item.

    Returns:
        json : JSON containing the details of the created item.
    """
    item_id = f"{time.time()}{item.item_code}"
    item_id = "".join(re.findall(r"\d+", item_id))

    db.json().set(f"item:{item_id}", Path.root_path(), obj=jsonable_encoder(item))
    #db.expire(f"item:{item_id}", 3600)
    return db.json().get(f"item:{item_id}")