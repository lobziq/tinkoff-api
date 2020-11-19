from dataclasses import dataclass
from typing import Optional, List
from decimal import Decimal

from tinkoff.investments.model.base import (
    BaseModel,
    Currency,
    FigiName,
    TickerName,
    InstrumentType,
)


@dataclass
class MarketInstrument(BaseModel):
    figi: FigiName
    ticker: TickerName
    lot: int
    name: str
    type: InstrumentType
    currency: Optional[Currency] = None
    isin: Optional[str] = None
    minPriceIncrement: Optional[Decimal] = None
    minQuantity: Optional[int] = None


@dataclass
class MarketInstrumentList(BaseModel):
    total: int
    instruments: List[MarketInstrument]


__all__ = [
    'MarketInstrument',
    'MarketInstrumentList',
]
