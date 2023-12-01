from main import app
import redis

db = redis.Redis(host='redis', port=6379)
db.ping()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}