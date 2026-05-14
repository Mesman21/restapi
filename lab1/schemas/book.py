from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    status: str
    year: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: UUID