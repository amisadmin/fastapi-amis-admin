# 用户认证

`FastAPI-Amis-Admin`以应用插件的方式为系统提供简单而强大的用户`RBAC`认证与授权.

项目地址: [FastAPI-User-Auth](https://github.com/amisadmin/fastapi_user_auth),更多教程文档及使用示例正在持续补充,

欢迎加入Q群[229036692](https://jq.qq.com/?_wv=1027&k=U4Dv6x8W)一起学习讨论.

## 安装

```bash
pip install fastapi-user-auth
```

## 简单示例

```python linenums="1" hl_lines="3 9 10 11 14"
from fastapi import FastAPI
from fastapi_amis_admin.admin import Settings
from fastapi_user_auth.site import AuthAdminSite

# 创建FastAPI应用
app = FastAPI()

# 创建AdminSite实例
site = AuthAdminSite(
    settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db')
)
auth = site.auth
# 挂载后台管理系统
site.mount_app(app)

# 创建初始化数据库表
@app.on_event("startup")
async def startup():
    await site.db.async_run_sync(SQLModel.metadata.create_all,is_session=False)
    # 创建默认测试用户, 请及时修改密码!!!
    await auth.create_role_user('admin')
    await auth.create_role_user('vip')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
```

!!! note "关于`AuthAdminSite`"

	- AuthAdminSite是FastAPI-User-Auth封装的一个默认授权管理站点类,它要求用户必须登录.
	- 通过AuthAdminSite注册的管理对象,默认权限与其一致(即:也要求用户必须登录).
	- 你可以通过重载`has_page_permission`方法,实现默认权限要求的升级或降级.

## 示例-1

需求: 现有一个用户管理应用,在要求用户登录的基础上,还需要当前登录的用户是管理员,其他非管理员用户禁止操作.

```python hl_lines="4"
class UserAuthApp(AdminApp):
    async def has_page_permission(self, request: Request) -> bool:
        return  await request.auth.requires(roles='admin', response=False)(request)
```

## 示例-2

需求: 在上例用户管理应用下,包含用户登录/注册表单管理对象,这部分路由并不需要用户处于登录状态.

```python  hl_lines="3"
class UserLoginFormAdmin(FormAdmin):
    async def has_page_permission(self, request: Request) -> bool:
        return True
```

## 示例-3

需求: 有一个`ModelAdmin`文章模型管理,权限要求如下:

- 所有文章全部公开,不需要用户登录也可以查看.
- 用户未登录,不可按标题过滤文章,并且最多每页最多只能查看10条数据.
- 用户已登录,并且注册时间大于3天,才可以发布文章.
- 用户已登录,并且只能修改自己的文章,并且不可批量修改.
- 管理员可以修改全部文章,并且可以批量修改.
- 必须管理员才可以删除文章.

```python linenums="1" hl_lines="32 33 41 42 49 60 65"
class ArticleAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label='文章管理', icon='fa fa-file')
    model = Article
    # 配置列表展示字段
    list_display = [Article.id, Article.title, Article.img, Article.status,
                    Category.name, User.username,
                    TableColumn(type='tpl', label='自定义模板列',
                                tpl='<a href="${source}" target="_blank">ID:${id},Title:${title}</a>'),
                    Article.create_time, Article.description,
                    ]
    # 配置模糊搜索字段
    search_fields = [Article.title, Category.name, User.username]
    # 配置关联模型
    link_model_fields = [Article.tags]

    # 自定义查询选择器
    async def get_select(self, request: Request) -> Select:
        sel = await super().get_select(request)
        return sel.join(Category, isouter=True).join(User, isouter=True)

    # 权限验证
    async def has_page_permission(self, request: Request) -> bool:
        return True

    async def has_list_permission(
            self, request: Request, paginator: Paginator,
            filter: BaseModel = None, **kwargs
    ) -> bool:
        # 用户未登录,不可按标题过滤文章,并且最多每页最多只能查看10条数据.
        return bool(
            await self.site.auth.requires(response=False)(request)
            or (paginator.perPage <= 10 and filter.title == '')
        )

    async def has_create_permission(
            self, request: Request, data: BaseModel, **kwargs
    ) -> bool:
        # 用户已登录,并且注册时间大于3天,才可以发布文章; 或admin角色
        return bool(
            await self.site.auth.requires(response=False)(request)
            and request.user.create_time < datetime.now() - timedelta(days=3)
        ) or await self.site.auth.requires(roles='admin', response=False)(request)

    async def has_delete_permission(
            self, request: Request, item_id: List[str], **kwargs
    ) -> bool:
        # 必须管理员才可以删除文章.
        return await self.site.auth.requires(roles='admin', response=False)(request)

    async def has_update_permission(
            self, request: Request, item_id: List[str], 
        	data: BaseModel, **kwargs
    ) -> bool:
        if await self.site.auth.requires(response=False)(request):
            if item_id is None:
                return True
            async with self.site.db.session_maker() as session:
                # 管理员可以修改全部文章, 并且可以批量修改.
                if await request.user.has_role(['admin'], session):
                    return True
                # 非管理员,只能修改自己的文章,并且不可批量修改.
                result = await session.execute(
                    select(Article.id).where(
                        Article.id == item_id[0], Article.user_id == request.user.id
                    ).limit(1)
                )
            if result.first():
                return True
        return False

    async def on_create_pre(
            self, request: Request, obj: BaseModel, **kwargs
    ) -> Dict[str, Any]:
        data = await super().on_create_pre(request, obj, **kwargs)
        # 创建新文章时,设置当前用户为发布者
        data['user_id'] = request.user.id
        return data
```

## 界面预览

- Open `http://127.0.0.1:8000/admin/auth/form/login` in your browser:

![Login](https://s2.loli.net/2022/03/20/SZy6sjaVlBT8gin.png)

- Open `http://127.0.0.1:8000/admin/` in your browser:

![ModelAdmin](https://s2.loli.net/2022/03/20/ItgFYGUONm1jCz5.png)

- Open `http://127.0.0.1:8000/admin/docs` in your browser:

![Docs](https://s2.loli.net/2022/03/20/1GcCiPdmXayxrbH.png)

