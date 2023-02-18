## PageSchemaAdmin

- 导航页面管理基类

### 继承基类

- #### [BaseAdmin](../BaseAdmin)

### 字段

#### page_schema

- 当前页面菜单导航信息. 如果为None,则不会在菜单导航中显示.

### 方法

#### has_page_permission

控制用户是否拥有访问当前页面权限,默认返回:`True`

```python
async def has_page_permission(self, request: Request)->bool:
    return True
```

#### error_no_page_permission

当前页面无访问权限错误

```python
def error_no_page_permission(self, request: Request):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No page permissions')
```

#### get_page_schema

返回当前页面导航信息

```python
def get_page_schema(self) -> Optional[PageSchema]
```

## LinkAdmin

- 链接管理

### 继承基类

- #### [PageSchemaAdmin](#pageschemaadmin)

### 字段

#### link

- 跳转的链接.

## IframeAdmin

- 内嵌框架管理

### 继承基类

- #### [PageSchemaAdmin](#pageschemaadmin)

### 字段

#### src

- 内嵌框架链接.

#### iframe

- 内嵌框架Amis Iframe对象.
- 参考: [iFrame](https://baidu.gitee.io/amis/zh-CN/components/iframe)

