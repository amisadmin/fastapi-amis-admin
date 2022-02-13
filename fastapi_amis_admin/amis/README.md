## Amis介绍

[amis](https://github.com/baidu/amis) 是`Baidu`团队开发的一个低代码前端框架，它使用 `JSON` 配置来生成页面，可以减少页面开发工作量，极大提升效率。`python amis`基于`baidu amis` , 对`amis`数据结构通过[pydantic](https://pydantic-docs.helpmanual.io) 转换为对应的python数据模型,并添加部分常用方法.



## Amis亮点

- **不需要懂前端**：在百度内部，大部分 amis 用户之前从来没写过前端页面，也不会 `JavaScript`，却能做出专业且复杂的后台界面，这是所有其他前端 UI 库都无法做到的；
- **不受前端技术更新的影响**：百度内部最老的 amis 页面是 6 年多前创建的，至今还在使用，而当年的 `Angular/Vue/React` 版本现在都废弃了，当年流行的 `Gulp` 也被 `Webpack` 取代了，如果这些页面不是用 amis，现在的维护成本会很高；
- **享受 amis 的不断升级**：amis 一直在提升细节交互体验，比如表格首行冻结、下拉框大数据下不卡顿等，之前的 JSON 配置完全不需要修改；
- 可以 **完全** 使用 [可视化页面编辑器](https://aisuda.github.io/amis-editor-demo/) 来制作页面：一般前端可视化编辑器只能用来做静态原型，而 amis 可视化编辑器做出的页面是可以直接上线的。
- **提供完整的界面解决方案**：其它 UI 框架必须使用 JavaScript 来组装业务逻辑，而 amis 只需 JSON 配置就能完成完整功能开发，包括数据获取、表单提交及验证等功能，做出来的页面不需要经过二次开发就能直接上线；
- **大量内置组件（120+），一站式解决**：其它 UI 框架大部分都只有最通用的组件，如果遇到一些稍微不常用的组件就得自己找第三方，而这些第三方组件往往在展现和交互上不一致，整合起来效果不好，而 amis 则内置大量组件，包括了富文本编辑器、代码编辑器、diff、条件组合、实时日志等业务组件，绝大部分中后台页面开发只需要了解 amis 就足够了；
- **支持扩展**：除了低代码模式，还可以通过 [自定义组件](https://baidu.gitee.io/amis/zh-CN/docs/extend/internal) 来扩充组件，实际上 amis 可以当成普通 UI 库来使用，实现 90% 低代码，10% 代码开发的混合模式，既提升了效率，又不失灵活性；
- **容器支持无限级嵌套**：可以通过嵌套来满足各种布局及展现需求；
- **经历了长时间的实战考验**：amis 在百度内部得到了广泛使用，**在 6 年多的时间里创建了 5 万页面**，从内容审核到机器管理，从数据分析到模型训练，amis 满足了各种各样的页面需求，最复杂的页面有超过 1 万行 JSON 配置。



## 安装

```bash
pip install amis 
```



## 简单示例

**main.py**:

```python
from amis.components import Page

page = Page(title='标题', body='Hello World!')
# 输出为json
print(page.amis_json())
# 输出为dict
print(page.amis_dict())
# 输出页面html
print(page.amis_html())
```



## 开发文档

参考: [Amis官方文档](https://baidu.gitee.io/amis/zh-CN/docs/index)



## 依赖项目

- [pydantic](https://pydantic-docs.helpmanual.io/) 

- [amis](https://baidu.gitee.io/amis) 

  

## 许可协议

该项目遵循 Apache2.0 许可协议。



