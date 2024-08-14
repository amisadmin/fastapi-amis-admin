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

我们仍旧基于第一节[快速开始](/tutorials/quickstart)中创建的`adminsite.py`来修改。

1、首先注释(或删除)掉`site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))`
2、在`templates`目录中创建`new_app.html`模板文件（如果指定了模板文件而模板文件内容为空的话，后台将显示空白），html内容如下：
```html
<!DOCTYPE html>
<html lang="">
<head>
    <meta charset="UTF-8"/>
    <title>${site_title} - 这里是自定义的后台首页</title>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    <meta content="width=device-width, initial-scale=1, maximum-scale=1" name="viewport"/>
    <meta content="IE=Edge" http-equiv="X-UA-Compatible"/>
    <!-- 可以自由替换静态资源的链接以加快访问速度。 -->
    <link href="${site_icon}" rel="shortcut icon" type="image/x-icon"/>
    <link href="${cdn}/${pkg}/sdk/sdk.css" rel="stylesheet" title="default"/>
    <link href="${cdn}/${pkg}/sdk/helper.css" rel="stylesheet"/>
    <link href="${cdn}/${pkg}/sdk/iconfont.css" rel="stylesheet"/>
    ${theme_css}
    <script src="${cdn}/${pkg}/sdk/sdk.js"></script>
    <script src="${cdn}/vue@2.7.14/dist/vue.min.js"></script>
    <script src="${cdn}/history@5.3.0/umd/history.production.min.js"></script>
    <!-- 可以自由修改样式文件以实现不同的显示效果。 -->
    <style>
        html, body,
        .app-wrapper {
            position: relative;
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
        }

        /*DropDownButton组件下拉菜单样式修改*/
        .amis-scope .cxd-DropDown-menu {
            min-width: 100%;
            text-align: center;
        }
    </style>
</head>
<body>
<div class="app-wrapper" id="root"></div>
<script>
    (function () {
        let amis = amisRequire('amis/embed');
        const match = amisRequire('path-to-regexp').match;

        // 如果想用 browserHistory 请切换下这处代码, 其他不用变
        // const history = HistoryLibrary.createBrowserHistory();
        const history = HistoryLibrary.createHashHistory();
        const app = ${AmisSchemaJson};

        function normalizeLink(to, location = history.location) {
            to = to || '';

            if (to && to[0] === '#') {
                to = location.pathname + location.search + to;
            } else if (to && to[0] === '?') {
                to = location.pathname + to;
            }

            const idx = to.indexOf('?');
            const idx2 = to.indexOf('#');
            let pathname = ~idx ? to.substring(0, idx) : ~idx2 ? to.substring(0, idx2) : to;
            let search = ~idx ? to.substring(idx, ~idx2 ? idx2 : undefined) : '';
            let hash = ~idx2 ? to.substring(idx2) : location.hash;
            if (!pathname) {
                pathname = location.pathname;
            } else if (pathname[0] != '/' && !/^https?\:\/\//.test(pathname)) {
                let relativeBase = location.pathname;
                const paths = relativeBase.split('/');
                paths.pop();
                let m;
                while ((m = /^\.\.?\//.exec(pathname))) {
                    if (m[0] === '../') {
                        paths.pop();
                    }
                    pathname = pathname.substring(m[0].length);
                }
                pathname = paths.concat(pathname).join('/');
            }
            return pathname + search + hash;
        }

        function isCurrentUrl(to, ctx) {
            if (!to) {
                return false;
            }
            const pathname = history.location.pathname;
            const link = normalizeLink(to, {
                ...location,
                pathname,
                hash: ''
            });

            if (!~link.indexOf('http') && ~link.indexOf(':')) {
                let strict = ctx && ctx.strict;
                return match(link, {
                    decode: decodeURIComponent,
                    strict: typeof strict !== 'undefined' ? strict : true
                })(pathname);
            }

            return decodeURI(pathname) === link;
        }

        let amisInstance = amis.embed(
            '#root',
            app,
            {location: history.location, locale: "${locale}"},
            {
                // watchRouteChange: fn => {
                //   return history.listen(fn);
                // },
                updateLocation: (location, replace) => {
                    location = normalizeLink(location);
                    if (location === 'goBack') {
                        return history.goBack();
                    } else if (
                        (!/^https?\:\/\//.test(location) &&
                            location ===
                            history.location.pathname + history.location.search) ||
                        location === history.location.href
                    ) {
                        // 目标地址和当前地址一样，不处理，免得重复刷新
                        return;
                    } else if (/^https?\:\/\//.test(location) || !history) {
                        return (window.location.href = location);
                    }

                    history[replace ? 'replace' : 'push'](location);
                },
                jumpTo: (to, action) => {
                    if (to === 'goBack') {
                        return history.goBack();
                    }

                    to = normalizeLink(to);

                    if (isCurrentUrl(to)) {
                        return;
                    }

                    if (action && action.actionType === 'url') {
                        action.blank === false
                            ? (window.location.href = to)
                            : window.open(to, '_blank');
                        return;
                    } else if (action && action.blank) {
                        window.open(to, '_blank');
                        return;
                    }

                    if (/^https?:\/\//.test(to)) {
                        window.location.href = to;
                    } else if (
                        (!/^https?\:\/\//.test(to) &&
                            to === history.pathname + history.location.search) ||
                        to === history.location.href
                    ) {
                        // do nothing
                    } else if (location.hash && to.indexOf("?") > -1) {
                        //如果当前页面有hash，且跳转的页面有参数，将hash拼接到参数后面
                        const [hash, search] = to.split("?");
                        window.location.href = location.pathname + "?" + search + "#" + hash;
                    } else {
                        history.push(to);
                    }
                },
                isCurrentUrl: isCurrentUrl,
                theme: "${theme}"
            }
        );

        history.listen(state => {
            amisInstance.updateProps({
                location: state.location || state,
                locale: "${locale}"
            });
        });
    })();
</script>
</body>
</html>

```

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
        super().__init__(settings, fastapi=fastapi, engine=engine)
        # 取消注册默认管理类
        self.unregister_admin(DocsAdmin, ReDocsAdmin)

    async def get_page(self, request: Request) -> App:
        app = await super().get_page(request)
        # 自定义站点名称,logo信息, 参考: https://baidu.gitee.io/amis/zh-CN/components/app
        app.brandName = 'MyAdminSite'
        app.logo = "https://baidu.gitee.io/amis/static/favicon_b3b0647.png"
        return app


# 通过自定义管理站点类创建后台管理系统实例
site = NewAdminSite(settings=Settings(debug=True, database_url_async='sqlite+aiosqlite:///amisadmin.db'))
```

- 通过修改`template_name`字段,你可以自定义后台界面模板. 例如: 修改静态资源链接以加快网络访问速度, 修改后台展示样式.

!!! note annotate "关于自定义管理站点"

    管理站点继承重写属于高级功能,建议对fastapi_amis_admin足够了解的情况下才进行重写.

    你可以自由修改后台管理界面,但是请尊重fastapi_amis_admin团队的开发成果,必须在展示界面中明确显示关于FastAPI-Amis-Admin的版权信息.

