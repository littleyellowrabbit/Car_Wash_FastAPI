"""
Last Update Date:20261014
Python Version:3.14.5
Project Name:Car Wash.
Project Description:
    1.Try to simple project and learn simple FastAPI/Godot/postGreSQL function.
        1.FastAPI:Get/Post/Delete/ConfigParser/Async/APIRouter/JWT(RS256)/Redis/CI&CD/Pytest.
        2.SQL:SQLAlchemy/SQLAlchemy.Orm.
        3.Godot:Fundamental show result and button with action.
    2.Deploy software using Docker.
"""
import asyncio
from fastapi import FastAPI,Request,status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn, multiprocessing
from contextlib import asynccontextmanager
from library.route.account import account as account_route
from library.route.plc import plc as plc_route
import library.plc_simulator.plc_simulator_bridge as ps_psb
import library.sql.initialize_sheet as s_is
import library.redis.redis as r_r
import library.file.config_token as f_ct

@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    print(fast_api)
    r_r.init_redis_session()
    f_ct.initial_token()
    s_is.init_sql_parameter()
    await s_is.init_datasheet()

    ps_psb.running_flag["active"] = True
    plc_task = asyncio.create_task(asyncio.to_thread(ps_psb.plc_client))

    yield

    ps_psb.running_flag["active"] = False
    await plc_task

    if r_r.redis_pool:
        await r_r.close_redis_session()

    if s_is.sql_engine:
        await s_is.sql_engine.dispose()


app = FastAPI(lifespan = lifespan)

#Because format limit error can't be intercept
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request,exc: RequestValidationError):
#request in parameter is necessary even without use it,if without it would error occur.
    print(request)
    print(f"{exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": "format wrong."
        }
    )

app.include_router(account_route)
app.include_router(plc_route)

if __name__ == "__main__":
    #Prevent Windows exe bug
    multiprocessing.freeze_support()

    uvicorn.run(app, host="0.0.0.0", port=8000)