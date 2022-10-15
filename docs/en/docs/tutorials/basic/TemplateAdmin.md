# Template Management

In some cases, the `amis` page may not be convenient to achieve your complex interface display, or you prefer to use the template rendering way to display the administrative page. Then you can use `TemplateAdmin` to achieve your needs.

## Example

```python
@site.register_admin
class SimpleTemplateAdmin(admin:)
    page_schema = PageSchema(label='SimpleTemplate', icon='fa fa-link')
    templates: Jinja2Templates = Jinja2Templates(directory='templates')
    template_name = 'simple.html'

    async def get_page(self, request: Request) -> Dict[str, Any]:
        return {'current_time': datetime.datetime.now()}
```

## Configuring the template engine

Configure the Jinja2 template engine via the `templates` field.

## Configure template files

Configure the Jinja2 template file via the `template_name` field.

## Page rendering data

Get page rendering data via the `get_page` method.

## More usage

### Related documentation

- [TemplateAdmin](/amis_admin/TemplateAdmin/)

- [fastapi_amis_admin_demo](https://github.com/amisadmin/fastapi_amis_admin_demo/)