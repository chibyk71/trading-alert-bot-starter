
from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session
from .config import settings

engine = create_engine(settings.DB_URL, echo=False)

class Candle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    interval: int
    start: int
    end: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    confirm: bool

class Signal(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    symbol: str
    interval: int
    side: str
    reason: str
    ts: int

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
