# 快速开始

## 安装

```bash
pip install fastapi_amis_admin
```



## 简单示例

1.创建文件**`adminsite.py`**:

```python
from fastapi_amis_admin.amis_admin.settings import Settings
from fastapi_amis_admin.amis_admin.site import AdminSite
from fastapi_amis_admin.amis_admin import admin

# 创建AdminSite实例
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///admisadmin.db'))

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
    uvicorn.run(app,debug=True)
```



## 运行程序

```bash
uvicorn main:app
```



## 更多功能

- API参考文档: [API Reference](../../amis_admin/BaseAdmin)

- 示例程序: [amisadmin/fastapi_amis_admin_demo (github.com)](https://github.com/amisadmin/fastapi_amis_admin_demo)
