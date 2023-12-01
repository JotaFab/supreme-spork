import redis
import time
import re
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from redis.commands.json.path import Path
from pydantic import BaseModel
from contextlib import asynccontextmanager
import json



db : redis.Redis = redis.Redis(host='localhost', port=6379, password="jota123")
    
    
app = FastAPI(decode_responses=True)



    
    

@app.get("/items/")
async def get_items(description: str | None = None):
    
    response = None
    
    if not description:
        response =  db.ft("idx:items_json").search("*")
    else: 
        response = db.ft("idx:items_json").search("*"+description+"*")
    
    try:
        if response.total == 0:
            return {"message" : "No items found"}
        else:
            doc_list : list[dict] = response.docs
            ans : dict = {}
            
            for doc in doc_list:
                data = json.loads(doc.json)
                item_name = data["item_name"]
                
                ans[f"name : {item_name}"] = f"http://localhost:8000/item/{doc.id}"
                
                
            return ans
    except Exception as e:
        print(e)
    
@app.get("/item/{item_id}")
async def get_item(item_id: str):
    
    
    return db.json().get(item_id)

class Item(BaseModel):
    item_code: int
    item_name: str
    description: str | None = None
    price: float
    

    

@app.put("/item/{id}")
def update_item(id: str, item: Item):
    
    return {"id" : id, "item" : item.model_dump()}

@app.post("/item/")
async def create_item(item: Item):
    item_id = f"{time.time()}{item.item_code}"
    item_id = "".join(re.findall(r"\d+", item_id))
    

    db.json().set(f"items:{item_id}",Path.root_path() ,obj = jsonable_encoder(item))
    
    return db.json().get(f"items:{item_id}")


