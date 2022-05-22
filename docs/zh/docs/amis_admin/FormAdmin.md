## BaseFormAdmin

- 表单管理基类

### 继承基类

- #### [PageAdmin](../PageAdmin)

### 字段

#### schema

- 表单数据模型,必须设置.

#### schema_init_out

- 表单初始化返回数据模型

#### schema_submit_out

- 表单提交返回数据模型

#### form

- 当前表单amis Form对象.
- 参考: [Form 表单](https://baidu.gitee.io/amis/zh-CN/components/form/index)

#### form_path

- 表单提交和初始化数据接口api路由路径.

#### form_init

- 是否开启表单数据初始化.默认: `None`,不开启.

#### route_init

- 初始化表单路由

#### route_submit

- 提交表单路由

### 方法

#### get_form

- 获取当前页面Form表单对象.

```python
async def get_form(self, request: Request) -> Form
```

#### get_form_item

- 返回当前页面表单字段的`amis` `FormItem`对象.
- 参考: [FormItem 普通表单项](https://baidu.gitee.io/amis/zh-CN/components/form/formitem)

```python
async def get_form_item(self, request: Request, 
                  modelfield: ModelField) -> Union[FormItem, SchemaNode]
```

# FormAdmin

- 表单管理

### 继承基类

- ### [BaseFormAdmin](#baseformadmin)

### 方法

#### handle

处理页面表单提交数据.

- `request`: 当前请求对象.
- `data`: 用户提交的表单数据模型`schema`实例对象.

```python
async def handle(self, request: Request, data: BaseModel, **kwargs) -> BaseApiOut[Any]
```

#### get_init_data

获取页面表单初始化数据.

```python
async def get_init_data(self, request: Request, **kwargs) -> BaseApiOut[Any]
```





