from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(title="Library API with MongoDB")

app.include_router(router)