from typing import Literal

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """项目配置"""
    debug: bool = False
    version: str = '0.0.0'
    site_url: str = ''
    root_path: str = '/admin'
    database_url_async: str = Field(..., env='DATABASE_URL_ASYNC')
    language: Literal['en_US', 'zh_CN'] = 'en_US'  # 'zh_CN'

    @validator('language', pre=True)
    def check_language(cls, v):
        return 'zh_CN' if str(v).startswith('zh') else 'en_US'
