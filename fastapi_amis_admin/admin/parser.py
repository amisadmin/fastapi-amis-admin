import datetime
from typing import Any, Iterable

from pydantic import Json
from pydantic.fields import ModelField
from pydantic.utils import smart_deepcopy

from fastapi_amis_admin import amis
from fastapi_amis_admin.amis.components import (
    FormItem,
    InputNumber,
    Remark,
    TableColumn,
    Validation,
)
from fastapi_amis_admin.amis.constants import LabelEnum
from fastapi_amis_admin.models.enums import Choices
from fastapi_amis_admin.utils.translation import i18n as _


class ModelFieldParser:
    """AmisParser,used to parse pydantic fields to amis form item or table column."""

    def __init__(self, modelfield: ModelField):
        self.modelfield = modelfield  # read only

    @property
    def label(self):
        return self.modelfield.field_info.title or self.modelfield.name

    @property
    def remark(self):
        return Remark(content=self.modelfield.field_info.description) if self.modelfield.field_info.description else None

    def as_form_item(self, set_default: bool = False, is_filter: bool = False) -> FormItem:
        formitem = self._parse_form_item_from_kwargs(is_filter)
        if not is_filter:
            if self.modelfield.field_info.max_length:
                formitem.maxLength = self.modelfield.field_info.max_length
            if self.modelfield.field_info.min_length:
                formitem.minLength = self.modelfield.field_info.min_length
            formitem.required = self.modelfield.required and not issubclass(self.modelfield.type_, bool)
            if set_default:
                formitem.value = self.modelfield.default
        formitem.name = self.modelfield.alias
        formitem.label = formitem.label or self.label
        formitem.labelRemark = formitem.labelRemark or self.remark
        return formitem

    def as_table_column(self, quick_edit: bool = False) -> TableColumn:
        column = self._parse_table_column_from_kwargs()
        column.name = self.modelfield.alias
        column.label = column.label or self.label
        column.remark = column.remark or self.remark
        column.sortable = True
        if column.type in ["text", None]:
            column.searchable = True
        elif column.type in ["switch", "mapping"]:
            column.sortable = False
        return column

    def _parse_form_item_from_kwargs(self, is_filter: bool = False) -> FormItem:
        kwargs = {}
        formitem = self.modelfield.field_info.extra.get(["amis_form_item", "amis_filter_item"][is_filter])
        if formitem is not None:
            formitem = smart_deepcopy(formitem)
            if isinstance(formitem, FormItem):
                pass
            elif isinstance(formitem, dict):
                kwargs = formitem
                formitem = FormItem(**kwargs) if kwargs.get("type") else None
            elif isinstance(formitem, str):
                formitem = FormItem(type=formitem)
            else:
                formitem = None
        if formitem is not None:
            pass
        elif self.modelfield.type_ in [str, Any]:
            kwargs["type"] = "input-text"
        elif issubclass(self.modelfield.type_, Choices):
            kwargs.update(
                {
                    "type": "select",
                    "options": [{"label": l, "value": v} for v, l in self.modelfield.type_.choices],
                    "extractValue": True,
                    "joinValues": False,
                }
            )
            if not self.modelfield.required:
                kwargs["clearable"] = True
        elif issubclass(self.modelfield.type_, bool):
            kwargs["type"] = "switch"
        elif is_filter:
            if issubclass(self.modelfield.type_, datetime.datetime):
                kwargs["type"] = "input-datetime-range"
                kwargs["format"] = "YYYY-MM-DD HH:mm:ss"
                # 给筛选的 DateTimeRange 添加 today 标签
                kwargs["ranges"] = "today,yesterday,7daysago,prevweek,thismonth,prevmonth,prevquarter"
            elif issubclass(self.modelfield.type_, datetime.date):
                kwargs["type"] = "input-date-range"
                kwargs["format"] = "YYYY-MM-DD"
            elif issubclass(self.modelfield.type_, datetime.time):
                kwargs["type"] = "input-time-range"
                kwargs["format"] = "HH:mm:ss"
            else:
                kwargs["type"] = "input-text"
        elif issubclass(self.modelfield.type_, int):
            formitem = InputNumber(precision=0, validations=Validation(isInt=True))
        elif issubclass(self.modelfield.type_, float):
            formitem = InputNumber(validations=Validation(isFloat=True))
        elif issubclass(self.modelfield.type_, datetime.datetime):
            kwargs["type"] = "input-datetime"
            kwargs["format"] = "YYYY-MM-DD HH:mm:ss"
        elif issubclass(self.modelfield.type_, datetime.date):
            kwargs["type"] = "input-date"
            kwargs["format"] = "YYYY-MM-DD"
        elif issubclass(self.modelfield.type_, datetime.time):
            kwargs["type"] = "input-time"
            kwargs["format"] = "HH:mm:ss"
        elif issubclass(self.modelfield.type_, Json):
            kwargs["type"] = "json-editor"
        else:
            kwargs["type"] = "input-text"
        return formitem or FormItem(**kwargs)

    def _parse_table_column_from_kwargs(self) -> TableColumn:
        kwargs = {}
        column = self.modelfield.field_info.extra.get("amis_table_column")
        if column is not None:
            column = smart_deepcopy(column)
            if isinstance(column, TableColumn):
                pass
            elif isinstance(column, dict):
                kwargs = column
                column = TableColumn(**kwargs) if kwargs.get("type") else None
            elif isinstance(column, str):
                column = TableColumn(type=column)
            else:
                column = None
        if column is not None:
            pass
        elif self.modelfield.type_ in [str, Any]:
            pass
        elif issubclass(self.modelfield.type_, bool):
            kwargs["type"] = "switch"
            kwargs["filterable"] = {
                "options": [
                    {"label": _("YES"), "value": True},
                    {"label": _("NO"), "value": False},
                ]
            }
        elif issubclass(self.modelfield.type_, datetime.datetime):
            kwargs["type"] = "datetime"
        elif issubclass(self.modelfield.type_, datetime.date):
            kwargs["type"] = "date"
        elif issubclass(self.modelfield.type_, datetime.time):
            kwargs["type"] = "time"
        elif issubclass(self.modelfield.type_, Choices):
            kwargs["type"] = "mapping"
            kwargs["filterable"] = {"options": [{"label": v, "value": k} for k, v in self.modelfield.type_.choices]}
            kwargs["map"] = {
                k: f"<span class='label label-{l}'>{v}</span>"
                for (k, v), l in zip(self.modelfield.type_.choices, cyclic_generator(LabelEnum))
            }
        return column or TableColumn(**kwargs)


