from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(title="Library API 4 with MongoDB")

app.include_router(router)