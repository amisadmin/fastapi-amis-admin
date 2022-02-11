## BaseModelAdmin

- 模型管理基类

### 继承基类

- #### [SQLModelCrud](../../crud/SQLModelCrud)



### 字段

#### list_display

批量查询需要显示的字段列表.
- 支持SQLModel模型字段, SQLModel模型, 当前模型数据库表字段名
- 支持当前模型字段,和其它模型字段. 
- 支持amis类型:  TableColumn

- 默认: `self.schema_list.__fields__.values()`

#### list_filter

- 批量查询过滤表单的字段列表
- 默认: `self.schema_filter.__fields__.values()`

#### list_per_page

- 批量查询每页的数据量,默认为: 15

#### search_fields

- 表格中支持文本模糊搜索的字段列表,默认为:[]

#### bulk_edit_fields

- 表格中支持批量编辑的字段列表,默认为:[]

#### link_model_fields

- 批量查询需要链接的多对多关联的字段列表,默认为: []. 即: 默认不识别关联列表字段.

#### link_model_forms

- 批量查询需要链接的多对多关联的字段表单列表,默认根据`self.link_model_fields`生成.



### 方法


#### get_list_display

- 返回表格列表显示的字段列表.

```python
async def get_list_display(self, 
                     request: Request) -> List[Union[SQLModelListField, TableCRUD.Column]]
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
async def get_list_column(self, request: Request, 
                    modelfield: ModelField) -> TableColumn
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
- 参考: [CRUD 增删改查](https://baidu.gitee.io/amis/zh-CN/components/crud) , [Table 表格](https://baidu.gitee.io/amis/zh-CN/components/table)

```python
async def get_list_table(self, request: Request) -> TableCRUD
```

---

#### get_form_item

- 返回页面表单字段的`amis` `FormItem`对象.
- 参考: [FormItem 普通表单项 (gitee.io)](https://baidu.gitee.io/amis/zh-CN/components/form/formitem)

```python
async def get_form_item(self, request: Request, 
                  modelfield: ModelField, 
                  action: CrudEnum) -> Union[FormItem, SchemaNode]
```


#### get_form_item_on_foreign_key

- 返回页面表单`foreign_key`字段的`amis` `FormItem`对象.

```python
async def get_form_item_on_foreign_key(self, 
                                 modelfield: ModelField) -> Union[Service, SchemaNode]
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

#### get_delete_action

- 返回删除模型数据执行动作`amis Action`对象.
- 参考: [Action 行为按钮](https://baidu.gitee.io/amis/zh-CN/components/action?page=1#弹框)

```python
async def get_delete_action(self, request: Request, bulk: bool = False) -> Optional[Action]
```

#### get_actions_on_header_toolbar

- 返回列表表格顶部工具条执行动作列表.

```python
async def get_actions_on_header_toolbar(self, request: Request) -> List[Action]
```

#### get_actions_on_item

- 返回列表表格数据单项操作执行动作列表.

```python
async def get_actions_on_item(self, request: Request) -> List[Action]
```

#### get_actions_on_bulk

- 返回列表表格数据批量操作执行动作列表.

```python
async def get_actions_on_bulk(self, request: Request) -> List[Action]
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

