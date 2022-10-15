## TemplateAdmin

- `Jinja2` rendering template management
- Reference: [Jinja](https://jinja.palletsprojects.com/)

### Inherit from base class

- #### [PageAdmin](../PageAdmin)

### fields

#### page

- The current page context context dictionary.

#### templates

- `Jinja2Templates` template renderer

### method

#### get_page

- Get the context dictionary of the current page context.

```python
async def get_page(self, request: Request) -> Dict[str, Any]
```

#### page_parser

- Parse the page dictionary into response data.

```python
def page_parser(self, request: Request, page: Dict[str, Any])-> Response:
    page.update({'request': request})
    return self.templates.TemplateResponse(self.template_name, page)
```

 