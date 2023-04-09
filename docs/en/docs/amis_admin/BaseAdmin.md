## BaseAdmin

- Page management base class

### fields

#### app

The application `AdminApp` object registered by the current admin object.

- Note that `app` is not the top level and may be registered by other `AdminApp` or `AdminSite`.)

#### site

The `AdminSite` site where the current management object is registered, the top-level Admin object.

#### unique_id

The unique ID of the current management object.

- Customizable settings, if not set, it will be automatically generated according to the default rules.
- Unique IDs should not change when a project is started or stopped, and should be unique per Admin class within a project.



## Admin ClassDiagram

- FastAPI-Amis-Admin core class diagram

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
    
    LinkAdmin --|> PageSchemaAdmin
    IframeAdmin --|> PageSchemaAdmin
    IframeAdmin: +Iframe iframe
    
    PageAdmin --|> PageSchemaAdmin
    PageAdmin --|> RouterAdmin
    PageAdmin: +Page page
    
    BaseActionAdmin --|> PageAdmin
    FormAdmin --|> BaseActionAdmin
    FormAdmin: +Form form
    FormAdmin: +BaseModel schema
    
    TemplateAdmin --|> PageAdmin
    TemplateAdmin: +Jinja2Templates templates
    
    %% model
    FormAction --|> AdminAction
    FormAction --|> FormAdmin
    ModelAction --|> FormAction
    AdminAction: +BaseActionAdmin admin
    AdminAction: +Action action
    
    class SQLModelSelector
    SQLModelSelector: +SQLModel model
    BaseCrud --|> RouterMixin
    SQLModelCrud ..|> BaseCrud
    SQLModelCrud --|> SQLModelSelector
    
    ModelAdmin --|> BaseActionAdmin
    ModelAdmin --|> SQLModelCrud
	
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

- fastapi-amis-admin class and amis component class diagram

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
FormAction --> Form
FormAction --> Action
ModelAdmin --> TableCRUD
ModelAdmin --> Action

```