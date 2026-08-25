from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from collections.abc import AsyncGenerator
from library.sql import sql_format as sf
from library.file import config_sql as cs

sql_engine: Optional[AsyncEngine] = None
sql_session: Optional[async_sessionmaker] = None

def init_sql_parameter() -> None:
    global sql_engine, sql_session
    sql_user,sql_password,sql_host,sql_database = cs.read_sql_config()
    sql_url = f"postgresql+asyncpg://{sql_user}:{sql_password}@{sql_host}/{sql_database}"
    sql_engine = create_async_engine(sql_url,pool_size=5,max_overflow=5,pool_timeout=3,pool_pre_ping=True,pool_recycle=300)
    sql_session = async_sessionmaker(bind=sql_engine,autoflush=False,autocommit=False,expire_on_commit=False)

async def get_sql_session() -> AsyncGenerator[AsyncSession, None]:
    global sql_session
    async with sql_session() as session:
        yield session

async def init_datasheet() -> None:
    async with sql_engine.connect() as conn:
        async with conn.begin():
            await conn.run_sync(sf.SQLBase.metadata.create_all)