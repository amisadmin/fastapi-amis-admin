## Project Debugging

## IDE debugging

All IDE debugging is turned on by default and can be turned off in the following ways.

1. Global debugging configuration via the ``debug`'' property in the ``Settings`' object

```python
site = AdminSite(settings=Settings(debug=False, database_url_async='sqlite+aiosqlite:///amisadmin.db'))
```

2. Customize `FastAPI` object and turn off `debug`

```python
site = AdminSite(settings=Settings(debug=False, database_url_async='sqlite+aiosqlite:///amisadmin.db'),
                 fastapi=FastAPI(debug=False))
```

3.Customize `AsyncEngine` object and turn off `debug`

```python
site = AdminSite(settings=Settings(debug=False),
                 engine=create_async_engine('sqlite+aiosqlite:///amisadmin.db', echo=False, future=True))
```

## ApiDocs

`fastapi` can automatically generate two interactive documents, and all the interfaces of `fastapi-amis-admin` can be debugged online via docs documents.

### Main application

- `/docs`

- `/redoc`

### admin

- `/admin/docs`

- `/admin/redoc`

## Amis debugging

`amis` has a built-in debugging tool that allows you to view the internal running logs of the component for easy analysis of problems.

### Enabling method

This feature is not enabled by default, and can be enabled in the following two ways.

1. configure the global variable `enableAMISDebug` with a value of `true`, for example `window.enableAMISDebug = true`.
2. Add `amisDebug=1` to the page URL parameter, such as `https://demo.amis.work/admin/?amisDebug=1`

After turning on, it will be displayed on the right side of the page.

### Current features

The Debug tool currently provides two functions. 1:

1. run logs, mainly api and data conversion logs
2. View the component data chain, after the Debug tool is expanded, click on any component to see the component's data chain

## Amis visual editor

- Project URL: [https://github.com/aisuda/amis-editor-demo](https://github.com/aisuda/amis-editor-demo)


- Online demo: http://aisuda.github.io/amis-editor-demo


