from fastapi import FastAPI
from sqlmodel import SQLModel
import asyncio
from tests.test_crud.models import Category
from tests.test_crud.db import session_factory, engine
from fastapi_amis_admin.crud import SQLModelCrud

crud = SQLModelCrud(Category, session_factory).register_crud()

app = FastAPI()
app.include_router(crud.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


asyncio.run(startup())
