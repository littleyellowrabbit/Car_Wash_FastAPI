import datetime
from fastapi import Depends, HTTPException, status, APIRouter
import library.sql.initialize_sheet as s_is
import library.route.route_format as r_rf
import library.sql.account as s_a
import library.error.error_list as el
import library.redis.redis as r_r
import library.file.config_token as f_ct
from library.file.config_name import redis_name


account = APIRouter(prefix="/account", tags=["login"])

@account.post("/login", response_model=r_rf.LoginResponse, status_code=status.HTTP_200_OK)
async def user_login(data: r_rf.Login, async_session = Depends(s_is.get_sql_session)) -> r_rf.LoginResponse:
    try:
        sql_data = await s_a.match_users(data,async_session)

        timedelta_access = datetime.timedelta(minutes=30)
        expire_access = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0) + timedelta_access
        exp_access = int(expire_access.timestamp())

        access_payload = {
            "id" : str(sql_data.id),
            "permission" : sql_data.permission,
            "type" : "access",
            "exp" : exp_access
        }
        access_token = f_ct.encode_private_key(access_payload)
        r_r.set_with_expiry(redis_name.get('token_access_name') + str(sql_data.id),access_token,int(timedelta_access.total_seconds()))

        timedelta_refresh = datetime.timedelta(days=2)
        expire_refresh = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0) + timedelta_refresh
        exp_refresh = int(expire_refresh.timestamp())

        refresh_payload = {
            "id" : str(sql_data.id),
            "type" : "refresh",
            "exp" : exp_refresh
        }
        refresh_token = f_ct.encode_private_key(refresh_payload)
        r_r.set_with_expiry(redis_name.get('token_refresh_name') + str(sql_data.id), refresh_token,int(timedelta_refresh.total_seconds()))

        result = r_rf.LoginResponse(
            id = sql_data.id,
            permission = sql_data.permission,
            exp = exp_access,
            access_token = access_token,
            refresh_token = refresh_token
        )
        return result

    except (el.AccountNotMatch,el.AccountNotFound):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account or Password wrong")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@account.post("/refresh",response_model=r_rf.RefreshResponse, status_code=status.HTTP_200_OK)
async def user_refresh_token(data:r_rf.Refresh, async_session = Depends(s_is.get_sql_session)) -> r_rf.RefreshResponse:
    redis_key = redis_name.get('token_refresh_name') + str(data.id)
    if r_r.exists(redis_key) and r_r.get_value(redis_key) == data.refresh_token:
        try:
            sql_data = await s_a.search_users(data.id, async_session)
            timedelta_access = datetime.timedelta(minutes=30)
            expire_access = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0) + timedelta_access
            exp_access = int(expire_access.timestamp())

            access_payload = {
                "id" : str(sql_data.id),
                "type" : "access",
                "permission" : sql_data.permission,
                "exp" : exp_access,
            }

            access_token = f_ct.encode_private_key(access_payload)
            r_r.set_with_expiry(redis_name.get('token_access_name') + str(sql_data.id),access_token,int(timedelta_access.total_seconds()))

            timedelta_refresh = datetime.timedelta(days=2)
            expire_refresh = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0) + timedelta_refresh
            exp_refresh = int(expire_refresh.timestamp())

            refresh_payload = {
                "id": str(sql_data.id),
                "type": "refresh",
                "exp": exp_refresh,
            }

            refresh_token = f_ct.encode_private_key(refresh_payload)
            r_r.set_with_expiry(redis_name.get('token_refresh_name') + str(sql_data.id), refresh_token,int(timedelta_refresh.total_seconds()))

            result = r_rf.RefreshResponse(
                id = sql_data.id,
                permission = sql_data.permission,
                exp = exp_access,
                access_token = access_token,
                refresh_token = refresh_token
            )
            return result

        except el.AccountNotFound:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account not found")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token expired")



@account.post("/logout",status_code=status.HTTP_200_OK)
async def user_logout(userid,) -> None:
    #still need check access key because their may hack try to auto logout.
    try:
        token = f_ct.get_token()
        r_r
