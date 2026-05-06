from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.endpoints import router
from database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
   

app = FastAPI(title="Library API", lifespan=lifespan)

app.include_router(router)