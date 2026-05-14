from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from typing import Optional

class BookStatus(str, Enum):
    AVAILABLE = "available"
    CHECKED_OUT = "checked_out"

class SortBy(str, Enum):
    TITLE = "title"
    YEAR = "year"

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: BookStatus = BookStatus.AVAILABLE
    year: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: str

    model_config = ConfigDict(from_attributes=True)