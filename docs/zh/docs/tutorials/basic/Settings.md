# 站点配置

`AdminSite`在创建实例时,接收`settings`,`fastapi`,`engine`三个基本参数.
通过这三个基本参数,已经可以满足大部分自定义配置需求.
如果你需要更多个性化配置,你可以通过继承`AdminSite`类进行更多丰富配置.

## 基本配置

`settings`接收一个`Settings`对象,它可以配置当前站点是否开启调试、挂载路径、数据库连接、CDN地址、Amis版本号等.

- 参考: [Settings](/amis_admin/Settings/)

## FastAPI应用

`AdminSite`对象内部维护一个`fastapi`应用对象,通过`fastapi`参数,你可以配置:

- 是否开启调试
- api文档路径
- 启动/停止应用事件
- 注册依赖
- 其他FastAPI配置,参考: [FastAPI](https://fastapi.tiangolo.com/zh/tutorial/metadata/?h=docs_url#urls)

## 数据库配置

`AdminSite`对象内部还维护一个`sqlalchemy`客户端,你可以通过`engine`参数提供一个自定义同步/异步数据库引擎.

## 示例-1

```python
from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite

site = AdminSite(
    # 基本配置
    settings=Settings(debug=True, database_url_async='sqlite+aiosqlite:///amisadmin.db'),
    # fastapi相关配置
    fastapi=FastAPI(debug=True, docs_url='/admin_docs', redoc_url='/admin_redoc')
)
```

## 自定义管理站点

管理站点重写可以实现非常自由丰富的站点配置,例如更换后台界面模板,添加/删除默认管理类或管理应用,更换静态资源链接等等.

### 示例-2

```python
from fastapi import FastAPI, Request
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite, ReDocsAdmin, DocsAdmin
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi_amis_admin.amis.components import App


# 自定义后台管理站点
class NewAdminSite(AdminSite):
    # 自定义应用模板,复制原模板文件修改,原路径: fastapi_amis_admin/amis/templates/app.html
    template_name = '/templates/new_app.html'

    def __init__(self, settings: Settings, fastapi: FastAPI = None, engine: AsyncEngine = None):
        super().__init__(settings, fastapi, engine)
        # 取消注册默认管理类
        self.unregister_admin(DocsAdmin, ReDocsAdmin)

    async def get_page(self, request: Request) -> App:
        app = await super().get_page(request)
        # 自定义站点名称,logo信息, 参考: https://baidu.gitee.io/amis/zh-CN/components/app
        app.brandName = 'MyAdminSite'
        app.logo = 'https://baidu.gitee.io/amis/static/logo_408c434.png'
        return app


# 通过自定义管理站点类创建后台管理系统实例
site = NewAdminSite(settings=Settings(debug=True, database_url_async='sqlite+aiosqlite:///amisadmin.db'))
```

- 通过修改`template_name`字段,你可以自定义后台界面模板. 例如: 修改静态资源链接以加快网络访问速度, 修改后台展示样式.

!!! note annotate "关于自定义管理站点"

    管理站点继承重写属于高级功能,建议对fastapi_amis_admin足够了解的情况下才进行重写.
    
    你可以自由修改后台管理界面,但是请尊重fastapi_amis_admin团队的开发成果,必须在展示界面中明确显示关于FastAPI-Amis-Admin的版权信息.

