## PageAdmin

- Amis页面管理

### 继承基类

- #### [PageSchemaAdmin](../PageSchemaAdmin)

- #### [RouterAdmin](../RouterAdmin)

### 字段

#### page

- Amis页面展示的Page对象
- 参考: [Page 页面](https://baidu.gitee.io/amis/zh-CN/components/page)

#### page_path

- 页面路径,默认为: 类模块名+类名

#### page_response_mode

页面响应类型, 默认: `json`

- `json`: 响应格式解析为json. 即 `page.amis_dict()`
- `html`: 响应格式解析为amis html. 即 `page.amis_html()`

#### page_route_kwargs

- 页面附加参数

#### template_name

- 页面渲染模板名称.

#### route_page

- 页面路由函数

```python
@property
def route_page(self) -> Callable
```

### 方法

#### page_permission_depend

- 当前页面路由权限检测依赖.

```python
 async def page_permission_depend(self, request: Request) -> bool
```

#### get_page

- 获取amis页面Page对象.

```python
 async def get_page(self, request: Request) -> Page
```

#### page_parser

- 将Page对象解析为响应数据.

```python
 def page_parser(self, request: Request, page: Page) -> Response
```

 
