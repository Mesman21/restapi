from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://root:password@mongodb:27017/")


def get_mongo_client():
    return AsyncIOMotorClient(MONGO_URL)

async def get_db():
    client = get_mongo_client()
    db = client.library_db
    try:
        yield db
    finally:
        client.close()