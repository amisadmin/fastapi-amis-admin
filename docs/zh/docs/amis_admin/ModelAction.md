## BaseModelAction

- 模型管理动作基类



### 字段

#### admin

- 当前动作所属模型管理对象.

#### action

- 当前动作amis Action对象.
- 参考:  [Action 行为按钮](https://baidu.gitee.io/amis/zh-CN/components/action?page=1#弹框)



### 方法

#### register_router

- 注册动作路由.


#### fetch_item_scalars

- 获取选项数据.


```python
async def fetch_item_scalars(self, session: AsyncSession, item_id: List[str]) -> ScalarResult:
    result = await session.execute(select(self.admin.model).where(self.admin.pk.in_(item_id)))
    return result.scalars()
```



## ModelAction

- 模型管理动作

### 继承基类

- #### [BaseFormAdmin](../FormAdmin/#baseformadmin)

- #### [BaseModelAction](#basemodelaction)

  

### 字段

#### schema

- 表单数据模型, 可以设置为: `None`.



### 方法

#### get_action

- 获取当前动作amis Action对象.

```python
async def get_action(self, request: Request, **kwargs) -> Action
```


#### handle

处理模型动作数据.

- `request`: 当前请求对象.
- `item_id`: 用户选择的模型数据主键列表.
- `data`: 如果配置了动作表单数据模型`schema`,则表示表单数据对象.否则为`None`
- `session`:当前管理模型所属数据库连接异步会话.


```python
async def handle(self, request: Request, item_id: List[str], data: Optional[BaseModel],
                     session: AsyncSession, **kwargs) -> BaseApiOut[Any]
```

