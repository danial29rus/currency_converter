from sqlalchemy import Column, String, Float, Integer, DateTime

from app.database import Base


class CurrencyRate(Base):
    __tablename__ = 'currency_rates'

    id = Column(Integer, primary_key=True, index=True)
    currency_code = Column(String)
    rate = Column(Float)
    updated_at = Column(DateTime)