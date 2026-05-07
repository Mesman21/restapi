from pymongo import MongoClient

client = MongoClient("mongodb://mongo:27017/")
db = client["library_db"]
books_collection = db["books"]