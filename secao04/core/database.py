from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from core.configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL)
Session: AsyncSession = sessionmaker(autoflush=False,
                                     expire_on_commit=False,
                                     _class=AsyncSession,
                                     bind=engine)  # type: ignore
