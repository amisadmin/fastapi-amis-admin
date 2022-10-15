# 项目调试

## IDE调试

默认会开启全部IDE调试，可以通过下面几种方式关闭：

1.通过`Settings`对象中的`debug`属性进行全局调试配置

```python
site = AdminSite(settings=Settings(debug=False, database_url_async='sqlite+aiosqlite:///amisadmin.db'))
```

2.自定义`FastAPI`对象,并且关闭`debug`

```python
site = AdminSite(
    settings=Settings(debug=False, database_url_async='sqlite+aiosqlite:///amisadmin.db'),
    fastapi=FastAPI(debug=False)
)
```

3.自定义`AsyncEngine`对象,并且关闭`debug`

```python
site = AdminSite(
    settings=Settings(debug=False),
    engine=create_async_engine('sqlite+aiosqlite:///amisadmin.db', echo=False, future=True)
)
```

## ApiDocs

`fastapi`可自动生成两个交互式文档,`fastapi-amis-admin`的全部接口都可以通过docs文档进行在线调试.

### 主应用

- `/docs`

- `/redoc`

### admin

- `/admin/docs`

- `/admin/redoc`

## Amis调试

`amis` 内置了调试工具，可以查看组件内部运行日志，方便分析问题。

### 开启方法

默认不会开启这个功能，可以通过下面两种方式开启：

1. 配置全局变量 `enableAMISDebug` 的值为 `true`，比如 `window.enableAMISDebug = true`。
2. 在页面 URL 参数中加上 `amisDebug=1`，比如 `https://demo.amis.work/admin/?amisDebug=1`

开启之后，在页面右侧就会显示。

### 目前功能

目前 Debug 工具提供了两个功能:

1. 运行日志，主要是 api 及数据转换的日志
2. 查看组件数据链，Debug 工具展开后，点击任意组件就能看到这个组件的数据链

## Amis可视化编辑器

- 项目地址: [https://github.com/aisuda/amis-editor-demo](https://github.com/aisuda/amis-editor-demo)


- 在线体验：http://aisuda.github.io/amis-editor-demo


