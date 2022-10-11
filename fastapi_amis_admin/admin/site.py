import os.path
import platform
import time
import uuid

import aiofiles
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

import fastapi_amis_admin
from fastapi_amis_admin import amis
from fastapi_amis_admin.admin import AdminApp, admin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.amis.components import Page, PageSchema, Property
from fastapi_amis_admin.crud.schema import BaseApiOut
from fastapi_amis_admin.crud.utils import SqlalchemyDatabase
from fastapi_amis_admin.utils.translation import i18n as _


class DocsAdmin(admin.IframeAdmin):
    group_schema = PageSchema(label="APIDocs", icon="fa fa-book", sort=-100)
    page_schema = PageSchema(label="AdminDocs", icon="fa fa-book")

    @property
    def src(self):
        return self.app.site.router_path + self.app.site.fastapi.docs_url


class ReDocsAdmin(admin.IframeAdmin):
    group_schema = PageSchema(label="APIDocs", icon="fa fa-book", sort=-100)
    page_schema = PageSchema(label="AdminRedocs", icon="fa fa-book")

    @property
    def src(self):
        return self.app.site.router_path + self.app.site.fastapi.redoc_url


class HomeAdmin(admin.PageAdmin):
    group_schema = None
    page_schema = PageSchema(label=_("Home"), icon="fa fa-home", url="/home", isDefaultPage=True, sort=100)
    page_path = "/home"

    async def get_page(self, request: Request) -> Page:
        page = await super().get_page(request)
        page.body = [
            Property(
                title="SiteInfo",
                column=4,
                items=[
                    Property.Item(label="title", content=self.site.settings.site_title),
                    Property.Item(label="version", content=self.site.settings.version),
                    Property.Item(label="language", content=self.site.settings.language),
                    Property.Item(label="debug", content=str(self.site.settings.debug)),
                ],
            ),
            amis.Divider(),
            Property(
                title="FastAPI-Amis-Admin",
                column=4,
                items=[
                    Property.Item(label="system", content=platform.system()),
                    Property.Item(label="python", content=platform.python_version()),
                    Property.Item(label="version", content=fastapi_amis_admin.__version__),
                    Property.Item(label="license", content="Apache2.0"),
                    Property.Item(label="amis-cdn", content=self.site.settings.amis_cdn),
                    Property.Item(label="amis-pkg", content=self.site.settings.amis_pkg),
                    Property.Item(label="amis-theme", content=self.site.settings.amis_theme),
                ],
            ),
        ]
        return page


class FileAdmin(admin.RouterAdmin):
    # todo perfect: Limit file size/suffixes/content_type
    file_directory: str = "upload"
    file_path: str = "/upload"
    file_max_size: int = 2 * 1024 * 1024
    router_prefix = "/file"

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.file_directory = self.file_directory or self.file_path
        self.static_path = self.mount_staticfile()

    def get_filename(self, file: UploadFile):
        filename = str(uuid.uuid4()).replace("-", "") + os.path.splitext(file.filename)[1]
        return os.path.join(time.strftime("%Y%m"), filename)

    def mount_staticfile(self) -> str:
        os.path.exists(self.file_directory) or os.makedirs(self.file_directory)
        self.app.site.fastapi.mount(
            self.file_path,
            StaticFiles(directory=self.file_directory),
            self.file_directory,
        )
        return self.app.site.router_path + self.file_path

    def register_router(self):
        @self.router.post(self.file_path, response_model=BaseApiOut[self.UploadOutSchema])
        async def file_upload(file: UploadFile = File(...)):
            filename = self.get_filename(file)
            file_path = os.path.join(self.file_directory, filename)
            file_dir = os.path.dirname(file_path)
            os.path.exists(file_dir) or os.makedirs(file_dir)
            try:
                res = await file.read()
                if self.file_max_size and len(res) > self.file_max_size:
                    return BaseApiOut(status=-2, msg="The file size exceeds the limit")
                async with aiofiles.open(file_path, "wb") as f:
                    await f.write(res)
                return BaseApiOut(
                    data=self.UploadOutSchema(filename=filename, url=f"{self.static_path}/{filename}"),
                )

            except Exception as e:
                return BaseApiOut(status=-1, msg=str(e))

    class UploadOutSchema(BaseModel):
        filename: str = None
        url: str = None


class AdminSite(admin.BaseAdminSite):
    def __init__(
        self,
        settings: Settings,
        fastapi: FastAPI = None,
        engine: SqlalchemyDatabase = None,
    ):
        super().__init__(settings, fastapi, engine)
        self.register_admin(HomeAdmin, DocsAdmin, ReDocsAdmin, FileAdmin)
