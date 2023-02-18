## PageSchemaAdmin

- Navigation page management base class

### Inherit from base class

- #### [BaseAdmin](../BaseAdmin)

### fields


#### page_schema

- Current page menu navigation information.If None, it will not be displayed in the menu navigation.

### method

#### has_page_permission

Controls whether the user has permission to access the current page, the default return: `True`

```python
async def has_page_permission(self, request: Request)->bool:
    return True
```

#### error_no_page_permission

The current page has no access permission error

```python
def error_no_page_permission(self, request: Request):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No page permissions')
```

#### get_page_schema

Return to the current page navigation information

```python
def get_page_schema(self) -> Optional[PageSchema]
```


## LinkAdmin

- Link management

### Inherit from base class

- #### [PageSchemaAdmin](#pageschemaadmin)

### fields

#### link

- Jump links.

## IframeAdmin

- iframe management

### Inherit from base class

- #### [PageSchemaAdmin](#pageschemaadmin)

### fields

#### src

- iframe link.

#### iframe

- Inline frame Amis Iframe object.
- 参考: [iFrame](https://baidu.gitee.io/amis/zh-CN/components/iframe)
