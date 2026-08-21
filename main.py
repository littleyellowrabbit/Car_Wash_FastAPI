"""
Last Update Date:20260819
Python Version:3.14.5
Project Name:Car Wash.
Project Description:
    1.Try to simple project and learn simple FastAPI/Godot/postGreSQL function.
        1.FastAPI:Get/Post/ConfigParser/Async/APIRouter/JWT/Thread/Lock/Redis.
        2.SQL:SQLAlchemy/SQLAlchemy.Orm.
        3.Godot:Fundamental show result and button with action.
    2.Test to run in Linux by WSL Ubuntu and UI program in local.
    3.Deploy software using Docker.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from library.route.login import login as login_route
import library.sql.initialize_sheet as s_is
import uvicorn, multiprocessing

@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    print(fast_api)
    s_is.init_sql_parameter()
    await s_is.init_datasheet()
    yield
    if s_is.sql_engine:
        await s_is.sql_engine.dispose()

app = FastAPI(lifespan = lifespan)

app.include_router(login_route)

if __name__ == "__main__":
    #Prevent Windows exe bug
    multiprocessing.freeze_support()

    uvicorn.run(app, host="0.0.0.0", port=8000)