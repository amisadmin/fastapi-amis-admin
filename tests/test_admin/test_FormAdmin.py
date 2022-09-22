from typing import Any

import pytest
from httpx import AsyncClient
from pydantic import BaseModel
from starlette.requests import Request

from fastapi_amis_admin import admin
from fastapi_amis_admin.admin import AdminSite
from fastapi_amis_admin.crud import BaseApiOut


class LoginSchema(BaseModel):
    username: str
    password: str


class TmpAdmin(admin.FormAdmin):
    page_path = "/test"


class TmpAdmin1(TmpAdmin):
    schema = LoginSchema

    async def handle(self, request: Request, data: BaseModel, **kwargs) -> BaseApiOut[Any]:
        ret = data.dict()
        return BaseApiOut(data={**ret, "extra": "success"})


class TmpAdmin2(TmpAdmin1):
    form_init = True

    async def get_init_data(self, request: Request, **kwargs) -> BaseApiOut[Any]:
        return BaseApiOut(data={"username": "admin", "password": "admin"})


async def test_form_admin_register(site: AdminSite):
    site.register_admin(TmpAdmin)

    with pytest.raises(AssertionError) as exc:
        site.get_admin_or_create(TmpAdmin)
    assert exc.match("schema is None")


async def test_form_admin_route_submit(site: AdminSite, async_client: AsyncClient):
    site.register_admin(TmpAdmin1)

    ins = site.get_admin_or_create(TmpAdmin1)

    site.register_router()
    # test form amis json
    res = await async_client.post(ins.router_path + ins.page_path)
    assert res.json()["data"]["body"]["type"] == "form"
    assert res.json()["data"]["body"]["api"]["url"] == ins.router_path + ins.form_path
    assert res.text.find("username") and res.text.find("password")
    # test form api submit
    data = {"username": "admin", "password": "admin"}
    res = await async_client.post(ins.router_path + ins.form_path, json=data)
    assert res.json()["data"] == {
        "username": "admin",
        "password": "admin",
        "extra": "success",
    }


async def test_form_admin_route_init(site: AdminSite, async_client: AsyncClient):
    site.register_admin(TmpAdmin2)

    ins = site.get_admin_or_create(TmpAdmin2)

    site.register_router()
    # test form amis json
    res = await async_client.post(ins.router_path + ins.page_path)
    assert res.json()["data"]["body"]["type"] == "form"
    assert res.json()["data"]["body"]["initApi"]["url"] == ins.router_path + ins.form_path
    assert res.text.find("username") and res.text.find("password")
    # test form api init
    data = {"username": "admin", "password": "admin"}
    res = await async_client.get(ins.router_path + ins.form_path)
    assert res.json()["data"] == data
