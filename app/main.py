import asyncio

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from app.database import get_db
from app.endpoint.task import router, update_currency_rates

app = FastAPI(title="Currency Converter")
app.include_router(router)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(update_currency_rates())
    loop.run_until_complete(task)
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000, log_level='info', loop=loop)
