from fastapi import FastAPI
from api.endpoints import router as books_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "API is running"}

app.include_router(books_router, prefix="/books", tags=["Books"])