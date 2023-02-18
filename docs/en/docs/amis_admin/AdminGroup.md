## AdminGroup

- Amis page group

### Inherited base class

- #### [PageSchemaAdmin](. /PageSchemaAdmin)



### Fields

#### _children

- List of child page properties for the current page group



### Methods

#### get_page_schema_children

Returns a list of child page attributes for the current page group.

- Permissions are filtered by the `request` parameter, and those without permissions are not included in the returned results.

- Reference: [App multi-page application#property description](https://baidu.gitee.io/amis/zh-CN/components/app#属性说明)

```python
async def get_page_schema_children(self, request: Request) -> List[PageSchema]
```


#### append_child

- Add a navigation page.

```python
def append_child(self, child: _PageSchemaAdminT)->None
```

#### get_page_schema_child

- Get page attributes by `unique_id`.

``` python
def get_page_schema_child(self, unique_id: str) -> Optional[_PageSchemaAdminT]
```

#### `__iter__`

- Iterator for child pages within a group.

``` python
def __iter__(self) -> Iterator[_PageSchemaAdminT]:
    return self._children.__iter__()
```