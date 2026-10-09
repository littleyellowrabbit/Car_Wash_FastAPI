from sqlalchemy import select, insert, delete
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

async def search_users(userid, async_session) -> sf.User:
    exc = select(sf.User).where(sf.User.id == userid)
    result = await async_session.execute(exc)
    sql_data = result.scalars().one_or_none()

    if sql_data is None:
        raise el.AccountNotFound

    return sql_data

async def user_list(async_session) -> list:
    exc = select(sf.User.name, sf.User.permission)

    result = await async_session.execute(exc)

    sql_data = result.mappings().all()

    sql_dict = [dict(row) for row in sql_data]

    return sql_dict

async def user_add(data: rf.AddUser,async_session) -> None:
    print(data)
    exc = insert(sf.User).values(name=data.name, password=data.password, permission=data.permission)
    await async_session.execute(exc)
    await async_session.commit()

async def user_del(data: rf.DelUser,async_session) -> None:
    print(data)
    exc = delete(sf.User).where(sf.User.name == data.name)
    await async_session.execute(exc)
    await async_session.commit()
