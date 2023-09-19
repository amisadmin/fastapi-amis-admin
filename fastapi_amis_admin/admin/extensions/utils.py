from typing import Dict, Iterable, Type

from pydantic import BaseModel

from fastapi_amis_admin.utils.pydantic import model_fields


def get_schema_fields_name_label(
    schema: Type[BaseModel],
    *,
    prefix: str = "",
    exclude_required: bool = False,
    exclude: Iterable[str] = None,
    include: Iterable[str] = None,
) -> Dict[str, str]:
    """获取schema字段名和标签.如果exclude中包含__all__,则返回空字典."""
    if not schema:
        return {}
    exclude = set(exclude or [])
    if "__all__" in exclude:
        return {}
    include = set(include or ["__all__"])
    fields = {}
    for field in model_fields(schema).values():
        if exclude_required and field.required:
            continue
        name = field.alias or field.name
        if name in exclude or (name not in include and "__all__" not in include):
            continue
        label = field.field_info.title or field.name
        fields[name] = prefix + label
    return fields
