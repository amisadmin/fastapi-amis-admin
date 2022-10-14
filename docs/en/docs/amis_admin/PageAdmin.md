## PageAdmin

- Amis page management

### Inherit from base class

- #### [PageSchemaAdmin](../PageSchemaAdmin)

- #### [RouterAdmin](../RouterAdmin)

### fields

#### page

- Amis page displays the main Page object
- Reference: [Page](https://baidu.gitee.io/amis/zh-CN/components/page)

#### page_path

- Page path, the default is: class module name + class name

#### page_response_mode

page response type, default: `json`

- `json`: The response format is parsed as json. That is `page.amis_dict()`
- `html`: The response format is parsed as amis html. That is `page.amis_html()`

#### page_route_kwargs

- page additional parameters

#### template_name

- Page rendering template name.

#### route_page

- Page routing function

```python
  @property
  def route_page(self)->Callable
```

### method

#### page_permission_depend

- The current page routing permission detection dependency.

```python
 async def page_permission_depend(self, request: Request) -> bool
```

#### get_page

- Get the amis page Page object.

```python
 async def get_page(self, request: Request) -> Page
```

#### page_parser

- Parse the Page object into response data.

```python
 def page_parser(self, request: Request, page: Page) -> Response
```

 