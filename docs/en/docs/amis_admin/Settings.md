## Settings

- Site Settings

### Inherit from base class

- #### [Pydantic BaseSettings](https://pydantic-docs.helpmanual.io/usage/settings/)

### fields

#### debug

- Whether to enable management site debugging.
- Default: False

#### site_title

- Current admin site title

#### site_icon

- Current management site ICON

#### site_url

- current admin site url

#### site_path

- The path where the current management site is mounted under the FastAPI instance.

#### database_url_async

- Current admin site `sqlalchemy` database engine asynchronous connection url.

#### database_url

- Current admin site `sqlalchemy` database engine sync connection url.

#### language

- The international language used by the current management site project. The system default built-in supported languages ​​are: `en_US`, `zh_CN`
- Starting from version 0.1.1, try to set environment variables `LANGUAGE`/`LANG` > OS default language > English `en_US`
- Note: Setting this value does not directly switch the language, please refer to the tutorial ([Multilingual](/tutorials/basic/i18n/)) to switch the language environment.

#### amis_cdn

- CDN address of the current management site Amis page, for example: `https://npm.elemecdn.com`
- Default: `https://unpkg.com`

#### amis_pkg

- Current admin site Amis version, eg: `amis@beta` , `amis@1.9.0`
- Default: `amis@1.10.1`
- The default value may change after each release of `FastAPI-Amis-Admin`, it is recommended that projects set their own stable Amis version.

#### amis_theme

- current admin site Amis template theme, optional: `cxd` , `antd`
- Default: `cxd`

#### logger

- Currently admin site logger, supports: `logging` , `loguru`
- Default: `logging.getLogger("fastapi_amis_admin")`