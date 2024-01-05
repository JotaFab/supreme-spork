from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx


router = APIRouter(prefix="/home", tags=["Front"])

templates = Jinja2Templates(directory="templates")

router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/", response_class= HTMLResponse)
async def home(request: Request):
    # Render the index.html template
    return templates.TemplateResponse(name="index.html", context={"request":request}) 


@router.get("/search", response_class= HTMLResponse)
async def search_items(request: Request,q: str = "*"):

    results : dict
    # Fetch search results from the external API
    
    try:
        
        async with httpx.AsyncClient() as client:
            response = await client.get("http://web:8000/api/v1/items", params={"q": q})
            results = response.json()
            search_results_html = render_search_results(request, results)
            return search_results_html
    except Exception as e:
        print(e)
            


def render_search_results(request: Request, results: dict):
    # Render search results as HTML using a template or client-side rendering
    response : str = "<h1>Search Results</h1><ul>"
    url : list = []
    data : list = []
    
    if results is None:
        response += f"<p>No results found</p>"
    
    else:    
        for key, value in results.items():
            key = key.lstrip("name: ")
            url.append(key)
            data.append(value)
            print(key)
        
    return templates.TemplateResponse(name="item.html", context={"request" : request, "data" : data, "items" : url}) 


@router.get("/item/{item_id}", response_class= HTMLResponse)
async def item(request: Request, item_id: str):
    # Render the index.html template
    item : dict = None
    try:
        async with httpx.AsyncClient() as client:
            item = await client.get(f"http://web:8000/api/v1/item/{item_id}")
            item = item.json()
            return templates.TemplateResponse(name="item.html", context={"request" : request, "item" : item}) 
    except Exception as e:
        print(e)
        
    
