import logging
from typing import Any, Union

from pydantic import BaseSettings, Field, root_validator, validator
from typing_extensions import Literal

from fastapi_amis_admin.amis import API


class Settings(BaseSettings):
    """Project configuration"""

    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False
    version: str = "0.0.0"
    site_title: str = "FastAPI Amis Admin"
    site_icon: str = "https://baidu.gitee.io/amis/static/favicon_b3b0647.png"
    site_url: str = ""
    root_path: str = "/admin"
    database_url_async: str = Field("", env="DATABASE_URL_ASYNC")
    database_url: str = Field("", env="DATABASE_URL")
    language: Union[Literal["zh_CN", "en_US", "de_DE"], str] = ""
    amis_cdn: str = "https://unpkg.com"
    amis_pkg: str = "amis@2.4.0"
    amis_theme: Literal["cxd", "antd", "dark", "ang"] = "cxd"
    amis_image_receiver: API = None  # Image upload interface
    amis_file_receiver: API = None  # File upload interface
    logger: Union[logging.Logger, Any] = logging.getLogger("fastapi_amis_admin")

    @validator("amis_cdn", "root_path", "site_url", pre=True)
    def valid_url(cls, url: str):
        return url[:-1] if url.endswith("/") else url

    @root_validator(pre=True)
    def valid_database_url(cls, values):
        if not values.get("database_url") and not values.get("database_url_async"):
            values.setdefault(
                "database_url",
                "sqlite+aiosqlite:///amisadmin.db?check_same_thread=False",
            )
        return values

    @validator("amis_image_receiver", "amis_file_receiver", pre=True)
    def valid_receiver(cls, v, values):
        return v or f"post:{values.get('root_path', '')}/file/upload"
