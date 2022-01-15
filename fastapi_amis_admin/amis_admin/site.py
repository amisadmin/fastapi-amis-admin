import os.path
import platform
import time
import uuid

from fastapi import UploadFile, File
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from fastapi_amis_admin.amis.components import PageSchema, Page, Property
from fastapi_amis_admin.amis_admin.admin import IframeAdmin, PageAdmin, AdminApp, RouterAdmin, \
    BaseAdminSite
from fastapi_amis_admin.fastapi_crud.schema import BaseApiOut


class DocsAdmin(IframeAdmin):
    group_schema = PageSchema(label='APIDocs', sort=-100)
    page_schema = PageSchema(label='docs', icon='fa fa-book')

    @property
    def src(self):
        return self.app.site.router_path + self.app.site.fastapi.redoc_url


class ReDocsAdmin(IframeAdmin):
    group_schema = PageSchema(label='APIDocs', sort=-100)
    page_schema = PageSchema(label='redocs', icon='fa fa-book')

    @property
    def src(self):
        return self.app.site.router_path + self.app.site.fastapi.redoc_url


class HomeAdmin(PageAdmin):
    group_schema = PageSchema(label='Home', sort=100)
    page_schema = PageSchema(label='Home', icon='fa fa-home', url='/home', isDefaultPage=True)
    page_path = '/home/amis.json'

    async def get_page(self, request: Request) -> Page:
        page = await super().get_page(request)
        os = platform.system()
        property = Property(title='机器配置', items=[
            Property.Item(label='os', content=os),
            Property.Item(label='cpu', content='2G'),
            Property.Item(label='memory', content='4G'),
            Property.Item(label='disk', content='80G'),
            Property.Item(label='memory', content='4G'),
        ])
        page.body = property
        return page


class FileAdmin(RouterAdmin):
    # todo perfect: Limit file size/suffixes/content_type
    file_directory: str = 'staticfile'
    file_path: str = '/staticfile'
    file_max_size: int = 1 * 1024 * 1024
    router_prefix = ''

    def __init__(self, app: "AdminApp"):
        super().__init__(app)
        self.file_directory = self.file_directory or self.file_path
        self.static_path = self.mount_staticfile()

    def get_filename(self, file: UploadFile):
        dir = time.strftime("%Y%m")
        filename = str(uuid.uuid4()).replace('-', '') + os.path.splitext(file.filename)[1]
        return os.path.join(dir, filename)

    def mount_staticfile(self) -> str:
        os.path.exists(self.file_directory) or os.makedirs(self.file_directory)
        self.app.site.fastapi.mount(self.file_path, StaticFiles(directory=self.file_directory), self.file_directory)
        return self.app.site.router_path + self.file_path

    def register_router(self):

        @self.router.post(self.file_path + "_upload", response_model=BaseApiOut[self.UploadOutSchema])
        async def file_upload(file: UploadFile = File(...)):
            filename = self.get_filename(file)
            file_path = os.path.join(self.file_directory, filename)
            file_dir = os.path.dirname(file_path)
            os.path.exists(file_dir) or os.makedirs(file_dir)
            try:
                res = await file.read()
                if self.file_max_size and len(res) > self.file_max_size:
                    return BaseApiOut(status=-2, msg='The file size exceeds the limit')
                with open(file_path, "wb") as f:
                    f.write(res)
                return BaseApiOut(data=self.UploadOutSchema(filename=filename,
                                                            url=self.static_path + '/' + filename))
            except Exception as e:
                return BaseApiOut(status=-1, msg=str(e))

    class UploadOutSchema(BaseModel):
        filename: str = None
        url: str = None


class AdminSite(BaseAdminSite):

    def on_register_router_pre(self):
        self.setup_admin(HomeAdmin, DocsAdmin, ReDocsAdmin, FileAdmin)
