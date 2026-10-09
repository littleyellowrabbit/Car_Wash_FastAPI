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
async def user_login(data: r_rf.Login, async_session = Depends(s_is.get_sql_session), redis_session = Depends(r_r.get_redis_client)) -> r_rf.LoginResponse:
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
        # token in decode auto check "exp"
        #r_r.set_with_expiry(redis_name.get('token_access_name') + str(sql_data.id),access_token,int(timedelta_access.total_seconds()))

        timedelta_refresh = datetime.timedelta(days=2)
        expire_refresh = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0) + timedelta_refresh
        exp_refresh = int(expire_refresh.timestamp())

        refresh_payload = {
            "id" : str(sql_data.id),
            "type" : "refresh",
            "exp" : exp_refresh
        }
        refresh_token = f_ct.encode_private_key(refresh_payload)
        await r_r.set_with_expiry(redis_session, redis_name.get('token_refresh_name') + str(sql_data.id), refresh_token,int(timedelta_refresh.total_seconds()))

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
async def user_refresh_token(refresh_user : r_rf.RefreshUser = Depends(f_ct.decode_public_key_refresh), async_session = Depends(s_is.get_sql_session), redis_session = Depends(r_r.get_redis_client)) -> r_rf.RefreshResponse:
    try:
        sql_data = await s_a.search_users(refresh_user.id, async_session)
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
        #token in decode auto check "exp"
        #r_r.set_with_expiry(redis_name.get('token_access_name') + str(sql_data.id),access_token,int(timedelta_access.total_seconds()))

        timedelta_refresh = datetime.timedelta(days=2)
        expire_refresh = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0) + timedelta_refresh
        exp_refresh = int(expire_refresh.timestamp())

        refresh_payload = {
            "id": str(sql_data.id),
            "type": "refresh",
            "exp": exp_refresh,
        }

        refresh_token = f_ct.encode_private_key(refresh_payload)
        await r_r.set_with_expiry(redis_session, redis_name.get('token_refresh_name') + str(sql_data.id), refresh_token,int(timedelta_refresh.total_seconds()))

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


@account.post("/logout",status_code=status.HTTP_200_OK)
async def user_logout(access_user : r_rf.AccessUser = Depends(f_ct.decode_public_key_access),access_token : str = Depends(f_ct.get_token), redis_session = Depends(r_r.get_redis_client)) -> dict:
    try:
        #still need check access key because their may hack try to auto logout.
        now_time = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        await r_r.key_delete(redis_session, redis_name.get('token_refresh_name') + str(access_user.id))
        #max() prevent from second to negative number
        await r_r.set_with_expiry(redis_session, redis_name.get('token_access_black_name') + access_token, str(access_user.id), max(access_user.exp - int(now_time.timestamp()),1))
        return {'detail' : 'Logout Success'}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@account.get("/user_list",status_code=status.HTTP_200_OK)
async def user_list_update(_ : r_rf.AccessUser = Depends(f_ct.decode_public_key_access),async_session = Depends(s_is.get_sql_session)) -> list:
    try:
        user_list = await s_a.user_list(async_session)
        return user_list

    except Exception as e:
        raise   HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@account.post("/user_add",status_code=status.HTTP_200_OK)
async def user_account_add(user_data: r_rf.AddUser,_ : r_rf.AccessUser = Depends(f_ct.decode_public_key_access),async_session = Depends(s_is.get_sql_session)) -> dict:
    try:
        print(user_data)
        await s_a.user_add(user_data,async_session)
        return {'detail' : 'Add Success'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@account.delete("/user_delete",status_code=status.HTTP_200_OK)
async def user_account_delete(user_data: r_rf.DelUser,_ : r_rf.AccessUser = Depends(f_ct.decode_public_key_access),async_session = Depends(s_is.get_sql_session)) -> dict:
    try:
        print(user_data)
        await s_a.user_del(user_data,async_session)
        return {'detail' : 'Delete Success'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
