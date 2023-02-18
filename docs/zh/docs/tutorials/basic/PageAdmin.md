# 页面管理

`fastapi-amis-admin`支持多种类型页面管理,几乎可以实现任何复杂的后台管理页面场景.

- 本教程的示例都默认你已经完成第一步[quickstart](/quickstart).即: 已经定义管理站点对象`site`并且成功运行项目.
- 如果你注册的管理对象无法显示,请检查是否在`site.mount_app(app)`之前导入对应的模块.

## 页面管理

`PageAdmin`实现在菜单列表显示一个菜单.点击菜单后将展现一个`amis`页面.
你可以通过阅读[`baidu-amis`官方文档](https://baidu.gitee.io/amis/zh-CN/components/page)
,实现各种复杂的页面展示.先看一个Hello World页面示例吧.

```python
@site.register_admin
class HelloWorldPageAdmin(admin.PageAdmin):
    page_schema = 'Hello World Page'
    # 通过page类属性直接配置页面信息;
    page = Page(title='标题', body='Hello World!')
```

非常简单吧,接下来再实现一个获取当前时间的页面.

```python
@site.register_admin
class CurrentTimePageAdmin(admin.PageAdmin):
    page_schema = 'Current Time Page'

    # 通过get_page类方法实现动态获取页面信息.
    async def get_page(self, request: Request) -> Page:
        page = await super().get_page(request)
        page.body = '当前时间是: ' + time.strftime('%Y-%m-%d %H:%M:%S')
        return page
```

在这个示例中并没有通过`page`对象配置静态的页面信息,而是通过`get_page`方法动态获取信息,
在`fastapi-amis-admin`中会有很多类似的实现,如果你需要动态配置某些信息,
都建议你通过重载对应的方法实现,但是建议在大多数情况下,请先调用父类的方法.

!!! note annotate "使用符合Amis语法的Json注册管理页面"

```python
@site.register_admin
class AmisPageAdmin(admin.PageAdmin):
    page_schema = 'Amis Json Page'
    page = Page.parse_obj(
        {
            "type": "page",
            "title": "表单页面",
            "body": {
                "type": "form",
                "mode": "horizontal",
                "api": "/saveForm",
                "body": [
                    {
                        "label": "Name",
                        "type": "input-text",
                        "name": "name"
                    },
                    {
                        "label": "Email",
                        "type": "input-email",
                        "name": "email"
                    }
                ]
            }
        }
    )
```

## 链接管理

`LinkAdmin`实现在菜单列表显示一个链接跳转菜单.点击菜单后将通过打开一个新的浏览器标签,访问设置的链接:

```python
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.amis import PageSchema


@site.register_admin
class GitHubLinkAdmin(admin.LinkAdmin):
    # 通过page_schema类属性设置页面菜单信息;
    # PageSchema组件支持属性参考: https://baidu.gitee.io/amis/zh-CN/components/app
    page_schema = PageSchema(label='AmisLinkAdmin', icon='fa fa-github')
    # 设置跳转链接
    link = 'https://github.com/amisadmin/fastapi_amis_admin'
```

上面的示例是一个最简单的页面管理类, 主要做了下面几步:

1. 定义一个页面管理类, 继承`admin.LinkAdmin`. 关于内置的`BaseAdmin`基类,可以参考: [BaseAdmin](/amis_admin/BaseAdmin)
2. 通过 `page_schema`字段配置菜单信息.这里只配置了菜单的标签和图标, 你可以阅读相关的文档,配置更多自定义信息.
3. 通过`link`字段指定需要跳转的链接.
2. 最后一步, 你必须通过`site.register_admin`装饰器,将管理类注册到管理站点.

## 内嵌框架管理

`IframeAdmin`实现在菜单列表显示一个菜单.点击菜单后将通过在当前页面内嵌一个框架,访问设置的链接. 使用方法与`LinkAdmin`
非常相似,不同的仅仅是链接的打开方式.

```python
@site.register_admin
class ReDocsAdmin(admin.IframeAdmin):
    # 设置页面菜单信息
    page_schema = PageSchema(label='Redocs', icon='fa fa-book')

    # 设置跳转链接
    @property
    def src(self):
        return self.app.site.settings.site_url + '/redoc'
```

上面的示例是一个配置更加细致的`IframeAdmin`页面管理类,它完成了以下工作:

1.  通过`src`动态字段,设置`Iframe`跳转的链接.

!!! note annotate "关于 `self.app.site.settings.site_url`"

    表示: 当前类实例所在管理站点的根路径.看似比较复杂,事实上非常容易理解,并且可能在以后的开发中非常有用.
    建议先简单阅读一遍 [BaseAdmin](/amis_admin/BaseAdmin) 了解`amis-admin`的架构以及常用管理类对象所拥有的字段与方法,这将会非常有利于以后的开发与应用.

