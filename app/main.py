from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.endpoint.task import router, celery

app = FastAPI(title="Currency Converter")

app.include_router(router)







celery.conf.beat_schedule = {
    'update-currency-rates-every-10-seconds': {
        'task': 'update_currency_rates',
        'schedule': 10.0,
    },
}


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(f"redis://redis", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
