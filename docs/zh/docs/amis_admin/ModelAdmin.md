## BaseModelAdmin

- 模型管理基类

### 继承基类

- #### [SQLModelCrud](../../crud/SQLModelCrud)

### 字段

#### list_display

批量查询需要显示的字段列表.

- 支持SQLModel模型字段, 当前模型数据库表字段名
- 支持当前模型字段,和其它模型字段.
- 支持amis类型:  TableColumn
- 支持sqlalchemy Label类型: 可通过`LabelField`方法构造.
    - 例如: `User.name.label('nickname')`, `LabelField(User.name.label('nickname'),Field(None,title='用户昵称'))`
- 默认: `self.schema_list.__fields__.values()`

#### list_filter

- 批量查询过滤表单的字段列表
- 支持amis类型:  FormItem
- 支持sqlalchemy Label类型: 可通过`LabelField`方法构造.
- 默认: `self.schema_filter.__fields__.values()`

#### list_per_page

- 批量查询每页的数据量,默认为: 15

#### search_fields

- 表格中支持文本模糊搜索的字段列表,默认为:[]

#### update_fields

- 表格中支持编辑的字段列表,默认为:[]

#### bulk_update_fields

- 表格中支持批量编辑的字段列表,默认为:[]

#### link_model_fields

- 批量查询需要链接的多对多关联的字段列表,默认为: []. 即: 默认不识别关联列表字段.

#### link_model_forms

- 批量查询需要链接的多对多关联的字段表单列表,默认根据`self.link_model_fields`生成.

#### enable_bulk_create

- 是否启用批量创建,默认为: False

#### registered_admin_actions

- 注册的管理动作列表,默认为: []

### 方法

#### get_list_display

- 返回表格列表显示的字段列表.

```python
async def get_list_display(
    self,
    request: Request
) -> List[Union[SQLModelListField, TableCRUD.Column]]
```

#### get_list_filter

- 返回表格列表查询过滤的字段列表.

```python
async def get_list_filter(self, request: Request) -> List[Union[SQLModelListField, FormItem]]
```

#### get_list_column

返回表格列字段的`amis` `TableColumn`对象.

- 参考: [Table 表格](https://baidu.gitee.io/amis/zh-CN/components/table#列配置属性表)

```python
async def get_list_column(
    self, request: Request,
    modelfield: ModelField
) -> TableColumn
```

#### get_list_columns

返回表格列字段的`amis` `TableColumn`对象列表.

```python
async def get_list_columns(self, request: Request) -> List[TableCRUD.Column]
```

#### get_list_filter_api

- 返回列表筛选过滤器表单的AmisAPI对象.

```python
async def get_list_filter_api(self, request: Request) -> AmisAPI
```

#### get_list_table

- 返回页面的`amis` `TableCRUD`对象.
- 参考: [CRUD 增删改查](https://baidu.gitee.io/amis/zh-CN/components/crud)
  , [Table 表格](https://baidu.gitee.io/amis/zh-CN/components/table)

```python
async def get_list_table(self, request: Request) -> TableCRUD
```

---

#### get_form_item

- 返回页面表单字段的`amis` `FormItem`对象.
- 参考: [FormItem 普通表单项 (gitee.io)](https://baidu.gitee.io/amis/zh-CN/components/form/formitem)

```python
async def get_form_item(
    self, request: Request,
    modelfield: ModelField,
    action: CrudEnum
) -> Union[FormItem, SchemaNode]
```

#### get_form_item_on_foreign_key

- 返回页面表单`foreign_key`字段的`amis` `FormItem`对象.

```python
async def get_form_item_on_foreign_key(
    self,
    modelfield: ModelField
) -> Union[Service, SchemaNode]
```

#### get_link_model_forms

- 返回多对多关联的字段表单列表.

```python
def get_link_model_forms(self) -> List[LinkModelForm]
```

#### get_list_filter_form

- 返回列表筛选过滤器表单.

```python
async def get_list_filter_form(self, request: Request) -> Form
```

#### get_create_form

- 返回新增模型数据表单.

```python
async def get_create_form(self, request: Request, bulk: bool = False) -> Form
```

#### get_update_form

- 返回更新模型数据表单.

```python
async def get_update_form(self, request: Request, bulk: bool = False) -> Form
```

---

#### get_create_action

- 返回新增模型数据执行动作`amis Action`对象.
- 参考: [Action 行为按钮](https://baidu.gitee.io/amis/zh-CN/components/action?page=1#弹框)

```python
async def get_create_action(self, request: Request, bulk: bool = False) -> Optional[Action]
```

#### get_update_action

- 返回更新模型数据执行动作`amis Action`对象.
- 参考: [Action 行为按钮](https://baidu.gitee.io/amis/zh-CN/components/action?page=1#弹框)

```python
async def get_update_action(self, request: Request, bulk: bool = False) -> Optional[Action]
```

#### get_actions

返回列表表格指定标识的动作列表.当前支持的标识有:

- item: 当前动作在列表中的每一行显示.
- bulk: 当前动作在列表中的批量操作显示.
- toolbar: 当前动作在列表中的工具栏显示.
- column: 当前动作在列表中的最后一列显示.


```python
async def get_actions(self, request: Request, flag:str) -> List[Action]
```

#### get_action

返回列表表格指定名称的Amis动作对象.name为`get_actions`返回的动作名称,具有唯一性.


```python
async def get_action(self, request: Request, name: str) -> Action
```

## ModelAdmin

- 模型管理

### 继承基类

- #### [PageAdmin](../PageAdmin)

- #### [BaseModelAdmin](#BaseModelAdmin)

### 字段

#### bind_model

是否将模型管理页面绑定到模型, 默认: `True`

- 如果设置成`True` ,则可以通过`AdminSite.get_model_admin`获取.

- 在存在外键关联的模型中, 默认的`FormItem`(TablePicker),将使用绑定模型相对应的第一个管理页面.

#### admin_action_maker

- 模型管理页面动作生成器.生成器函数签名为`Callable[["ModelAdmin"], "AdminAction"]`.
  

## ModelAdmin数据控制核心字段/方法关系图

- A: 总是影响最终值.

- O?: 数值?表示优先顺序.

    - 优先采用数值最低的构造方案作为最终值.
    - 自身被重载覆盖将直接采用为最终值.

```mermaid
graph LR

	subgraph Read
		model--O1-->schema_read-->route_read:Response(ReadApiResponse)
		subgraph Selector
            model.->fields
            pk_name--A-->fields
            exclude--A-->fields
    	end
	end
	
	subgraph Create
        schema_create-->get_create_form-->create_form(AmisCreateForm)
        create_fields--O1-->schema_create-->route_create-->create_api_body(CreateApiRequest)
    end
    
	subgraph Update
		schema_update-->get_update_form-->update_form(AmisUpdateForm)
		update_fields--O1-->schema_update-->route_update-->update_api_body(UpdateApiRequest)
		readonly_fields--A-->schema_update
	end
	
	subgraph List
		fields-->_select_entities-->get_select
        fields-->schema_list-->list_api_response(ListApiResponse)
		list_display-->get_list_display-->get_list_columns-->list_columns(AmisListColumns)
		subgraph route_list
            get_select
            calc_filter_clause
            schema_list
            schema_filter
		end
        list_display--A-->fields--O2-->list_filter-->_filter_entities-->calc_filter_clause
        list_display--O1-->list_filter-->schema_filter-->route_list_body(ListApiRequest)
        subgraph Filter
        	search_fields--A-->list_filter-->get_list_filter-->get_list_filter_form-->list_filter_form(AmisListFilterForm)
        end
	end
	
```
