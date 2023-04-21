from fastapi import FastAPI

from app.endpoint.task import router

app = FastAPI(title="Currency Converter")


app.include_router(router)









