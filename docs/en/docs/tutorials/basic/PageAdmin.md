# Page Management

`fastapi-amis-admin` supports many types of page management, allowing you to implement almost any complex backend page management scenario.

- The examples in this tutorial all default to you having completed the first step [quickstart](/quickstart). That is: have defined the management site object `site` and successfully run the project.
- If your registered administrative object is not displayed, please check if you have imported the corresponding module before `site.mount_app(app)`.

## Page Management

`PageAdmin` implements to display a menu in the menu list. Clicking on the menu will display an `amis` page.
You can read the [`baidu-amis` official documentation](https://baidu.gitee.io/amis/zh-CN/components/page)
to implement various complex page displays. First look at a Hello World page example it .

```python
@site.register_admin
class HelloWorldPageAdmin(admin.PageAdmin):
    page_schema = 'Hello World Page'
    # Configure page information directly through the page class property;
    page = Page(title='Title', body='Hello World!')
```

Very simple, right, then implement a page to get the current time.

```python
@site.register_admin
class CurrentTimePageAdmin(admin.PageAdmin):
    page_schema = 'Current Time Page'

    # Get page information dynamically via get_page class method.
    async def get_page(self, request: Request) -> Page:
        page = await super().get_page(request)
        page.body = 'The current time is: ' + time.strftime('%Y-%m-%d %H:%M:%S')
        return page
```

In this example, instead of configuring static page information through the `page` object, the information is obtained dynamically through the `get_page` method,
There are many similar implementations in `fastapi-amis-admin`, if you need to dynamically configure certain information,
It is recommended that you do this by overloading the corresponding methods, but it is recommended that in most cases, please call the methods of the parent class first.

!!! note annotate "Register admin page with Amis syntax compliant Json"

```python
@site.register_admin
class AmisPageAdmin(admin.PageAdmin):
    page_schema = 'Amis Json Page'
    page = Page.parse_obj(
        {
            "type": "page",
            "title": "form page",
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

## Link Admin

`LinkAdmin` implements a link jumping menu in the menu list. Clicking on the menu will access the set link by opening a new browser tab:

```python
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.amis import PageSchema


@site.register_admin
class GitHubLinkAdmin(admin.LinkAdmin):
    # Set the page menu information via the page_schema class property;
    # PageSchema component support properties reference: https://baidu.gitee.io/amis/zh-CN/components/app
    page_schema = PageSchema(label='AmisLinkAdmin', icon='fa fa-github')
    # Set the jump link
    link = 'https://github.com/amisadmin/fastapi_amis_admin'
```

The above example is a simple page admin class, which does the following steps. 1:

1. Define a page admin class, inheriting from `admin.LinkAdmin`. About the built-in `BaseAdmin` base class, see: [BaseAdmin](/amis_admin/BaseAdmin)
2. configure the menu information through the `page_schema` field. Here only configure the menu label and icon, you can read the relevant documentation, configure more custom information. 3.
3. specify the links to jump to via the `link` field. 2.
The last step, you must register the administrative class to the administrative site through the `site.register_admin` decorator.

## Iframe Admin

The `IframeAdmin` implementation displays a menu in the menu list. Click on the menu will be embedded in the current page through a frame, access to set the link. Usage is very similar to `LinkAdmin`, the only difference is the way the link is opened.

```python
@site.register_admin
class ReDocsAdmin(admin.IframeAdmin):
    # Set page menu information
    page_schema = PageSchema(label='Redocs', icon='fa fa-book')

    # Set the jump link
    @property
    def src(self):
        return self.app.site.settings.site_url + '/redoc'
```

The above example is a more carefully configured `IframeAdmin` page administration class that does the following:

1.  set the `Iframe` jump link through the `src` dynamic field.

!!! note annotate "about `self.app.site.settings.site_url`"

    means: the root path of the administrative site where the current class instance is located. Seems complicated, but in fact it is very easy to understand and may be useful in future development.
    It is recommended to read through [BaseAdmin](/amis_admin/BaseAdmin) to understand the architecture of `amis-admin` and the common administrative class objects have fields and methods, which will be very useful for future development and application.

