from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from uuid import UUID

class BookStatus(str, Enum):
    AVAILABLE = "наявні в бібліотеці"
    BORROWED = "видані комусь"

class BookBase(BaseModel):
    title: str = Field(..., json_schema_extra={"example": "Clean Code"})
    author: str = Field(..., json_schema_extra={"example": "Robert C. Martin"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "Книга про написання чистого коду"})
    year: int = Field(..., json_schema_extra={"example": 2008})
    status: BookStatus = Field(default=BookStatus.AVAILABLE)
class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: UUID