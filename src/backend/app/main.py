
from fastapi import FastAPI, Depends
from .routers import items,test,security_test
from .internal import admin
from .front import front

# Connect to Redis

# Create FastAPI app
app = FastAPI(decode_responses=True)

app.include_router(front.router)

app.include_router(items.router)
app.include_router(test.router)
#app.include_router(admin.router)
app.include_router(security_test.router)
async def parameters():
    return 
