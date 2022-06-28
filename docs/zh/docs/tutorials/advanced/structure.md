# 目录结构

在实际项目开发中,涉及的数据模型及管理页面数量一般都比较多,`fastapi-amis-admin`建议项目采用类似django项目的目录结构.
请参考[fastapi_amis_admin_demo](https://github.com/amisadmin/fastapi_amis_admin_demo), 但是这并非强制限制,你也可以采用你自己熟悉的目录结构.

## 执行初始化命令

通过执行以下命令可以快速生成初始化项目文件

```bash
# 初始化一个`FastAPI-Amis-Admin`项目
faa new project_name --init

# 初始化一个`FastAPI-Amis-Admin`应用
faa new app_name
```

## 示例项目结构

```
│.
│  .gitignore
│  docker-compose.yml
│  Dockerfile
│  README.md
│  
├─backend
│  │  .env
│  │  alembic.ini
│  │  amisadmin.db
│  │  main.py
│  │  requirements.txt
│  │  
│  ├─apps
│  │  │  __init__.py
│  │  │  
│  │  ├─blog
│  │  │  │  admin.py
│  │  │  │  apis.py
│  │  │  │  views.py
│  │  │  │  models.py
│  │  │  │  schemas.py
│  │  │  │  jobs.py
│  │  │  │  settings.py
│  │  │  │  __init__.py
│  │  │  │  
│  │  │  ├─templates
│  │  │  ├─static
│  │  │  
│  │  │          
│  │  ├─demo
│  │     │  admin.py
│  │     │  __init__.py
│  │     │  
│  │     ├─templates
│  │     │      element.html
│  │     │      simple.html
│  │          
│  ├─core
│  │  │  adminsite.py
│  │  │  settings.py
│  │  │  __init__.py
│  │          
│  ├─migrations
│  │  │  env.py
│  │  │  README
│  │  │  script.py.mako
│  │  │  
│  │  ├─versions
│  │     │  bcd68ae939ea_add_url.py
│  │     │  c79e1785119e_init.py
│  │          
│  ├─upload
│  │          
│  ├─utils
│          
├─scripts
       run.sh

```

