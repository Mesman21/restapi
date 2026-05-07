from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    status: str
    year: int

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: str = Field(alias="_id")

    # Новий спосіб налаштування у Pydantic V2
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )