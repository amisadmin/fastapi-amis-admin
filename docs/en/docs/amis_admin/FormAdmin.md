## BaseFormAdmin

- Form management base class

### Inherit from base class

- #### [PageAdmin](../PageAdmin)

### fields

#### schema

- Form data model, must be set.

#### schema_init_out

- Form initialization returns data model

#### schema_submit_out

- Form submit returns data model

#### form

- The current form amis Form object.
- Reference: [Form Form](https://baidu.gitee.io/amis/zh-CN/components/form/index)

#### form_path

- Form submission and initialization data interface api routing path.

#### form_init

- Whether to enable form data initialization. Default: `None`, not enabled.

#### route_init

- Initialize form routing

#### route_submit

- submit form routing

### method

#### get_form

- Get the current page Form object.

```python
async def get_form(self, request: Request) -> Form
```

#### get_form_item

- Returns the `amis` `FormItem` object for the current page's form fields.
- Reference: [FormItem common form item](https://baidu.gitee.io/amis/zh-CN/components/form/formitem)

```python
async def get_form_item(self, request: Request, 
                  modelfield: ModelField) -> Union[FormItem, SchemaNode]
```

# FormAdmin

- Form management

### Inherit from base class

- ### [BaseFormAdmin](#baseformadmin)

### method

#### handle

Handle page form submission data.

- `request`: The current request object.
- `data`: The form data model `schema` instance object submitted by the user.

```python
async def handle(self, request: Request, data: BaseModel, **kwargs) -> BaseApiOut[Any]
```

#### get_init_data

Get page form initialization data.

```python
async def get_init_data(self, request: Request, **kwargs) -> BaseApiOut[Any]
```
