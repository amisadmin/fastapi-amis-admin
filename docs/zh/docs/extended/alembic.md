# alembic 数据库迁移

## 创建迁移文件夹

- 项目第一次运行, 生成migrations文件夹

```bash
alembic init -t async migrations
```

## 修改配置文件

- env文件路径: `project/migrations/env.py`

```python
# 导入SQLModel

from sqlmodel import SQLModel  

# 导入模型数据

from app.models import *  

# 设置metadata

target_metadata = SQLModel.metadata

```

- ini文件路径: `project/alembic.ini`

```ini
# 修改成项目的异步数据库连接
sqlalchemy.url = sqlite+aiosqlite:///admisadmin.db
```

## 生成迁移文件

- 执行命令, 生成sqlModel 初始化迁移文件

```bash
alembic revision --autogenerate -m "init"
```

## 更新数据库

```bash
- 执行命令, 更新数据库: alembic_version
alembic upgrade head
```

## 迁移

- 以下命令在每次修改完模型后执行一次.

```bash
- 执行命令, 生成sqlModel 更新迁移文件
- "add year" 修改备注,每次命名不能重复!
alembic revision --autogenerate -m "add year"  

- 执行命令, 更新数据库: alembic_version
alembic upgrade head
```

## 参考文档:

- [FastAPI with Async SQLAlchemy, SQLModel, and Alembic | TestDriven.io](https://testdriven.io/blog/fastapi-sqlmodel/)

- [Alembic 1.7.5 documentation](https://alembic.sqlalchemy.org/en/latest/)
