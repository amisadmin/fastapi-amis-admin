import os
from typing import Any, Dict

from httpx import AsyncClient
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from fastapi_amis_admin import admin, amis
from fastapi_amis_admin.admin import AdminSite
from fastapi_amis_admin.amis import Page


async def test_BaseAdmin(site: AdminSite):
    @site.register_admin
    class TmpAdmin(admin.BaseAdmin):
        pass

    ins = site.get_admin_or_create(TmpAdmin)
    assert ins.site is site
    assert ins.unique_id


async def test_PageSchemaAdmin(site: AdminSite):
    @site.register_admin
    class TmpAdmin(admin.PageSchemaAdmin):
        pass

    ins = site.get_admin_or_create(TmpAdmin)
    assert ins.page_schema

    @site.register_admin
    class TmpAdmin1(admin.PageSchemaAdmin):
        page_schema = "page_label"

    ins = site.get_admin_or_create(TmpAdmin1)

    assert isinstance(ins.page_schema, amis.PageSchema) and ins.page_schema.label == "page_label"

    @site.register_admin
    class TmpAdmin2(admin.PageSchemaAdmin):
        page_schema = amis.PageSchema(label="page_label", isDefaultPage=True, sort=100)

    ins = site.get_admin_or_create(TmpAdmin2)

    assert isinstance(ins.page_schema, amis.PageSchema) and ins.page_schema.label == "page_label"


async def test_LinkAdmin(site: AdminSite):
    @site.register_admin
    class TmpAdmin(admin.LinkAdmin):
        link = "https://docs.amis.work"

    ins = site.get_admin_or_create(TmpAdmin)
    assert ins.page_schema.link == "https://docs.amis.work"


async def test_IframeAdmin(site: AdminSite):
    @site.register_admin
    class TmpAdmin(admin.IframeAdmin):
        src = "https://docs.amis.work"

    ins = site.get_admin_or_create(TmpAdmin)
    assert isinstance(ins.page_schema.schema_, amis.Iframe) and ins.page_schema.schema_.src == "https://docs.amis.work"


async def test_RouterAdmin(site: AdminSite, async_client: AsyncClient):
    @site.register_admin
    class TmpAdmin(admin.RouterAdmin):
        router_prefix = "/router"

        def register_router(self):
            @self.router.get("/hello")
            def hello():
                return {"username": "hello"}

    ins = site.get_admin_or_create(TmpAdmin)
    assert ins.router_path == f"{site.settings.site_path}/router"

    site.register_router()
    res = await async_client.get("/router/hello")
    assert res.json() == {"username": "hello"}


async def test_PageAdmin(site: AdminSite, async_client: AsyncClient):
    @site.register_admin
    class TmpAdmin(admin.PageAdmin):
        page_path = "/test"

        async def get_page(self, request: Request) -> Page:
            return Page(title="hello", body="Test Amis Page")

    ins = site.get_admin_or_create(TmpAdmin)
    assert ins.page_path == "/test"
    assert ins.page_schema.url == ins.router_path + ins.page_path

    site.register_router()
    # test amis json
    res = await async_client.post(ins.router_path + ins.page_path)
    assert res.json()["data"] == {
        "type": "page",
        "title": "hello",
        "body": "Test Amis Page",
    }
    # test amis html
    res = await async_client.get(ins.router_path + ins.page_path)
    assert res.text.find(Page(title="hello", body="Test Amis Page").amis_json())
    # test amis json _update
    res = await async_client.post(
        ins.router_path + ins.page_path,
        json={"_update": {"title": "new title", "extra": "extra data"}},
    )
    assert res.json()["data"] == {
        "type": "page",
        "title": "new title",
        "body": "Test Amis Page",
        "extra": "extra data",
    }


async def test_TemplateAdmin(site: AdminSite, async_client: AsyncClient, tmpdir):
    path = os.path.join(tmpdir, "index.html")
    with open(path, "w") as file:
        file.write("<html>Hello,{{ username }}</html>")

    @site.register_admin
    class TmpAdmin(admin.TemplateAdmin):
        page_path = "/index"
        templates = Jinja2Templates(directory=str(tmpdir))
        template_name = "index.html"

        async def get_page(self, request: Request) -> Dict[str, Any]:
            return {"username": "hello"}

    ins = site.get_admin_or_create(TmpAdmin)
    assert ins.page_path == "/index"
    assert ins.page_schema.url == ins.router_path + ins.page_path
    assert isinstance(ins.page_schema.schema_, amis.Iframe) and ins.page_schema.schema_.src == ins.page_schema.url
    site.register_router()

    # test jinja2 html
    res = await async_client.get(ins.router_path + ins.page_path)
    assert res.text == "<html>Hello,hello</html>"
