from typing import Optional

from pydantic import BaseModel


class StockKeepingUnit(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    is_offer: Optional[bool] = None
