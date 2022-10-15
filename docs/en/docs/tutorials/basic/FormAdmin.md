# Form Management

`FormAdmin` implements to display a menu in the menu list. Clicking on the menu will display an `amis` form page.

## Example

```python
from fastapi_amis_admin.admin import admin
from fastapi_amis_admin.crud import BaseApiOut
from fastapi_amis_admin.models.fields import Field
from pydantic import BaseModel
from starlette.requests import Request


@site.register_admin
class UserLoginFormAdmin(admin.FormAdmin):
    page_schema = 'UserLoginForm'
    # Configure form information, can be omitted
    form = Form(title='This is a test login form', submitText='Login')

    # Create a form data model
    class schema(BaseModel):
        username: str = Field(... , title='username', min_length=3, max_length=30)
        password: str = Field(... , title='password')

    # Handle form submission data
    async def handle(self, request: Request, data: BaseModel, **kwargs) -> BaseApiOut[Any]:
        if data.username == 'amisadmin' and data.password == 'amisadmin':
            return BaseApiOut(msg='Login successful!' , data={'token': 'xxxxxxx'})
        return BaseApiOut(status=-1, msg='Username or password error!')
```

What is shown here is just a simple and basic function.

## Form object

The class field `form` can be used to configure basic information about the form, such as: title, form style, submit button, submit API, message prompt, etc. Please refer to: [Form form](https://baidu.gitee.io/amis/zh-CN/components/form/index)

## Form Data Model

The class field `schema` defines the form data model, which is inherited from `pydantic BaseModel`, and supports various types of fields, which are automatically parsed into corresponding components on the front-end by `amis`. The functions that can be accomplished through `schema` are:

- Define basic field properties. For example: name, label, data type, basic restrictions
- Custom field handling or validators. Reference: [Validators - pydantic](https://pydantic-docs.helpmanual.io/usage/validators/)

- Customize the `amis` component. You can customize the `amis` component with `amis_form_item`.

## Handle functions

The class method `handle` receives the form data submitted by the user, where you can perform all kinds of complex logical processing of the form data.

## More Uses

In fact `FormAdmin` has more complex uses than can be explained in detail here, please refer to the following documents.

### Related documentation

- [FormAdmin](/amis_admin/FormAdmin/)
