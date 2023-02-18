## AdminGroup

- Amis页面组

### 继承基类

- #### [PageSchemaAdmin](../PageSchemaAdmin)

### 字段

#### _children

- 当前页面组子页面属性列表

### 方法

#### get_page_schema_children

返回当前页面组的子页面属性列表.

- 通过`request`参数进行权限过滤,无权限的不包括在返回结果.

- 参考: [App 多页应用#属性说明](https://baidu.gitee.io/amis/zh-CN/components/app#属性说明)

```python
async def get_page_schema_children(self, request: Request) -> List[PageSchema]
```

#### append_child

- 添加导航页面.

```python
def append_child(self, child: _PageSchemaAdminT)->None
```

#### get_page_schema_child

- 通过`unique_id`获取页面属性.

```python
def get_page_schema_child(self, unique_id: str) -> Optional[_PageSchemaAdminT]
```

#### `__iter__`

- 组内子页面迭代器.

```python
def __iter__(self) -> Iterator[_PageSchemaAdminT]:
    return self._children.__iter__()
```

 