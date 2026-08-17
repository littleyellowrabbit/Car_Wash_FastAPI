from sqlalchemy import select
import library.sql.sql_format as sf
import library.route.route_format as rf
from typing import Optional, Tuple

async def match_users(data : rf.User, async_session) -> Tuple[Optional[sf.User], bool]:
    is_login = False
    match_data = sf.User(**data.model_dump(exclude_none=True))
    exc = select(sf.User).where(sf.User.name == match_data.name)
    result = await async_session.execute(exc)
    sql_data = result.scalar().one_or_none()

    if sql_data is not None :
        if (sql_data.name == rf.User.name and
            sql_data.password == rf.User.password and
            sql_data.permission == rf.User.permission):
            is_login = True
    return sql_data,is_login
