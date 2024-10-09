from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session

async def get_session():
    session : AsyncSession = Session()
    try:
        yield session
    finally:
        session.close()
    