import datetime
from typing import Any, Generator, Iterable, Type, TypeVar, Union

from pydantic import BaseModel, Json
from pydantic.fields import ModelField
from pydantic.utils import deep_update, smart_deepcopy
from typing_extensions import get_origin

from fastapi_amis_admin import amis
from fastapi_amis_admin.amis import AmisNode
from fastapi_amis_admin.amis.components import (
    Form,
    FormItem,
    InputArray,
    Remark,
    TableColumn,
    Validation,
)
from fastapi_amis_admin.amis.constants import LabelEnum
from fastapi_amis_admin.models.enums import Choices
from fastapi_amis_admin.utils.translation import i18n as _

_T = TypeVar("_T")


class AmisParser:
    """AmisParser,used to parse pydantic fields to amis form item or table column.
    AmisParser can set the default image and file upload receiver.
    """

    def __init__(
        self,
        image_receiver: amis.API = None,
        file_receiver: amis.API = None,
    ):
        """
        Args:
            image_receiver: Image upload receiver, used to upload images to a specified location and return the image address
            file_receiver: File upload receiver, used to upload files to a specified location and return the file address
        """
        self.image_receiver = image_receiver
        self.file_receiver = file_receiver

    def _wrap_form_item(self, formitem: FormItem) -> FormItem:
        """Wrap formitem, add image and file upload receiver."""
        if formitem.type == "input-image" and not getattr(formitem, "receiver", None):
            formitem.receiver = self.image_receiver
        elif formitem.type == "input-file" and not getattr(formitem, "receiver", None):
            formitem.receiver = self.file_receiver
        elif formitem.type == "input-rich-text":
            formitem.receiver = getattr(formitem, "receiver", None) or self.image_receiver
            formitem.videoReceiver = getattr(formitem, "videoReceiver", None) or self.file_receiver
        if formitem.type in {"input-image", "input-file"}:
            # Add manual input file link component.
            formitem = amis.Group(
                name=formitem.name,
                body=[
                    formitem,
                    formitem.copy(
                        exclude={"maxLength", "receiver"},
                        update={"type": "input-text"},
                    ),
                ],
            )
        return formitem

    def as_form_item(self, modelfield: ModelField, set_default: bool = False, is_filter: bool = False) -> FormItem:
        """
        Get amis form item from pydantic field.
        Args:
            modelfield: pydantic field
            set_default: Is set default value
            is_filter: Is filter form

        Returns:

        """
        formitem = self._get_form_item_from_kwargs(modelfield, is_filter=is_filter)
        formitem = self.update_common_attrs(modelfield, formitem, set_default=set_default, is_filter=is_filter)
        return self._wrap_form_item(formitem)

    def as_table_column(self, modelfield: ModelField, quick_edit: bool = False) -> TableColumn:
        column = self._get_table_column_from_kwargs(modelfield)
        column = self.update_common_attrs(modelfield, column, set_default=False, is_filter=False)
        column.sortable = True
        if column.type in ["text", None]:
            column.searchable = True
        elif column.type in ["switch", "mapping"]:
            column.sortable = False
        if quick_edit:
            column.quickEdit = self.as_form_item(modelfield, set_default=True).dict(
                exclude_none=True, by_alias=True, exclude={"name", "label"}
            )
            column.quickEdit.update({"saveImmediately": True})
            if column.quickEdit.get("type") == "switch":
                column.quickEdit.update({"mode": "inline"})
        return column

    def as_amis_form(self, model: Type[BaseModel], set_default: bool = False, is_filter: bool = False) -> Form:
        """Get amis form from pydantic model.
        Args:
            model: Pydantic model
            set_default: Is set default value
            is_filter: Is filter form
        Returns:
            amis.Form
        """
        form = amis.Form(title=getattr(model.Config, "title", None))
        form.body = [
            self.as_form_item(modelfield, set_default=set_default, is_filter=is_filter)
            for modelfield in model.__fields__.values()
        ]
        # InputSubForm
        return form

    def update_common_attrs(
        self, modelfield: ModelField, item: Union[FormItem, TableColumn], set_default: bool = False, is_filter: bool = False
    ):
        """Set common attributes for FormItem and TableColumn."""
        if not is_filter:
            if modelfield.field_info.max_length:
                item.maxLength = modelfield.field_info.max_length
            if modelfield.field_info.min_length:
                item.minLength = modelfield.field_info.min_length
            item.required = modelfield.required and not issubclass(modelfield.type_, bool)
            if set_default:
                item.value = modelfield.default
        item.name = modelfield.alias
        if item.label is None:
            item.label = _(modelfield.field_info.title or modelfield.name)  # The use of I18N
        else:
            item.label = _(modelfield.field_info.title)  # The use of I18N

        label_name = "labelRemark" if isinstance(item, FormItem) else "remark"
        if getattr(item, label_name, None) is None:
            label = (
                Remark(content=_(modelfield.field_info.description)) if modelfield.field_info.description else None
            )  # The use of I18N
            setattr(item, label_name, label)
        return item

    def _get_form_item_from_kwargs(self, modelfield: ModelField, is_filter: bool = False) -> FormItem:
        formitem = self.get_field_amis_extra(modelfield, ["amis_form_item", "amis_filter_item"][is_filter])
        # List type parse to InputArray
        if issubclass(modelfield.type_, (list, set)) or (
            modelfield.outer_type_ and get_origin(modelfield.outer_type_) in {list, set}
        ):
            if not isinstance(formitem, FormItem):
                formitem = InputArray(**formitem)
            # Parse the internal type of the list.
            kwargs = self.get_field_amis_form_item_type(type_=modelfield.type_, is_filter=is_filter)
            update = formitem.items.amis_dict() if formitem.items else {}
            if update:
                kwargs = deep_update(kwargs, update)
            formitem.items = FormItem(**kwargs)
        if isinstance(formitem, FormItem):
            return formitem
        # other type parse to FormItem
        kwargs = self.get_field_amis_form_item_type(
            type_=modelfield.type_,
            is_filter=is_filter,
            required=modelfield.required,
        )
        return FormItem(**kwargs).update_from_dict(formitem)

    def _get_table_column_from_kwargs(self, modelfield: ModelField) -> TableColumn:
        table_column = self.get_field_amis_extra(modelfield, "amis_table_column")
        if isinstance(table_column, TableColumn):
            return table_column
        kwargs = self.get_field_amis_table_column_type(modelfield.type_)
        return TableColumn(**kwargs).update_from_dict(table_column)

    def get_field_amis_table_column_type(self, type_: Type) -> dict:
        """Get amis table column type from pydantic model field type."""
        kwargs = {}
        if type_ in [str, Any]:
            pass
        elif issubclass(type_, bool):
            kwargs["type"] = "switch"
            kwargs["filterable"] = {
                "options": [
                    {"label": _("YES"), "value": True},
                    {"label": _("NO"), "value": False},
                ]
            }
        elif issubclass(type_, datetime.datetime):
            kwargs["type"] = "datetime"
        elif issubclass(type_, datetime.date):
            kwargs["type"] = "date"
        elif issubclass(type_, datetime.time):
            kwargs["type"] = "time"
        elif issubclass(type_, Choices):
            kwargs["type"] = "mapping"
            kwargs["filterable"] = {"options": [{"label": v, "value": k} for k, v in type_.choices]}
            kwargs["map"] = {
                k: f"<span class='label label-{l.value}'>{v}</span>"
                for (k, v), l in zip(type_.choices, cyclic_generator(LabelEnum))
            }
        elif issubclass(type_, (dict, Json)):
            kwargs["type"] = "json"
        elif issubclass(type_, (list, set)):
            kwargs["type"] = "each"
            kwargs["items"] = {"type": "tpl", "tpl": "<span class='label label-info m-l-sm'><%= this.item %></span>"}
        return kwargs

    def get_field_amis_form_item_type(self, type_: Any, is_filter: bool, required: bool = False) -> dict:
        """Get amis form item type from pydantic model field type."""
        kwargs = {}
        if type_ in [str, Any]:
            kwargs["type"] = "input-text"
        elif issubclass(type_, Choices):
            kwargs.update(
                {
                    "type": "select",
                    "options": [{"label": l, "value": v} for v, l in type_.choices],
                    "extractValue": True,
                    "joinValues": False,
                }
            )
            if not required:
                kwargs["clearable"] = True
        elif issubclass(type_, bool):
            kwargs["type"] = "switch"
        elif is_filter:
            if issubclass(type_, datetime.datetime):
                kwargs["type"] = "input-datetime-range"
                kwargs["format"] = "YYYY-MM-DD HH:mm:ss"
                # 给筛选的 DateTimeRange 添加 today 标签
                kwargs["ranges"] = "today,yesterday,7daysago,prevweek,thismonth,prevmonth,prevquarter"
            elif issubclass(type_, datetime.date):
                kwargs["type"] = "input-date-range"
                kwargs["format"] = "YYYY-MM-DD"
            elif issubclass(type_, datetime.time):
                kwargs["type"] = "input-time-range"
                kwargs["format"] = "HH:mm:ss"
            else:
                kwargs["type"] = "input-text"
        elif issubclass(type_, int):
            kwargs["type"] = "input-number"
            kwargs["precision"] = 0
            kwargs["validations"] = Validation(isInt=True)
        elif issubclass(type_, float):
            kwargs["type"] = "input-number"
            kwargs["validations"] = Validation(isFloat=True)
        elif issubclass(type_, datetime.datetime):
            kwargs["type"] = "input-datetime"
            kwargs["format"] = "YYYY-MM-DD HH:mm:ss"
        elif issubclass(type_, datetime.date):
            kwargs["type"] = "input-date"
            kwargs["format"] = "YYYY-MM-DD"
        elif issubclass(type_, datetime.time):
            kwargs["type"] = "input-time"
            kwargs["format"] = "HH:mm:ss"
        elif issubclass(type_, (dict, Json)):
            kwargs["type"] = "json-editor"
        elif issubclass(type_, BaseModel):
            # pydantic model parse to InputSubForm
            kwargs["type"] = "input-sub-form"
            kwargs["labelField"] = get_model_label_field_name(type_)
            kwargs["btnLabel"] = getattr(type_.Config, "title", None)
            kwargs["form"] = self.as_amis_form(type_, is_filter=is_filter)
        else:
            kwargs["type"] = "input-text"
        return kwargs

    def get_field_amis_extra(
        self,
        modelfield: ModelField,
        name: str,
    ) -> Union[FormItem, TableColumn, dict]:
        """Get amis extra from pydantic model field.
        You can pass amis configuration through the extra parameter of the pydantic model field.
        """
        extra = modelfield.field_info.extra.get(name, {})
        if not extra:
            return {}
        extra = smart_deepcopy(extra)
        if isinstance(extra, (AmisNode, dict)):
            pass
        elif isinstance(extra, str):
            extra = dict(type=extra)
        else:
            extra = {}
        return extra


def cyclic_generator(iterable: Iterable[_T]) -> Generator[_T, None, None]:
    while True:
        yield from iterable


def get_model_label_field_name(model: Type[BaseModel]) -> str:
    """Get model label field name. The label field is used to display the model name in the form."""
    label_field_name = getattr(model.Config, "label_field_name", None)
    if label_field_name:
        return label_field_name
    for filed in model.__fields__.values():
        if filed.alias in ["name", "title", "label"]:
            return filed.alias
    return "id"
