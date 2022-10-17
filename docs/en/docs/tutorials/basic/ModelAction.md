# Model Actions

A model management action is an action that is performed on one or more model data. For example, the most basic actions are add/read/update/delete; but often you may need to add some special commands. For example: change data state, perform certain tasks. In this case you can add custom model management actions. `fastapi_amis_admin`
There are many types of model actions, here is a brief demonstration of a few of them that may be commonly used.

## Custom toolbar actions

### Example-1

```python
@site.register_admin
class ArticleAdmin(admin.ModelAdmin):
    group_schema = 'Articles'
    page_schema = PageSchema(label='Article Admin', icon='fa fa-file')
    model = Article

    # Add custom toolbar actions
    async def get_actions_on_header_toolbar(self, request: Request) -> List[Action]:
        actions = await super().get_actions_on_header_toolbar(request)

        actions.append(ActionType.Ajax(label='toolbar ajax action', 
                                       api='https://3xsw4ap8wah59.cfc-execute.bj.baidubce.com/api/amis-mock/mock2/form/saveForm'))

        actions.append(ActionType.Link(label='Toolbar link action', 
                                       link='https://github.com/amisadmin/fastapi_amis_admin'))

        return actions
```

In this example, two simple model actions are added to the model list form toolbar by overriding the `get_actions_on_header_toolbar` method:

1. `ActionType.Ajax` action will send an ajax request to the specified api. 2.
2. `ActionType.Link` action will jump to the specified link when clicked.

!!! note annotate "About `ActionType`"

    ActionType is actually a python model mapping of the [amis Action behavior button](https://baidu.gitee.io/amis/zh-CN/components/action?page=1) component, which supports many common behavior types. For example: ajax request/download request/jump link/send email/bounce window/drawer/copy text etc.
    
    fastapi_amis_admin is flexible because it is based on amis component-based development, you can freely replace or add built-in amis components in many places. Before that, I hope you can read the [amis documentation](https://baidu.gitee.io/amis/zh-CN/components/page) to have some understanding of the core components of amis.

## Customizing individual actions

### Example-2

```python
## Create a normal ajax action
class TestAction(admin.ModelAction):
    ## Configure action basic information
    action = ActionType.Dialog(label='Custom General Handling Action', dialog=Dialog())
    
	# Action handling
    async def handle(self, request: Request, item_id: List[str], data: Optional[BaseModel], **kwargs):
        # Get a list of data selected by the user from the database
        items = await self.fetch_item_scalars(item_id)
        # Perform action processing
        ...
        # Return the result of the action processing
        return BaseApiOut(data=dict(item_id=item_id, data=data, items=list(items))))

@site.register_admin
class ArticleAdmin(admin.ModelAdmin):
    group_schema = 'Articles'
    page_schema = PageSchema(label='article_admin', icon='fa fa-file')
    model = Article

    # Add a custom single action
    async def get_actions_on_item(self, request: Request) -> List[Action]:
        actions = await super().get_actions_on_item(request)
        action = await self.test_action.get_action(request)
        actions.append(action)
        return actions
    
    # Register a custom route
    def register_router(self):
        super().register_router()
        # Register action routes
        self.test_action = TestAction(self).register_router()
```

The work done in Example-2:

- Defines a very basic model action class `TestAction`, whose core is the `handle` method. Please refer to: [ModelAction](/amis_admin/ModelAction/#baseformadmin)

- By overriding the `register_router` method, the `TestAction` class is instantiated and the route is registered and bound to the current ModelAction class property field.

- Override the `get_actions_on_item` method to add the model actions corresponding to the `TestAction` instance to the list of single action actions.

## Customizing Bulk Actions

### Example-3

```python
from fastapi_amis_admin import admin

## Create form ajax action
class TestFormAction(admin.ModelAction):
    # Configure action basic information
    Dialog(label='Custom Form Action', dialog=Dialog())

    # Create action form data model
    class schema(BaseModel):
        username: str = Field(... , title='username')
        password: str = Field(... , title='password', amis_form_item='input-password')
        is_active: bool = Field(True, title='Active or not')
            
	# Action handling
    async def handle(self, request: Request, item_id: List[str], data: schema, **kwargs):
        # Get a list of data selected by the user from the database
        items = await self.fetch_item_scalars(item_id)
        # Perform action processing
        ...
        # Return the result of the action processing
        return BaseApiOut(data=dict(item_id=item_id, data=data, items=list(items))))
    
@site.register_admin
class ArticleAdmin(admin.ModelAdmin):
    group_schema = 'Articles'
    page_schema = PageSchema(label='article_admin', icon='fa fa-file')
    model = Article

    # Add custom bulk actions
    async def get_actions_on_bulk(self, request: Request) -> List[Action]:
        actions = await super().get_actions_on_bulk(request)
        action = await self.test_form_action.get_action(request)
        action.label = 'Custom Bulk Action'
        actions.append(action.copy())
        return actions
    
    # Register a custom route
    def register_router(self):
        super().register_router()
        # Register action routes
        self.test_form_action = TestFormAction(self).register_router()
```

Example-3 is very similar to Example-2, but it allows the user to add a custom form, which is very useful in many cases.

The definition and use of `schema` is very similar to `FormAdmin`.

## For more usage

Please refer to the [demo program](https://github.com/amisadmin/fastapi_amis_admin_demo), or read the following related documentation, which should help you.

- [ModelAdmin](/amis_admin/ModelAdmin/)

- [ModelAction](/amis_admin/ModelAction/#baseformadmin)

- [Action behavior button](https://baidu.gitee.io/amis/zh-CN/components/action?page=1)

