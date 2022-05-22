## TemplateAdmin

- `Jinja2`渲染模板管理
- 参考: [Jinja](https://jinja.palletsprojects.com/)

### 继承基类

- #### [PageAdmin](../PageAdmin)

### 字段

#### page

- 当前页面context上下文字典.

#### templates

- `Jinja2Templates`模板渲染器

### 方法

#### get_page

- 获取当前页面context上下文字典.

```python
async def get_page(self, request: Request) -> Dict[str, Any]
```

#### page_parser

- 将page字典解析为响应数据.

```python
def page_parser(self, request: Request, page: Dict[str, Any])-> Response:
    page.update({'request': request})
    return self.templates.TemplateResponse(self.template_name, page)
```

 