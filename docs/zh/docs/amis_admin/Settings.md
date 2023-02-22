## Settings

- 站点设置

### 继承基类

- #### [Pydantic BaseSettings](https://pydantic-docs.helpmanual.io/usage/settings/)

### 字段

#### debug

- 是否开启管理站点调试.
- 默认: False

#### site_title

- 当前管理站点标题

#### site_icon

- 当前管理站点ICON

#### site_url

- 当前管理站点url

#### site_path

- 当前管理站点挂载在FastAPI实例下的路径.

#### database_url_async

- 当前管理站点`sqlalchemy`数据库引擎异步连接url.

#### database_url

- 当前管理站点`sqlalchemy`数据库引擎同步连接url.

#### language

- 当前管理站点项目使用的国际化语言.系统默认内置支持语言有:`en_US`,`zh_CN`
- 从 0.1.1 版本开始系统默认语言依次尝试设置环境变量`LANGUAGE`/`LANG` > 操作系统默认语言 > 英文`en_US`
- 注意: 设置此值并不会直接切换语言,请参考教程([多语言](/tutorials/basic/i18n/))进行切换语言环境.

#### amis_cdn

- 当前管理站点Amis页面CDN地址, 例如: `https://npm.elemecdn.com`
- 默认: `https://unpkg.com`

#### amis_pkg

- 当前管理站点Amis版本, 例如: `amis@beta` , `amis@1.9.0`
- 默认: `amis@1.10.1`
- 默认值在`FastAPI-Amis-Admin`每次发布新版本后可能会改变,建议项目设置自己的稳定的Amis版本.

#### amis_theme

- 当前管理站点Amis模板主题, 可选: `cxd` , `antd`
- 默认: `cxd`

#### logger

- 当前管理站点日志记录器,支持: `logging` , `loguru`
- 默认: `logging.getLogger("fastapi_amis_admin")`