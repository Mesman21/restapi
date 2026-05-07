from fastapi import FastAPI
from api.endpoints import router as books_router
from api.auth import router as auth_router

app = FastAPI(title="Library API v6")

app.include_router(auth_router)
app.include_router(books_router)