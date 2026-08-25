from sqlalchemy import select
import library.sql.sql_format as sf
import library.route.route_format as rf
import library.error.error_list as el


async def match_users(data : rf.Login, async_session) -> sf.User:
    #match_data = sf.User(**data.model_dump(exclude_none=True)) if SQL class create will high efficiency consumption
    exc = select(sf.User).where(sf.User.name == data.name)
    result = await async_session.execute(exc)
    sql_data = result.scalars().one_or_none()

    if sql_data is not None :
        if (sql_data.name == data.name and
            sql_data.password == data.password):
            pass
        else:
            raise el.AccountNotMatch
    else:
        raise el.AccountNotFound

    return sql_data

async def search_users(id, async_session) -> sf.User:
    exc = select(sf.User).where(sf.User.id == id)
    result = await async_session.execute(exc)
    sql_data = result.scalars().one_or_none()

    if sql_data is None:
        raise el.AccountNotFound

    return sql_data
