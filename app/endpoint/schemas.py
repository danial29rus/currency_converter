from typing import List

from pydantic import BaseModel


class CurrencyRateResponse(BaseModel):
    currency_code: str
    rate: float


class CurrencyRatesResponse(BaseModel):
    currency_rates: List[CurrencyRateResponse]



