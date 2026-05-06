from pydantic import BaseModel, ConfigDict
from uuid import UUID
from enum import Enum
from typing import Optional

class BookStatus(str, Enum):
    AVAILABLE = "наявна в бібліотеці"
    ISSUED = "видана комусь"

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    status: BookStatus
    release_year: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)