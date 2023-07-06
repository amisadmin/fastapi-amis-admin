## SQLModelSelector

- SQLModel 选择器

### 字段

#### model

- 当前SQLModel ORM模型, 必须设置.

#### fields

查询字段列表.

- 支持SQLModel模型字段, 当前模型数据库表字段名
- 支持当前模型字段,和其它模型字段.
- 默认: `self.model`

#### exclude

排除字段列表.从当前模型中排除的字段列表.

- 支持当前SQLModel模型字段, 当前模型数据库表字段名
- 默认: []

#### ordering

- 选择器排序字段列表.
- 默认: []

#### link_models

- 链接模型字典.较复杂,详细解析待完善.

#### pk_name

- 当前模型主键字符串, 默认: `id`.
- 说明: **数据库表有且只能有一个自增加主键**.(待拓展)

#### pk

- 当前模型主键sqlalchemy InstrumentedAttribute.

#### parser

- 当前模型字段解析器.
- 参考: `SQLModelFieldParser`

#### _list_fields_ins

- 批量查询sqlalchemy字段列表.

### 方法:

#### get_select

- 返回SQLModel选择器.

```python
def get_select(self, request: Request) -> Select
```

#### calc_filter_clause

- 计算查询过滤条件.

```python
def calc_filter_clause(
    self,
    data: Dict[str, Any]
) -> List[BinaryExpression]
```

## SQLModelCrud

- SQLModel ORM Crud注册器

### 继承基类

- #### [BaseCrud](../BaseCrud/#basecrud)

- #### [SQLModelSelector](#sqlmodelselector)

### 字段

#### engine

- sqlalchemy 连接引擎, 必须设置.

#### readonly_fields

只读字段列表:

- 支持SQLModel模型字段, SQLModel模型, 当前模型数据库表字段名
- 支持当前模型字段,和其它模型字段.
- 默认: `[]`

### 方法:

#### get_select

- 返回SQLModel选择器.

```python
def get_select(self, request: Request) -> Select
```

#### on_create_pre

- 返回创建请求处理后的数据.

```python
async def on_create_pre(
    self,
    request: Request,
    obj: SchemaCreateT,
    **kwargs
) -> Dict[str, Any]
```

#### on_update_pre

- 返回更新请求处理后的数据.

```python
async def on_update_pre(
    self,
    request: Request,
    obj: SchemaUpdateT,
    item_id: Union[List[str], List[int]],
    **kwargs
) -> Dict[str, Any]
```

#### on_filter_pre

- 返回批量查询请求提交过滤器处理后的数据.

```python
async def on_filter_pre(
    self,
    request: Request,
    obj: SchemaFilterT,
    **kwargs
) -> Dict[str, Any]
```

