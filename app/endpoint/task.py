from datetime import datetime

import aiohttp as aiohttp
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import url
from app.database import get_async_session
from app.endpoint.models import CurrencyRate

router = APIRouter()


async def update_currency_rates(db: AsyncSession = Depends(get_async_session)):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            data = await response.json()
            timestamp = datetime.utcfromtimestamp(data['timestamp'])
            rates = data['rates']

            existing_rates = select(CurrencyRate)

            room = await db.execute(existing_rates)
            existing_rates_dict = {rate.currency_code: rate for rate in room.scalars()}

            for code, rate in rates.items():
                if code in existing_rates_dict:
                    existing_rates_dict[code].rate = rate
                else:
                    currency_rate = CurrencyRate(currency_code=code, rate=rate, updated_at=timestamp)
                    db.add(currency_rate)

            await db.commit()


@router.get('/convert_currency')
async def convert_currency(from_currency: str, to_currency: str, amount: float,
                           db: AsyncSession = Depends(get_async_session)):
    await update_currency_rates(db)
    from_rate = (
        await db.execute(
            select(CurrencyRate.rate).filter(CurrencyRate.currency_code == from_currency.upper()))).scalar_one()
    to_rate = (
        await db.execute(
            select(CurrencyRate.rate).filter(CurrencyRate.currency_code == to_currency.upper()))).scalar_one()

    return amount * to_rate / from_rate


@router.get("/currency_rates")
async def get_currency_rates(db: AsyncSession = Depends(get_async_session)):
    await update_currency_rates(db)
    query = await db.execute(select(CurrencyRate.currency_code, CurrencyRate.rate))
    ans = []
    for k, v in query:
        ans.append(f'валюта {k}, курс {v}')
    return ans
