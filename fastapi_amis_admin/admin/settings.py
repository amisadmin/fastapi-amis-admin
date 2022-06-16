from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """项目配置"""
    host: str = '127.0.0.1'
    port: int = 8000
    debug: bool = False
    version: str = '0.0.0'
    site_title: str = 'FastAPI Amis Admin'
    site_icon: str = 'https://baidu.gitee.io/amis/static/favicon_b3b0647.png'
    site_url: str = ''
    root_path: str = '/admin'
    database_url_async: str = Field(..., env='DATABASE_URL_ASYNC')
    language: str = ''  # 'zh_CN','en_US'
    amis_cdn: str = 'https://unpkg.com'
    amis_pkg: str = 'amis@1.10.2'

    @validator('amis_cdn', 'root_path', 'site_url', pre=True)
    def valid_url(url: str):
        return url[:-1] if url.endswith('/') else url
