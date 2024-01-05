import redis
from redis.commands.search.query import Query
from redis.commands.search.field import TextField, TagField, NumericField 
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

def get_redis_db():
    pool = redis.ConnectionPool(host='redis', port=6379, password="jota123",decode_responses=True)
    try:
        db = redis.Redis(connection_pool=pool)
        return db
    except(redis.ConnectionError, redis.DataError):
        raise
    finally:
        if db:
            db.close()
        
db: redis.Redis = get_redis_db()


def create_idx(index_name: str, index_prefix: str, schema: tuple) -> None:
    
    try:
        
        info = db.ft(index_name).info()
        print("Index already exists")
        return info
    except:
        
        
        definition = IndexDefinition(prefix=[index_prefix], index_type=IndexType.JSON)
        
        db.ft(index_name).create_index(fields=schema, definition=definition)
        
        print("Index created")
        info = db.ft(index_name).info()
        print(f"Index created:\n {info}")
        return info
        

def delete_idx(index_name: str)  :
    
    
    return db.ft(index_name).dropindex(delete_documents=True)

