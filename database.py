from motor.motor_asyncio import AsyncIOMotorClient
import redis.asyncio as redis

_client = None
_redis = None

def get_db():
    global _client
    if _client is None:
        _client = AsyncIOMotorClient("mongodb://mongo:27017/")
    return _client.library_db

def get_users_col():
    return get_db().get_collection("users")

def get_books_col():
    return get_db().get_collection("books")

def get_redis():
    global _redis
    if _redis is None:
        _redis = redis.from_url("redis://redis:6379", decode_responses=True)
    return _redis