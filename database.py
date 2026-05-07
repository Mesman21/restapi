from motor.motor_asyncio import AsyncIOMotorClient

_client = None

def get_db():
    global _client
    if _client is None:
        _client = AsyncIOMotorClient("mongodb://mongo:27017/")
    return _client.library_db

def get_books_col():
    return get_db().get_collection("books")

def get_users_col():
    return get_db().get_collection("users")