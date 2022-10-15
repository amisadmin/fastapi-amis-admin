# 模板管理

在某些情况下,`amis`页面可能并不方便实现你的复杂界面展示,或者你更加倾向于使用模板渲染方式展示管理页面.这时你可以使用`TemplateAdmin`
实现你的需求.

## 示例

```python
@site.register_admin
class SimpleTemplateAdmin(admin.TemplateAdmin):
    page_schema = PageSchema(label='SimpleTemplate', icon='fa fa-link')
    templates: Jinja2Templates = Jinja2Templates(directory='templates')
    template_name = 'simple.html'

    async def get_page(self, request: Request) -> Dict[str, Any]:
        return {'current_time': datetime.datetime.now()}
```

## 配置模板引擎

通过`templates`字段配置Jinja2模板引擎.

## 配置模板文件

通过`template_name`字段配置Jinja2模板文件.

## 页面渲染数据

通过`get_page`方法获取页面渲染数据.

## 更多用法

### 相关文档

- [TemplateAdmin](/amis_admin/TemplateAdmin/)

- [fastapi_amis_admin_demo](https://github.com/amisadmin/fastapi_amis_admin_demo/)