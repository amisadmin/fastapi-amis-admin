import datetime
from pydantic import Json
from pydantic.fields import ModelField
from pydantic.utils import smart_deepcopy
from fastapi_amis_admin.amis.components import FormItem, Remark, Validation, InputNumber, TableColumn
from fastapi_amis_admin.models.enums import Choices


class AmisParser():

    def __init__(self, modelfield: ModelField):
        self.modelfield = modelfield  # read only

    @property
    def label(self):
        return self.modelfield.field_info.title or self.modelfield.name

    @property
    def remark(self):
        return Remark(
            content=self.modelfield.field_info.description) if self.modelfield.field_info.description else None

    def as_form_item(self, set_deafult: bool = False, is_filter: bool = False) -> FormItem:
        # sourcery no-metrics
        kwargs = {}
        formitem = self.modelfield.field_info.extra.get(['amis_form_item', 'amis_filter_item'][is_filter])
        if formitem is not None:
            formitem = smart_deepcopy(formitem)
            if isinstance(formitem, FormItem):
                pass
            elif isinstance(formitem, dict):
                kwargs = formitem
                formitem = FormItem(**kwargs) if kwargs.get('type') else None
            elif isinstance(formitem, str):
                formitem = FormItem(type=formitem)
            else:
                formitem = None
        if formitem is not None:
            pass
        elif self.modelfield.type_ == str:
            kwargs['type'] = 'input-text'
        elif issubclass(self.modelfield.type_, Choices):
            kwargs.update({
                'type': 'select',
                'options': [{'label': l, 'value': v} for v, l in self.modelfield.type_.choices],
                'extractValue': True,
                'joinValues': False,
            })
            if not self.modelfield.required:
                kwargs['clearable'] = True
        elif issubclass(self.modelfield.type_, bool):
            kwargs['type'] = 'switch'
        elif is_filter:
            if issubclass(self.modelfield.type_, datetime.datetime):
                kwargs['type'] = 'input-datetime-range'
                kwargs['format'] = 'YYYY-MM-DD HH:mm:ss'
                # 给筛选的 DateTimeRange 添加 today 标签
                kwargs['ranges'] = "today,yesterday,7daysago,prevweek,thismonth,prevmonth,prevquarter"
            elif issubclass(self.modelfield.type_, datetime.date):
                kwargs['type'] = 'input-date-range'
                kwargs['format'] = 'YYYY-MM-DD'
            elif issubclass(self.modelfield.type_, datetime.time):
                kwargs['type'] = 'input-time-range'
                kwargs['format'] = 'HH:mm:ss'
            else:
                kwargs['type'] = 'input-text'
        elif issubclass(self.modelfield.type_, int):
            formitem = InputNumber(precision=0, validations=Validation(isInt=True))
        elif issubclass(self.modelfield.type_, float):
            formitem = InputNumber(validations=Validation(isFloat=True))
        elif issubclass(self.modelfield.type_, datetime.datetime):
            kwargs['type'] = 'input-datetime'
            kwargs['format'] = 'YYYY-MM-DDTHH:mm:ss'
        elif issubclass(self.modelfield.type_, datetime.date):
            kwargs['type'] = 'input-date'
            kwargs['format'] = 'YYYY-MM-DD'
        elif issubclass(self.modelfield.type_, datetime.time):
            kwargs['type'] = 'input-time'
            kwargs['format'] = 'HH:mm:ss'
        elif issubclass(self.modelfield.type_, Json):
            kwargs['type'] = 'json-editor'
        else:
            kwargs['type'] = 'input-text'

        formitem = formitem or FormItem(**kwargs)
        if not is_filter:
            if self.modelfield.field_info.max_length:
                formitem.maxLength = self.modelfield.field_info.max_length
            if self.modelfield.field_info.min_length:
                formitem.minLength = self.modelfield.field_info.min_length
            formitem.required = self.modelfield.required
            if set_deafult and self.modelfield.default is not None:
                formitem.value = self.modelfield.default
        formitem.name = self.modelfield.alias
        formitem.label = formitem.label or self.label
        formitem.labelRemark = formitem.labelRemark or self.remark
        return formitem

    def as_table_column(self) -> TableColumn:
        kwargs = {}
        column = self.modelfield.field_info.extra.get('amis_table_column')
        if column is not None:
            column = smart_deepcopy(column)
            if isinstance(column, TableColumn):
                pass
            elif isinstance(column, dict):
                kwargs = column
                column = TableColumn(**kwargs) if kwargs.get('type') else None
            elif isinstance(column, str):
                column = TableColumn(type=column)
            else:
                column = None
        if column is not None:
            pass
        elif self.modelfield.type_ == str:
            pass
        elif issubclass(self.modelfield.type_, bool):
            kwargs['type'] = 'switch'
        elif issubclass(self.modelfield.type_, datetime.datetime):
            kwargs['type'] = 'datetime'
        elif issubclass(self.modelfield.type_, datetime.date):
            kwargs['type'] = 'date'
        elif issubclass(self.modelfield.type_, datetime.time):
            kwargs['type'] = 'time'
        elif issubclass(self.modelfield.type_, Choices):
            kwargs['type'] = 'mapping'
            kwargs['map'] = dict(self.modelfield.type_.choices)
        column = column or TableColumn(**kwargs)
        column.name = self.modelfield.alias
        column.label = column.label or self.label
        column.remark = column.remark or self.remark
        column.sortable = True
        return column
