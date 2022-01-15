from pydantic import BaseSettings, Field, RedisDsn


class Settings(BaseSettings):
    '''项目配置'''
    debug: bool = False
    version: str = '0.0.0'  # api版本号
    database_url_async: str = Field(..., env='DATABASE_URL_ASYNC')