def cyclic_generator(iterable: Iterable):
    while True:
        yield from iterable


class AmisParser:
    """AmisParser,used to parse pydantic fields to amis form item or table column.
    Compared with ModelFieldParser, AmisParser can set the default image and file upload receiver.
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

    def as_form_item(self, modelfield: ModelField, set_default: bool = False, is_filter: bool = False) -> FormItem:
        formitem = ModelFieldParser(modelfield).as_form_item(set_default=set_default, is_filter=is_filter)
        if isinstance(formitem, amis.InputImage) and not formitem.receiver:
            formitem.receiver = self.image_receiver
        elif isinstance(formitem, amis.InputFile) and not formitem.receiver:
            formitem.receiver = self.file_receiver
        elif isinstance(formitem, amis.InputRichText):
            formitem.receiver = formitem.receiver or self.image_receiver
            formitem.videoReceiver = formitem.videoReceiver or self.file_receiver
        if formitem.type in {"input-image", "input-file"}:
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

    def as_table_column(self, modelfield: ModelField, quick_edit: bool = False) -> TableColumn:
        column = ModelFieldParser(modelfield).as_table_column()
        if quick_edit:
            column.quickEdit = self.as_form_item(modelfield, set_default=True).dict(
                exclude_none=True, by_alias=True, exclude={"name", "label"}
            )
            column.quickEdit.update({"saveImmediately": True})
            if column.quickEdit.get("type") == "switch":
                column.quickEdit.update({"mode": "inline"})
        return column
