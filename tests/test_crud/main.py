from fastapi import FastAPI
from sqlmodel import SQLModel
from tests.test_crud.models import Category, Tag
from tests.test_crud.db import session_factory, engine
from fastapi_amis_admin.crud import SQLModelCrud

app = FastAPI()
category_crud = SQLModelCrud(Category, session_factory).register_crud()

app.include_router(category_crud.router)

tag_crud = SQLModelCrud(Tag, session_factory).register_crud()

app.include_router(tag_crud.router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

