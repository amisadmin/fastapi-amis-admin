# 项目介绍
<h2 align="center">
  FastAPI-Amis-Admin
</h2>
<p align="center">
    <em>fastapi-amis-admin是一个拥有高性能,高效率,易拓展的fastapi管理后台框架</em><br/>
    <em>启发自Django-Admin,并且拥有不逊色于Django-Admin的强大功能.</em>
</p>
<p align="center">
    <a href="https://github.com/amisadmin/fastapi_amis_admin/blob/master/LICENSE" target="_blank">
        <img src="https://img.shields.io/badge/license-Apache2.0-brightgreen" alt="Test">
    </a>
    <a href="https://pypi.org/project/fastapi_amis_admin" target="_blank">
        <img src="https://img.shields.io/badge/pypi-v0.0.11-blue" alt="Package version">
    </a>
    <a href="https://pypi.org/project/fastapi_amis_admin" target="_blank">
        <img src="https://img.shields.io/badge/python-3.6%2B-blue" alt="Supported Python versions">
    </a>
    <a href="https://jq.qq.com/?_wv=1027&k=U4Dv6x8W" target="_blank">
        <img src="https://img.shields.io/badge/qq群-229036692-orange" alt="229036692">
    </a>
</p>
<p align="center">
  <a href="https://github.com/amisadmin/fastapi_amis_admin" target="_blank">源码</a>
  ·
  <a href="http://demo.amis.work/admin" target="_blank">在线演示</a>
  ·
  <a href="http://docs.amis.work" target="_blank">文档</a>
  ·
  <a href="http://docs.gh.amis.work" target="_blank">文档打不开？</a>
</p>

------

`fastapi-amis-admin`是一个基于`fastapi`+`amis`开发的高性能并且高效率 `web-admin` 框架，使用 Python 3.6+ 并基于标准的 Python 类型提示。
`fastapi-amis-admin`开发的初衷是为了完善`fastapi`应用生态, 为`fastapi` web应用程序快速生成一个可视化管理后台. 
`fastapi-amis-admin`遵循`Apache2.0`协议免费开源, 但是为了更好的长期运营与维护此项目, `fastapi-amis-admin`非常希望能够得到大家的赞助与支持.



## 关键特性

- **性能极高**：基于[FastAPI](https://fastapi.tiangolo.com/zh/), 可享受FastAPI的全部优势。

- **效率更快**：完善的编码类型提示, 代码可重用性更高.

- **支持异步和同步混合编写**: `ORM`基于`SQLModel`+`Sqlalchemy`, 可自由定制数据库类型, 支持同步及异步模式, 可拓展性强. 

- **前后端分离**: 前端由`Amis`渲染, 后端接口由`fastapi-amis-admin`自动生成, 接口可重复利用.

- **可拓展性强**:  后台页面支持`Amis`页面及普通`html`页面,开发者可以很方便的自由定制界面.

- **自动生成API文档**: 由`FastAPI`自动生成接口文档,方便开发者调试,以及接口分享.



## 核心依赖

- [Fastapi](https://fastapi.tiangolo.com) 负责 web 部分
- [SQLModel](https://sqlmodel.tiangolo.com/) 负责ORM模型映射(完美结合[SQLAlchemy](https://www.sqlalchemy.org/)+[Pydantic](https://pydantic-docs.helpmanual.io/), 拥有`SQLAlchemy`和`Pydantic`的所有功能)
- [Amis](https://baidu.gitee.io/amis) 负责Admin后台页面展示



## 项目组成

`fastapi-amis-admin`由三部分核心模块组成,其中`python_amis`, `fastapi_crud` 可作为独立模块单独使用,`amis_admin`基于前者共同构建.

- `python_amis`: 基于`baidu amis`的`pydantic`数据模型构建库,用于快速生成,解析`amis` `json` 数据.
- `fastapi_crud`: 基于`FastAPI`+`SQLModel`, 用于快速构建Create,Read,Update,Delete通用API接口.
- `amis_admin`: 启发自`Django-Admin`, 结合`python_amis+fastapi_crud`, 用于快速构建Web Admin管理后台.

## 未来计划

- [ ] bug修复,细节完善.
- [ ] 完善用户教程文档.
- [ ] 不断拓展与完善核心功能.
- [ ] 增加用户认证与授权系统.

## 许可协议

- `fastapi-amis-admin`基于`Apache2.0`开源免费使用，可以免费用于商业用途，但请在展示界面中明确显示关于FastAPI-Amis-Admin的版权信息.

## 界面预览

![ModelAdmin](https://raw.githubusercontent.com/amisadmin/fastapi_amis_admin_demo/master/upload/img/ModelAdmin.png)

![Docs](https://raw.githubusercontent.com/amisadmin/fastapi_amis_admin_demo/master/upload/img/Docs.png)
