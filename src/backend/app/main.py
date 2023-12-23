
from fastapi import FastAPI
from .routers import items

# Connect to Redis

# Create FastAPI app
app = FastAPI(decode_responses=True)

app.include_router(items.router)

