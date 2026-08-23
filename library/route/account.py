from fastapi import Depends, HTTPException, status, APIRouter
import library.sql.initialize_sheet as s_is
import library.route.route_format as r_rf
import library.sql.account as s_a
from typing import Optional
import library.error.error_list as el
import datetime
from library.file.config_token import encode_private_key
import library.redis.redis as r_r
import library.file.config_token as c_tk

account = APIRouter(prefix="/account", tags=["login"])

@account.post("/login", response_model=r_rf.LoginResponse, status_code=status.HTTP_200_OK)
async def user_login(data: r_rf.Login, async_session = Depends(s_is.get_sql_session)) -> Optional[r_rf.LoginResponse]:
    try:
        sql_data = await s_a.match_users(data,async_session)


        expire_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
        exp_timestamp = int(expire_time.timestamp())

        user_payload = {
            "id" : str(sql_data.id),
            "permission" : sql_data.permission,
            "exp" : expire_time
        }
        token = encode_private_key(user_payload)

        result = r_rf.LoginResponse(
            id = sql_data.id,
            permission = sql_data.permission,
            exp = exp_timestamp,
            access_token = token
        )

        return result

    except (el.AccountNotMatch,el.AccountNotFound):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account or Password wrong")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@account.post("/logout",status_code=status.HTTP_200_OK)
async def user_logout() -> None:
    try:
        token = c_tk.get_token()
        r_r