# 模型动作

模型管理动作指的是针对某一项或多项模型数据所进行的操作.例如:最基本的操作有增加/读取/更新/删除;
但是很多时候你可能需要添加某些特殊的操作命令.例如:改变数据状态,
执行某些任务.这时候你可以添加自定义模型管理动作.`fastapi_amis_admin`
拥有多种类型模型动作,下面简单演示几种可能常用的动作方式.

## 自定义工具条动作

### 示例-1

```python
@site.register_admin
class ArticleAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label='文章管理', icon='fa fa-file')
    model = Article

    # 添加自定义工具条动作
    admin_action_maker = [
        lambda admin: AdminAction(
            admin=admin,
            name='test_ajax_action',
            action=ActionType.Ajax(
                label='工具条ajax动作',
                api='https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/mock2/form/saveForm'
            ),
            flags=['toolbar']
        ),
        lambda admin: AdminAction(
            admin=admin,
            name='test_link_action',
            action=ActionType.Link(
                label='工具条link动作',
                link='https://github.com/amisadmin/fastapi_amis_admin'
            ),
            flags=['toolbar']
        )
    ]

```

在本示例中,通过`admin_action_maker`字段,在模型列表表格工具条添加了两个简单的模型动作:

1. `ActionType.Ajax`动作将发送一个ajax请求,到指定的api.
2. `ActionType.Link`动作点击后将跳转到指定的链接.

!!! note annotate "关于`ActionType`"

    ActionType事实上是[amis Action 行为按钮](https://baidu.gitee.io/amis/zh-CN/components/action?page=1)组件的一个python模型映射,它支持多种常见的行为类型.例如:ajax请求/下载请求/跳转链接/发送邮件/弹窗/抽屉/复制文本等等.
    
    fastapi_amis_admin的灵活性强体现之一,是因为它是基于amis的组件式开发,你可以在很多地方自由的替换或添加内置的amis组件.在此之前希望你能阅读[amis文档](https://baidu.gitee.io/amis/zh-CN/components/page),对amis核心组件有一定的了解.

## 自定义单项操作动作

### 示例-2

```python
# 创建普通ajax动作
class TestAction(admin.ModelAction):
    # 配置动作基本信息
    action = ActionType.Dialog(label='自定义普通处理动作', dialog=Dialog())

    # 动作处理
    async def handle(self, request: Request, item_id: List[str], data: Optional[BaseModel], **kwargs):
        # 从数据库获取用户选择的数据列表
        items = await self.fetch_item_scalars(item_id)
        # 执行动作处理
        ...
        # 返回动作处理结果
        return BaseApiOut(data=dict(item_id=item_id, data=data, items=list(items)))


@site.register_admin
class ArticleAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label='文章管理', icon='fa fa-file')
    model = Article
    # 添加自定义单项和批量操作动作
    admin_action_maker = [
        lambda admin: TestAction(admin, name='test_action',flags=['item','bulk'])
    ]
```

示例-2中所完成的工作:

- 定义了一个最基础的模型动作类`TestAction`,它的核心是`handle`
  方法.具体请参考: [ModelAction](/amis_admin/ModelAction/#baseformadmin)

- 通过`admin_action_maker`字段,实例化`TestAction`类,绑定到当前模型管理类的单项和批量操作动作.


## 自定义批量操作动作

### 示例-3

```python
from fastapi_amis_admin import admin


# 创建表单ajax动作
class TestFormAction(admin.ModelAction):
    # 配置动作基本信息
    action = ActionType.Dialog(label='自定义表单动作', dialog=Dialog())

    # 创建动作表单数据模型
    class schema(BaseModel):
        username: str = Field(..., title='用户名')
        password: str = Field(..., title='密码', amis_form_item='input-password')
        is_active: bool = Field(True, title='是否激活')

    # 动作处理

    async def handle(self, request: Request, item_id: List[str], data: schema, **kwargs):
        # 从数据库获取用户选择的数据列表
        items = await self.fetch_item_scalars(item_id)
        # 执行动作处理
        ...
        # 返回动作处理结果
        return BaseApiOut(data=dict(item_id=item_id, data=data, items=list(items)))


@site.register_admin
class ArticleAdmin(admin.ModelAdmin):
    page_schema = PageSchema(label='文章管理', icon='fa fa-file')
    model = Article

    # 添加自定义单项和批量操作动作
    admin_action_maker = [
        lambda admin: TestAction(admin, name='test_action',flags=['item','bulk'])
    ]

```

示例-3与示例-2非常相似, 但是它允许用户添加一个自定义表单,这个在很多情况下,非常有用.

`schema`的定义与使用与`FormAdmin`非常相似.

## 更多用法

请参考[demo程序](https://github.com/amisadmin/fastapi_amis_admin_demo),或阅读以下相关文档,应该会对你有所帮助.

- [ModelAdmin](/amis_admin/ModelAdmin/)

- [ModelAction](/amis_admin/ModelAction/#baseformadmin)

- [Action 行为按钮](https://baidu.gitee.io/amis/zh-CN/components/action?page=1)

