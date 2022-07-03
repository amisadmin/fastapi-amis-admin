## BaseAdmin

- 页面管理基类

### 字段

#### app

当前管理对象注册的应用`AdminApp`对象.

- 注意`app`并非最顶级,还可能被其他`AdminApp`或`AdminSite`注册.)

#### site

当前管理对象注册的站点`AdminSite`站点,最顶级Admin对象.

#### unique_id

当前管理对象的唯一性标识ID.

- 可自定义设置,如未设置则根据默认规则自动生成.
- 唯一性标识ID不应当随着项目的启动或停止产生变化, 并且在项目中每个Admin类标识应当唯一.



## Admin ClassDiagram

- FastAPI-Amis-Admin 核心类图

``` mermaid
classDiagram
	%% admin
    class RouterMixin
    RouterMixin: +APIRouter router
    RouterAdmin --|> RouterMixin
    class BaseAdmin
    BaseAdmin: +AdminAPP app
    RouterAdmin --|> BaseAdmin
    PageSchemaAdmin --|> BaseAdmin
    PageSchemaAdmin: +PageSchema page_schema
    PageSchemaAdmin: +PageSchema group_schema
    
    LinkAdmin --|> PageSchemaAdmin
    IframeAdmin --|> PageSchemaAdmin
    IframeAdmin: +Iframe iframe
    
    PageAdmin --|> PageSchemaAdmin
    PageAdmin --|> RouterAdmin
    PageAdmin: +Page page
    
    BaseFormAdmin --|> PageAdmin
    BaseFormAdmin: +Form form
    BaseFormAdmin: +BaseModel schema
    
    FormAdmin --|> BaseFormAdmin
    
    TemplateAdmin --|> PageAdmin
    TemplateAdmin: +Jinja2Templates templates
    
    %% model
    ModelFormAdmin --|> FormAdmin
    ModelFormAdmin --|> SQLModelSelector
    ModelAction --|> BaseFormAdmin
    ModelAction --|> BaseModelAction
    ModelAction: +ModelAdmin admin
    ModelAction: +Action action
    
    class SQLModelSelector
    SQLModelSelector: +SQLModel model
    BaseCrud --|> RouterMixin
    SQLModelCrud ..|> BaseCrud
    SQLModelCrud --|> SQLModelSelector
    
    BaseModelAdmin --|> SQLModelCrud
    ModelAdmin --|> BaseModelAdmin
	ModelAdmin --|> PageAdmin
	
	%% group,app,site
	AdminGroup --|> PageSchemaAdmin
	
    AdminAPP --|> AdminGroup
    AdminAPP --|> PageAdmin
    AdminAPP: +AsyncDatabase db
    AdminAPP: +AdminSite site
    
    AdminSite --|> AdminAPP
    AdminSite: +FastAPI fastapi
    AdminSite: +Settings settings
    
```

## Admin & Amis

- fastapi-amis-admin类与amis组件类关系图

```mermaid
classDiagram
AdminSite --> App
App --|> AmisNode
App *-- PageSchema
PageSchema --|> AmisNode
PageSchema *-- PageSchema

AdminApp --> App
AdminApp --> Tabs
Tabs *-- TabsItem
TabsItem --|> AmisNode

Page --|> AmisNode
PageAdmin --> Page

Form --|> AmisNode
FormItem --|> AmisNode
Form *-- FormItem
FormAdmin --> Form

Table --|> AmisNode
CRUD --|> AmisNode
TableCRUD --|> Table
TableCRUD --|> CRUD
Table *-- TableColumn
TableColumn --|> AmisNode
Action --|> AmisNode
ModelAction --> Form
ModelAction --> Action
ModelAdmin --> TableCRUD
ModelAdmin --> Action

```
