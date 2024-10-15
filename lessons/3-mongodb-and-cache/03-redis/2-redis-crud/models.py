from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    id: Optional[str] = None  # The item ID will be generated if not provided
    name: str
    description: str
    price: float
    in_stock: bool