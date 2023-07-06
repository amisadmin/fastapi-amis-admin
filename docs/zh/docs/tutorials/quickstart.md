# 快速开始

## 安装

```bash
pip install fastapi_amis_admin
```

## 简单示例

1.创建文件**`adminsite.py`**:

```python
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.amis.components import PageSchema

# 创建AdminSite实例
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))


# 注册管理类
@site.register_admin
class GitHubIframeAdmin(admin.IframeAdmin):
    # 设置页面菜单信息
    page_schema = PageSchema(label='AmisIframeAdmin', icon='fa fa-github')
    # 设置跳转链接
    src = 'https://github.com/amisadmin/fastapi_amis_admin'
```

2.创建文件**`main.py`**:

```python
from fastapi import FastAPI
from adminsite import site

app = FastAPI()

# 挂载后台管理系统
site.mount_app(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
```

## 运行程序

```bash
uvicorn main:app
```

## 界面预览

- 打开浏览器访问: `http://127.0.0.1:8000/admin/`

## 示例程序

- [`FastAPI-Amis-Admin-Demo`](https://github.com/amisadmin/fastapi_amis_admin_demo):  一个`FastAPI-Amis-Admin` 应用程序示例.
- [`FastAPI-User-Auth-Demo`](https://github.com/amisadmin/fastapi_user_auth_demo): 一个`FastAPI-User-Auth` 应用程序示例.

## 相关项目

- [`FastAPI-User-Auth`](https://github.com/amisadmin/fastapi_user_auth): 一个简单而强大的`FastAPI`用户`RBAC`认证与授权库.
- [`FastAPI-Scheduler`](https://github.com/amisadmin/fastapi_scheduler): 一个基于`FastAPI`+`APScheduler`的简单定时任务管理项目.

## 更多功能

- API参考文档: [API Reference](../../amis_admin/BaseAdmin)