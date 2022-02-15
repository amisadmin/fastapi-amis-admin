from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """项目配置"""
    debug: bool = False
    version: str = '0.0.0'
    site_url: str = ''
    root_path: str = '/admin'
    database_url_async: str = Field(..., env='DATABASE_URL_ASYNC')

