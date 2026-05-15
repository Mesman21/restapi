from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from uuid import UUID

class BookStatus(str, Enum):
    AVAILABLE = "наявні в бібліотеці"
    BORROWED = "видані комусь"

class BookBase(BaseModel):
    title: str = Field(..., example="Clean Code")
    author: str = Field(..., example="Robert C. Martin")
    description: Optional[str] = Field(None, example="Книга про написання чистого коду")
    year: int = Field(..., example=2008)
    status: BookStatus = Field(default=BookStatus.AVAILABLE)

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: UUID