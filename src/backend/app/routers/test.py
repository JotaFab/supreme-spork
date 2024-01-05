from fastapi import APIRouter, Response, File, UploadFile
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Annotated

router = APIRouter(prefix="/api/v1/test", tags=["Test"])



@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    
    return {"filename": file.filename, "content_type": file.content_type}

@router.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@router.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]