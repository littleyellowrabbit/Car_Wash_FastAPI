from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from collections.abc import AsyncGenerator
from typing import Optional
from library.sql import sql_format as Sf
from library.file import config_sql as Cs

sql_engine: Optional[AsyncEngine] = None
sql_session: Optional[async_sessionmaker] = None

def get_sql_session() -> AsyncGenerator[AsyncSession, None]:

def create_sql