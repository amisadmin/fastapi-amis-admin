import logging
from typing import Any, Union

from typing_extensions import Literal

from fastapi_amis_admin.amis import API
from fastapi_amis_admin.utils.pydantic import PYDANTIC_V2, BaseSettings


class Settings(BaseSettings):
    """Project configuration"""

    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False
    version: str = "0.0.0"
    site_title: str = "FastAPI Amis Admin"
    site_icon: str = "https://baidu.gitee.io/amis/static/favicon_b3b0647.png"
    site_url: str = ""
    site_path: str = "/admin"
    database_url_async: str = ""
    database_url: str = ""
    language: Union[Literal["zh_CN", "en_US", "de_DE"], str] = ""
    amis_cdn: str = "https://unpkg.com"
    amis_pkg: str = "amis@3.5.2"
    amis_theme: Literal["cxd", "antd", "dark", "ang"] = "cxd"
    amis_image_receiver: API = None  # Image upload interface
    amis_file_receiver: API = None  # File upload interface
    logger: Union[logging.Logger, Any] = logging.getLogger("fastapi_amis_admin")

    @classmethod
    def valid_url_(cls, url: str):
        return url[:-1] if url.endswith("/") else url

    @classmethod
    def valid_database_url_(cls, values):
        # set default file upload api.
        file_upload_api = f"post:{values.get('site_path', '')}/file/upload"
        values.setdefault("amis_image_receiver", file_upload_api)
        values.setdefault("amis_file_receiver", file_upload_api)
        # set default database url.
        if not values.get("database_url") and not values.get("database_url_async"):
            values.setdefault(
                "database_url_async",
                "sqlite+aiosqlite:///amisadmin.db?check_same_thread=False",
            )
        return values

    if PYDANTIC_V2:
        from pydantic import field_validator, model_validator

        valid_url = field_validator("amis_cdn", "site_path", "site_url", mode="before")(lambda cls, v: cls.valid_url_(v))
        valid_database_url = model_validator(mode="before")(lambda cls, values: cls.valid_database_url_(values))

    else:
        from pydantic import root_validator, validator

        valid_url = validator("amis_cdn", "site_path", "site_url", pre=True)(lambda cls, v: cls.valid_url_(v))
        valid_database_url = root_validator(pre=True, allow_reuse=True)(lambda cls, values: cls.valid_database_url_(values))


if PYDANTIC_V2:
    Settings.model_rebuild()
