## AdminAction

- 管理动作基类

### 字段

#### admin

- 当前动作所属管理对象.

#### action

- 当前动作amis Action对象.
- 参考:  [Action 行为按钮](https://baidu.gitee.io/amis/zh-CN/components/action?page=1#弹框)

#### name

- 当前动作名称.必须存在,并且应当唯一,否则会覆盖之前的动作.

#### label

- 当前动作显示名称.

#### flags

当前动作标记.可用于决定在`ModelAdmin`中是否显示的方式.

- item: 当前动作在列表中的每一行显示.
- bulk: 当前动作在列表中的批量操作显示.
- toolbar: 当前动作在列表中的工具栏显示.
- column: 当前动作在列表中的最后一列显示.

#### getter

- 当前动作获取`Action`的方法.

### 方法

#### get_action

- 获取当前动作amis Action对象.

```python
async def get_action(self, request: Request, **kwargs) -> Action
```


## ModelAction

- 模型管理动作

### 继承基类

- #### [FormAction](../FormAdmin/#baseformadmin)


### 字段

#### schema

- 表单数据模型, 可以设置为: `None`.

### 方法


#### handle

处理模型动作数据.

- `request`: 当前请求对象.
- `item_id`: 用户选择的模型数据主键列表.
- `data`: 如果配置了动作表单数据模型`schema`,则表示表单数据对象.否则为`None`

```python
async def handle(
    self, 
    request: Request, 
    item_id: List[str], 
    data: Optional[BaseModel],
    **kwargs
) -> BaseApiOut[Any]
```

