"""详细文档阅读地址: https://baidu.gitee.io/amis/zh-CN/components"""
from typing import Union, List, Optional, Any
from pydantic import Field
from .constants import LevelEnum, DisplayModeEnum, SizeEnum
from .types import API, Expression, AmisNode, SchemaNode, Template, BaseAmisModel, OptionsNode
from .utils import amis_templates
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

class Html(AmisNode):
    """Html"""
    type: str = "html"  # 指定为 html 组件
    html: str  # html  当需要获取数据域中变量时，使用 Tpl 。


class Icon(AmisNode):
    """图标"""
    type: str = "icon"  # 指定组件类型
    className: str = None  # 外层 CSS 类名
    icon: str = None  # icon 名，支持 fontawesome v4 或使用 url


class Remark(AmisNode):
    """标记"""
    type: str = "remark"  # remark
    className: str = None  # 外层 CSS 类名
    content: str = None  # 提示文本
    placement: str = None  # 弹出位置
    trigger: str = None  # 触发条件 ['hover', 'focus']
    icon: str = None  # "fa fa-question-circle"  # 图标


class Tpl(AmisNode):
    type: str = "tpl"  # 指定为 Tpl 组件
    tpl: str  # 配置模板
    className: str = None  # 外层 Dom 的类名


##########################其他########################
class Badge(AmisNode):
    """角标"""
    mode: str = "dot"  # 角标类型，可以是 dot/text/ribbon
    text: Union[str, int] = None  # 角标文案，支持字符串和数字，在mode='dot'下设置无效
    size: int = None  # 角标大小
    level: str = None  # 角标级别, 可以是info/success/warning/danger, 设置之后角标背景颜色不同
    overflowCount: int = 99  # 设置封顶的数字值
    position: str = "top-right"  # 角标位置， 可以是top-right/top-left/bottom-right/bottom-left
    offset: int = None  # 角标位置，优先级大于position，当设置了offset后，以postion为top-right为基准进行定位  number[top, left]
    className: str = None  # 外层 dom 的类名
    animation: bool = None  # 角标是否显示动画
    style: dict = None  # 角标的自定义样式
    visibleOn: Expression = None  # 控制角标的显示隐藏


##########################布局########################

class Page(AmisNode):
    """页面"""
    type: str = "page"  # 指定为 Page 组件
    title: SchemaNode = None  # 页面标题
    subTitle: SchemaNode = None  # 页面副标题
    remark: "Remark" = None  # 标题附近会出现一个提示图标，鼠标放上去会提示该内容。
    aside: SchemaNode = None  # 往页面的边栏区域加内容
    asideResizor: bool = None  # 页面的边栏区域宽度是否可调整
    asideMinWidth: int = None  # 页面边栏区域的最小宽度
    asideMaxWidth: int = None  # 页面边栏区域的最大宽度
    toolbar: SchemaNode = None  # 往页面的右上角加内容，需要注意的是，当有 title 时，该区域在右上角，没有时该区域在顶部
    body: SchemaNode = None  # 往页面的内容区域加内容
    className: str = None  # 外层 dom 类名
    cssVars: dict = None  # 自定义 CSS 变量，请参考样式
    toolbarClassName: str = None  # "v-middle wrapper text-right bg-light b-b"  # Toolbar dom 类名
    bodyClassName: str = None  # "wrapper"  # Body dom 类名
    asideClassName: str = None  # "w page-aside-region bg-auto"  # Aside dom 类名
    headerClassName: str = None  # "bg-light b-b wrapper"  # Header 区域 dom 类名
    initApi: API = None  # Page 用来获取初始数据的 api。返回的数据可以整个 page 级别使用。
    initFetch: bool = None  # True  # 是否起始拉取 initApi
    initFetchOn: Expression = None  # 是否起始拉取 initApi, 通过表达式配置
    interval: int = None  # 刷新时间(最小 1000)
    silentPolling: bool = None  # False  # 配置刷新时是否显示加载动画
    stopAutoRefreshWhen: Expression = None  # 通过表达式来配置停止刷新的条件
    regions: List[str] = None

    def amis_html(self, template_path: str = ''):
        """渲染html模板"""
        return amis_templates('page.html', template_path).replace(
            '[[AmisSchemaJson]]', self.amis_json()
        )


class Divider(AmisNode):
    """分割线"""
    type: str = "divider"  # "Divider"
    className: str = None  # 外层 Dom 的类名
    lineStyle: str = None  # 分割线的样式，支持dashed和solid


class Flex(AmisNode):
    """布局"""
    type: str = "flex"  # 指定为 Flex 渲染器
    className: str = None  # css 类名
    justify: str = None  # "start", "flex-start", "center", "end", "flex-end", "space-around", "space-between", "space-evenly"
    alignItems: str = None  # "stretch", "start", "flex-start", "flex-end", "end", "center", "baseline"
    style: dict = None  # 自定义样式
    items: List[SchemaNode] = None  #


class Grid(AmisNode):
    """水平布局"""

    class Column(AmisNode):
        """列配置"""
        xs: int = None  # "auto"   # 宽度占比： 1 - 12
        ClassName: str = None  # 列类名
        sm: int = None  # "auto"  # 宽度占比： 1 - 12
        md: int = None  # "auto"   # 宽度占比： 1 - 12
        lg: int = None  # "auto"   # 宽度占比： 1 - 12
        valign: str = None  # 'top' | 'middle' | 'bottom' | 'between = None # 当前列内容的垂直对齐
        body: List[SchemaNode] = None  #

    type: str = "grid"  # 指定为 Grid 渲染器
    className: str = None  # 外层 Dom 的类名
    gap: str = None  # 'xs' | 'sm' | 'base' | 'none' | 'md' | 'lg = None # 水平间距
    valign: str = None  # 'top' | 'middle' | 'bottom' | 'between = None # 垂直对齐方式
    align: str = None  # 'left' | 'right' | 'between' | 'center = None # 水平对齐方式
    columns: List[SchemaNode] = None  #


class Panel(AmisNode):
    """面板"""
    type: str = "panel"  # 指定为 Panel 渲染器
    className: str = None  # "panel-default"  # 外层 Dom 的类名
    headerClassName: str = None  # "panel-heading"  # header 区域的类名
    footerClassName: str = None  # "panel-footer bg-light lter wrapper"  # footer 区域的类名
    actionsClassName: str = None  # "panel-footer"  # actions 区域的类名
    bodyClassName: str = None  # "panel-body"  # body 区域的类名
    title: SchemaNode = None  # 标题
    header: SchemaNode = None  # 头部容器
    body: SchemaNode = None  # 内容容器
    footer: SchemaNode = None  # 底部容器
    affixFooter: bool = None  # 是否固定底部容器
    actions: List["Action"] = None  # 按钮区域


class Tabs(AmisNode):
    """选项卡"""

    class Item(AmisNode):
        title: str = None  # Tab 标题
        icon: Icon = None  # Tab 的图标
        tab: SchemaNode = None  # 内容区
        hash: str = None  # 设置以后将跟 url 的 hash 对应
        reload: bool = None  # 设置以后内容每次都会重新渲染，对于 crud 的重新拉取很有用
        unmountOnExit: bool = None  # 每次退出都会销毁当前 tab 栏内容
        className: str = "bg-white b-l b-r b-b wrapper-md"  # Tab 区域样式

    type: str = "tabs"  # 指定为 Tabs 渲染器
    className: str = None  # 外层 Dom 的类名
    mode: str = None  # 展示模式，取值可以是 line、card、radio、vertical
    tabsClassName: str = None  # Tabs Dom 的类名
    tabs: List[Item] = None  # tabs 内容
    source: str = None  # tabs 关联数据，关联后可以重复生成选项卡
    toolbar: SchemaNode = None  # tabs 中的工具栏
    toolbarClassName: str = None  # tabs 中工具栏的类名
    mountOnEnter: bool = None  # False  # 只有在点中 tab 的时候才渲染
    unmountOnExit: bool = None  # False  # 切换 tab 的时候销毁
    scrollable: bool = None  # False  # 是否导航支持内容溢出滚动，vertical和chrome模式下不支持该属性；chrome模式默认压缩标签


class Horizontal(AmisNode):
    left: int = None  # 左边 label 的宽度占比
    right: int = None  # 右边控制器的宽度占比。
    offset: int = None  # 当没有设置 label 时，右边控制器的偏移量


##########################功能########################
class Action(AmisNode):
    """行为按钮"""
    type: str = "button"  # 指定为 Page 渲染器。 button  action
    actionType: str  # 【必填】这是 action 最核心的配置，来指定该 action 的作用类型，支持：ajax、link、url、drawer、dialog、confirm、cancel、prev、next、copy、close。
    label: str = None  # 按钮文本。可用 ${xxx} 取值。
    level: LevelEnum = None  # 按钮样式，支持：link、primary、secondary、info、success、warning、danger、light、dark、default。
    size: str = None  # 按钮大小，支持：xs、sm、md、lg。
    icon: str = None  # 设置图标，例如fa fa-plus。
    iconClassName: str = None  # 给图标上添加类名。
    rightIcon: str = None  # 在按钮文本右侧设置图标，例如fa fa-plus。
    rightIconClassName: str = None  # 给右侧图标上添加类名。
    active: bool = None  # 按钮是否高亮。
    activeLevel: str = None  # 按钮高亮时的样式，配置支持同level。
    activeClassName: str = None  # 给按钮高亮添加类名。 "is-active"
    block: bool = None  # 用display:"block"来显示按钮。
    confirmText: Template = None  # 当设置后，操作在开始前会询问用户。可用 ${xxx} 取值。
    reload: str = None  # 指定此次操作完后，需要刷新的目标组件名字（组件的name值，自己配置的），多个请用 , 号隔开。
    tooltip: str = None  # 鼠标停留时弹出该段文字，也可以配置对象类型：字段为title和content。可用 ${xxx} 取值。
    disabledTip: str = None  # 被禁用后鼠标停留时弹出该段文字，也可以配置对象类型：字段为title和content。可用 ${xxx} 取值。
    tooltipPlacement: str = None  # 如果配置了tooltip或者disabledTip，指定提示信息位置，可配置top、bottom、left、right。
    close: Union[
        bool, str] = None  # 当action配置在dialog或drawer的actions中时，配置为true指定此次操作完后关闭当前dialog或drawer。当值为字符串，并且是祖先层弹框的名字的时候，会把祖先弹框关闭掉。
    required: List[str] = None  # 配置字符串数组，指定在form中进行操作之前，需要指定的字段名的表单项通过验证
    # primary:bool=None


class ActionType:
    """行为按钮类型"""

    class Ajax(Action):
        actionType: str = 'ajax'  # 点击后显示一个弹出框
        api: API = None  # 请求地址，参考 api 格式说明。
        redirect: Template = None  # 指定当前请求结束后跳转的路径，可用 ${xxx} 取值。
        feedback: "Dialog" = None  # 如果 ajax 类型的，当 ajax 返回正常后，还能接着弹出一个 dialog 做其他交互。返回的数据可用于这个 dialog 中。格式可参考Dialog
        messages: dict = None  # success：ajax 操作成功后提示，可以不指定，不指定时以 api 返回为准。failed：ajax 操作失败提示。

    class Dialog(Action):
        actionType: str = 'dialog'  # 点击后显示一个弹出框
        dialog: Union["Dialog", "Service", SchemaNode]  # 指定弹框内容，格式可参考Dialog
        nextCondition: bool = None  # 可以用来设置下一条数据的条件，默认为 true。

    class Drawer(Action):
        actionType: str = 'drawer'  # 点击后显示一个侧边栏
        drawer: Union["Drawer", "Service", SchemaNode]  # 指定弹框内容，格式可参考Drawer

    class Copy(Action):
        actionType: str = 'copy'  # 复制一段内容到粘贴板
        content: Template  # 指定复制的内容。可用 ${xxx} 取值。
        copyFormat: str = None  # 可以通过 copyFormat 设置复制的格式，默认是文本 text/html

    class Url(Action):
        """直接跳转"""
        actionType: str = 'url'  # 直接跳转
        url: str  # 按钮点击后，会打开指定页面。可用 ${xxx} 取值。
        blank: bool = None  # false 如果为 true 将在新 tab 页面打开。

    class Link(Action):
        """单页跳转"""
        actionType: str = 'link'  # 单页跳转
        link: str  # 用来指定跳转地址，跟 url 不同的是，这是单页跳转方式，不会渲染浏览器，请指定 amis 平台内的页面。可用 ${xxx} 取值。


class PageSchema(AmisNode):
    """页面配置"""
    label: str = None  # 菜单名称。
    icon: str = None  # 菜单图标，比如：fa fa-file.
    url: str = None  # 页面路由路径，当路由命中该路径时，启用当前页面。当路径不是 / 打头时，会连接父级路径。比如：父级的路径为 folder，而此时配置 pageA, 那么当页面地址为 /folder/pageA 时才会命中此页面。当路径是 / 开头如： /crud/list 时，则不会拼接父级路径。另外还支持 /crud/view/:id 这类带参数的路由，页面中可以通过 ${params.id} 取到此值。
    schema_: Page = Field(None, alias='schema')  # 页面的配置，具体配置请前往 Page 页面说明
    schemaApi: API = None  # 如果想通过接口拉取，请配置。返回路径为 json>data。schema 和 schemaApi 只能二选一。
    link: str = None  # 如果想配置个外部链接菜单，只需要配置 link 即可。
    redirect: str = None  # 跳转，当命中当前页面时，跳转到目标页面。
    rewrite: str = None  # 改成渲染其他路径的页面，这个方式页面地址不会发生修改。
    isDefaultPage: Union[str, bool] = None  # 当你需要自定义 404 页面的时候有用，不要出现多个这样的页面，因为只有第一个才会有用。
    visible: str = None  # 有些页面可能不想出现在菜单中，可以配置成 false，另外带参数的路由无需配置，直接就是不可见的。
    className: str = None  # 菜单类名。
    children: List["PageSchema"] = None  # 子菜单
    sort: int = None  # 排序


class App(AmisNode):
    """多页应用"""
    type: str = "app"
    api: API = None  # 页面配置接口，如果你想远程拉取页面配置请配置。返回配置路径 json>data>pages，具体格式请参考 pages 属性。
    brandName: str = None  # 应用名称
    logo: str = None  # 支持图片地址，或者 svg。
    className: str = None  # css 类名
    header: str = None  # header
    asideBefore: str = None  # 页面菜单上前面区域。
    asideAfter: str = None  # 页面菜单下前面区域。
    footer: str = None  # 页面。
    pages: List[
        PageSchema] = None  # Array<页面配置>具体的页面配置。 通常为数组，数组第一层为分组，一般只需要配置 label 集合，如果你不想分组，直接不配置，真正的页面请在第二层开始配置，即第一层的 children 中。

    def amis_html(self, template_path: str = ''):
        """渲染html模板"""
        return amis_templates('app.html', template_path).replace(
            '[[AmisSchemaJson]]', self.amis_json()
        )


class ButtonGroup(AmisNode):
    """按钮组"""
    type: str = 'button-group'
    buttons: List[Action]  # 行为按钮组
    className: str = None  # 外层 Dom 的类名
    vertical: bool = None  # 是否使用垂直模式


class Service(AmisNode):
    """功能型容器"""
    type: str = "service"  # 指定为 service 渲染器
    className: str = None  # 外层 Dom 的类名
    body: SchemaNode = None  # 内容容器
    api: API = None  # 初始化数据域接口地址
    ws: str = None  # WebScocket 地址
    dataProvider: str = None  # 数据获取函数
    initFetch: bool = None  # 是否默认拉取
    schemaApi: API = None  # 用来获取远程 Schema 接口地址
    initFetchSchema: bool = None  # 是否默认拉取 Schema
    messages: dict = None  # 消息提示覆写，默认消息读取的是接口返回的 toast 提示文字，但是在此可以覆写它。
    # messages.fetchSuccess: str = None  # 接口请求成功时的 toast 提示文字
    # messages.fetchFailed: str = "初始化失败"  # 接口请求失败时 toast 提示文字
    interval: int = None  # 轮询时间间隔(最低 3000)
    silentPolling: bool = None  # False  # 配置轮询时是否显示加载动画
    stopAutoRefreshWhen: Expression = None  # 配置停止轮询的条件


class Nav(AmisNode):
    """导航"""

    class Link(AmisNode):
        label: str = None  # 名称
        to: Template = None  # 链接地址
        target: str = None  # "链接关系"  #
        icon: str = None  # 图标
        children: List["Link"] = None  # 子链接
        unfolded: bool = None  # 初始是否展开
        active: bool = None  # 是否高亮
        activeOn: Expression = None  # 是否高亮的条件，留空将自动分析链接地址
        defer: bool = None  # 标记是否为懒加载项
        deferApi: API = None  # 可以不配置，如果配置优先级更高

    type: str = "nav"  # 指定为 Nav 渲染器
    className: str = None  # 外层 Dom 的类名
    stacked: bool = True  # 设置成 false 可以以 tabs 的形式展示
    source: API = None  # 可以通过变量或 API 接口动态创建导航
    deferApi: API = None  # 用来延时加载选项详情的接口，可以不配置，不配置公用 source 接口。
    itemActions: SchemaNode = None  # 更多操作相关配置
    draggable: bool = None  # 是否支持拖拽排序
    dragOnSameLevel: bool = None  # 仅允许同层级内拖拽
    saveOrderApi: API = None  # 保存排序的 api
    itemBadge: Badge = None  # 角标
    links: list = None  # 链接集合


class AnchorNav(AmisNode):
    """锚点导航"""

    class Link(AmisNode):
        label: str = None  # 名称
        title: str = None  # 区域 标题
        href: str = None  # 区域 标识
        body: SchemaNode = None  # 区域 内容区
        className: str = None  # "bg-white b-l b-r b-b wrapper-md"  # 区域成员 样式

    type: str = "anchor-nav"  # 指定为 AnchorNav 渲染器
    className: str = None  # 外层 Dom 的类名
    linkClassName: str = None  # 导航 Dom 的类名
    sectionClassName: str = None  # 锚点区域 Dom 的类名
    links: list = None  # links 内容
    direction: str = None  # "vertical"  # 可以配置导航水平展示还是垂直展示。对应的配置项分别是：vertical、horizontal
    active: str = None  # 需要定位的区域


##########################数据输入########################
class ButtonToolbar(AmisNode):
    """按钮工具栏"""
    type: str = 'button-toolbar'
    buttons: List[Action]  # 行为按钮组


class Validation(BaseAmisModel):
    isEmail: bool = None  # 必须是 Email。
    isUrl: bool = None  # 必须是 Url。
    isNumeric: bool = None  # 必须是 数值。
    isAlpha: bool = None  # 必须是 字母。
    isAlphanumeric: bool = None  # 必须是 字母或者数字。
    isInt: bool = None  # 必须是 整形。
    isFloat: bool = None  # 必须是 浮点形。
    isLength: int = None  # 是否长度正好等于设定值。
    minLength: int = None  # 最小长度。
    maxLength: int = None  # 最大长度。
    maximum: int = None  # 最大值。
    minimum: int = None  # 最小值。
    equals: str = None  # 当前值必须完全等于 xxx。
    equalsField: str = None  # 当前值必须与 xxx 变量值一致。
    isJson: bool = None  # 是否是合法的 Json 字符串。
    isUrlPath: bool = None  # 是 url 路径。
    isPhoneNumber: bool = None  # 是否为合法的手机号码
    isTelNumber: bool = None  # 是否为合法的电话号码
    isZipcode: bool = None  # 是否为邮编号码
    isId: bool = None  # 是否为身份证号码，没做校验
    matchRegexp: str = None  # 必须命中某个正则。 /foo/


class FormItem(AmisNode):
    """表单项通用"""
    type: str = 'input-text'  # 指定表单项类型
    className: str = None  # 表单最外层类名
    inputClassName: str = None  # 表单控制器类名
    labelClassName: str = None  # label 的类名
    name: str = None  # 字段名，指定该表单项提交时的 key
    label: Template = None  # 表单项标签  模板或false
    value: Union[int, str] = None  # 字段的值
    labelRemark: "Remark" = None  # 表单项标签描述
    description: Template = None  # 表单项描述
    placeholder: str = None  # 表单项描述
    inline: bool = None  # 是否为 内联 模式
    submitOnChange: bool = None  # 是否该表单项值发生变化时就提交当前表单。
    disabled: bool = None  # 当前表单项是否是禁用状态
    disabledOn: Expression = None  # 当前表单项是否禁用的条件
    visible: Expression = None  # 当前表单项是否禁用的条件
    visibleOn: Expression = None  # 当前表单项是否禁用的条件
    required: bool = None  # 是否为必填。
    requiredOn: Expression = None  # 过表达式来配置当前表单项是否为必填。
    validations: Union[Validation, Expression] = None  # 表单项值格式验证，支持设置多个，多个规则用英文逗号隔开。
    validateApi: Expression = None  # 表单校验接口


class Form(AmisNode):
    """表单"""

    class Messages(AmisNode):
        fetchSuccess: str = None  # 获取成功时提示
        fetchFailed: str = None  # 获取失败时提示
        saveSuccess: str = None  # 保存成功时提示
        saveFailed: str = None  # 保存失败时提示

    type: str = "form"  # "form" 指定为 Form 渲染器
    name: str = None  # 设置一个名字后，方便其他组件与其通信
    mode: DisplayModeEnum = None  # 表单展示方式，可以是：normal、horizontal 或者 inline
    horizontal: Horizontal = None  # 当 mode 为 horizontal 时有用，用来控制 label {"left": "col-sm-2", "right": "col-sm-10","offset": "col-sm-offset-2"}
    title: Optional[str] = None  # Form 的标题
    submitText: Optional[str] = "提交"  # 默认的提交按钮名称，如果设置成空，则可以把默认按钮去掉。
    className: str = None  # 外层 Dom 的类名
    body: List[Union[FormItem, SchemaNode]] = None  # Form 表单项集合
    actions: List["Action"] = None  # Form 提交按钮，成员为 Action
    actionsClassName: str = None  # actions 的类名
    messages: Messages = None  # 消息提示覆写，默认消息读取的是 API 返回的消息，但是在此可以覆写它。
    wrapWithPanel: bool = None  # 是否让 Form 用 panel 包起来，设置为 false 后，actions 将无效。
    panelClassName: str = None  # 外层 panel 的类名
    api: API = None  # Form 用来保存数据的 api。
    initApi: API = None  # Form 用来获取初始数据的 api。
    rules: list = None  # 表单组合校验规则 Array<{rule:string;message:string}>
    interval: int = None  # 刷新时间(最低 3000)
    silentPolling: bool = False  # 配置刷新时是否显示加载动画
    stopAutoRefreshWhen: str = None  # 通过表达式 来配置停止刷新的条件
    initAsyncApi: API = None  # Form 用来获取初始数据的 api,与 initApi 不同的是，会一直轮询请求该接口，直到返回 finished 属性为 true 才 结束。
    initFetch: bool = None  # 设置了 initApi 或者 initAsyncApi 后，默认会开始就发请求，设置为 false 后就不会起始就请求接口
    initFetchOn: str = None  # 用表达式来配置
    initFinishedField: Optional[
        str] = None  # 设置了 initAsyncApi 后，默认会从返回数据的 data.finished 来判断是否完成，也可以设置成其他的 xxx，就会从 data.xxx 中获取
    initCheckInterval: int = None  # 设置了 initAsyncApi 以后，默认拉取的时间间隔
    asyncApi: API = None  # 设置此属性后，表单提交发送保存接口后，还会继续轮询请求该接口，直到返回 finished 属性为 true 才 结束。
    checkInterval: int = None  # 轮询请求的时间间隔，默认为 3 秒。设置 asyncApi 才有效
    finishedField: Optional[str] = None  # 如果决定结束的字段名不是 finished 请设置此属性，比如 is_success
    submitOnChange: bool = None  # 表单修改即提交
    submitOnInit: bool = None  # 初始就提交一次
    resetAfterSubmit: bool = None  # 提交后是否重置表单
    primaryField: str = None  # 设置主键 id, 当设置后，检测表单是否完成时（asyncApi），只会携带此数据。
    target: str = None  # 默认表单提交自己会通过发送 api 保存数据，但是也可以设定另外一个 form 的 name 值，或者另外一个 CRUD 模型的 name 值。 如果 target 目标是一个 Form ，则目标 Form 会重新触发 initApi，api 可以拿到当前 form 数据。如果目标是一个 CRUD 模型，则目标模型会重新触发搜索，参数为当前 Form 数据。当目标是 window 时，会把当前表单的数据附带到页面地址上。
    redirect: str = None  # 设置此属性后，Form 保存成功后，自动跳转到指定页面。支持相对地址，和绝对地址（相对于组内的）。
    reload: str = None  # 操作完后刷新目标对象。请填写目标组件设置的 name 值，如果填写为 window 则让当前页面整体刷新。
    autoFocus: bool = None  # 是否自动聚焦。
    canAccessSuperData: bool = None  # 指定是否可以自动获取上层的数据并映射到表单项上
    persistData: str = None  # 指定一个唯一的 key，来配置当前表单是否开启本地缓存
    clearPersistDataAfterSubmit: bool = None  # 指定表单提交成功后是否清除本地缓存
    preventEnterSubmit: bool = None  # 禁用回车提交表单
    trimValues: bool = None  # trim 当前表单项的每一个值
    promptPageLeave: bool = None  # form 还没保存，即将离开页面前是否弹框确认。
    columnCount: int = None  # 表单项显示为几列
    debug: bool = None


class Button(FormItem):
    """按钮"""
    className: str = None  # 指定添加 button 类名
    href: str = None  # 点击跳转的地址，指定此属性 button 的行为和 a 链接一致
    size: str = None  # 设置按钮大小 'xs' | 'sm' | 'md' | 'lg'
    actionType: str = None  # 设置按钮类型 'button' | 'reset' | 'submit'| 'clear'| 'url'
    level: LevelEnum = None  # 设置按钮样式 'link' | 'primary' | 'enhance' | 'secondary' | 'info'|'success' | 'warning' | 'danger' | 'light'| 'dark' | 'default'
    tooltip: Union[str, dict] = None  # 气泡提示内容 TooltipObject
    tooltipPlacement: str = None  # 气泡框位置器 'top' | 'right' | 'bottom' | 'left'
    tooltipTrigger: str = None  # 触发 tootip 'hover' | 'focus'
    disabled: bool = None  # 按钮失效状态
    block: bool = None  # 将按钮宽度调整为其父宽度的选项
    loading: bool = None  # 显示按钮 loading 效果
    loadingOn: str = None  # 显示按钮 loading 表达式


class InputArray(FormItem):
    """数组输入框"""
    type: str = 'input-array'
    items: FormItem = None  # 配置单项表单类型
    addable: bool = None  # 是否可新增。
    removable: bool = None  # 是否可删除
    draggable: bool = False  # 是否可以拖动排序, 需要注意的是当启用拖动排序的时候，会多一个$id 字段
    draggableTip: str = None  # 可拖拽的提示文字，默认为："可通过拖动每行中的【交换】按钮进行顺序调整"
    addButtonText: str = "新增"  # 新增按钮文字
    minLength: int = None  # 限制最小长度
    maxLength: int = None  # 限制最大长度


class Hidden(FormItem):
    """隐藏字段"""
    type: str = 'hidden'


class Checkbox(FormItem):
    """勾选框"""
    type: str = 'checkbox'
    option: str = None  # 选项说明
    trueValue: Any = None  # 标识真值
    falseValue: Any = None  # 标识假值


class Checkboxes(FormItem):
    """复选框"""
    type: str = 'checkboxes'
    options: OptionsNode = None  # 选项组
    source: API = None  # 动态选项组
    delimeter: str = None  # ","  # 拼接符
    labelField: str = None  # "label"  # 选项标签字段
    valueField: str = None  # "value"  # 选项值字段
    joinValues: bool = None  # True  # 拼接值
    extractValue: bool = None  # False  # 提取值
    columnsCount: int = None  # 1  # 选项按几列显示，默认为一列
    checkAll: bool = None  # False  # 是否支持全选
    inline: bool = None  # True  # 是否显示为一行
    defaultCheckAll: bool = None  # False  # 默认是否全选
    creatable: bool = None  # False  # 新增选项
    createBtnLabel: str = None  # "新增选项"  # 新增选项
    addControls: List[FormItem] = None  # 自定义新增表单项
    addApi: API = None  # 配置新增选项接口
    editable: bool = None  # False  # 编辑选项
    editControls: List[FormItem] = None  # 自定义编辑表单项
    editApi: API = None  # 配置编辑选项接口
    removable: bool = None  # False  # 删除选项
    deleteApi: API = None  # 配置删除选项接口


class InputCity(FormItem):
    """城市选择器"""
    type: str = 'location-city'
    allowCity: bool = None  # True  # 允许选择城市
    allowDistrict: bool = None  # True  # 允许选择区域
    searchable: bool = None  # False  # 是否出搜索框
    extractValue: bool = None  # True  # 默认 true 是否抽取值，如果设置成 false 值格式会变成对象，包含 code、province、city 和 district 文字信息。


class InputColor(FormItem):
    """颜色选择器"""
    type: str = 'input-color'
    format: str = None  # "hex"  # 请选择 hex、hls、rgb或者rgba。
    presetColors: List[str] = None  # "选择器预设颜色值"  # 选择器底部的默认颜色，数组内为空则不显示默认颜色
    allowCustomColor: bool = None  # True  # 为false时只能选择颜色，使用 presetColors 设定颜色选择范围
    clearable: bool = None  # "label"  # 是否显示清除按钮
    resetValue: str = None  # ""  # 清除后，表单项值调整成该值


class Combo(FormItem):
    """组合"""
    type: str = 'combo'
    formClassName: str = None  # 单组表单项的类名
    addButtonClassName: str = None  # 新增按钮 CSS 类名
    items: List[FormItem] = None  # 组合展示的表单项
    # items[x].columnClassName: str = None  # 列的类名，可以用它配置列宽度。默认平均分配。
    # items[x].unique: bool = None  # 设置当前列值是否唯一，即不允许重复选择。
    noBorder: bool = False  # 单组表单项是否显示边框
    scaffold: dict = {}  # 单组表单项初始值
    multiple: bool = False  # 是否多选
    multiLine: bool = False  # 默认是横着展示一排，设置以后竖着展示
    minLength: int = None  # 最少添加的条数
    maxLength: int = None  # 最多添加的条数
    flat: bool = False  # 是否将结果扁平化(去掉 name),只有当 items 的 length 为 1 且 multiple 为 true 的时候才有效。
    joinValues: bool = True  # 默认为 true 当扁平化开启的时候，是否用分隔符的形式发送给后端，否则采用 array 的方式。
    delimiter: str = "False"  # 当扁平化开启并且 joinValues 为 true 时，用什么分隔符。
    addable: bool = False  # 是否可新增
    addButtonText: str = "新增"  # 新增按钮文字
    removable: bool = False  # 是否可删除
    deleteApi: API = None  # 如果配置了，则删除前会发送一个 api，请求成功才完成删除
    deleteConfirmText: str = "确认要删除？"  # 当配置 deleteApi 才生效！删除时用来做用户确认
    draggable: bool = False  # 是否可以拖动排序, 需要注意的是当启用拖动排序的时候，会多一个$id 字段
    draggableTip: str = "可通过拖动每行中的【交换】按钮进行顺序调整"  # 可拖拽的提示文字
    subFormMode: str = "normal"  # 可选normal、horizontal、inline
    placeholder: str = "``"  # 没有成员时显示。
    canAccessSuperData: bool = False  # 指定是否可以自动获取上层的数据并映射到表单项上
    conditions: dict = None  # 数组的形式包含所有条件的渲染类型，单个数组内的test 为判断条件，数组内的items为符合该条件后渲染的schema
    typeSwitchable: bool = False  # 是否可切换条件，配合conditions使用
    strictMode: bool = True  # 默认为严格模式，设置为 false 时，当其他表单项更新是，里面的表单项也可以及时获取，否则不会。
    syncFields: List[
        str] = "[]"  # 配置同步字段。只有 strictMode 为 false 时有效。如果 Combo 层级比较深，底层的获取外层的数据可能不同步。但是给 combo 配置这个属性就能同步下来。输入格式：["os"]
    nullable: bool = False  # 允许为空，如果子表单项里面配置验证器，且又是单条模式。可以允许用户选择清空（不填）。


class ConditionBuilder(FormItem):
    """组合条件"""

    class Field(AmisNode):
        type: str = "text"  # 字段配置中配置成 "text"
        label: str = None  # 字段名称。
        placeholder: str = None  # 占位符
        operators: List[
            str] = None  # 默认为 [ 'equal', 'not_equal', 'is_empty', 'is_not_empty', 'like', 'not_like', 'starts_with', 'ends_with' ] 如果不要那么多，可以配置覆盖。
        defaultOp: str = None  # 默认为 "equal"

    class Text(Field):
        """文本"""

    class Number(Field):
        """数字"""
        type: str = 'number'
        minimum: float = None  # 最小值
        maximum: float = None  # 最大值
        step: float = None  # 步长

    class Date(Field):
        """日期"""
        type: str = 'date'
        defaultValue: str = None  # 默认值
        format: str = None  # 默认 "YYYY-MM-DD" 值格式
        inputFormat: str = None  # 默认 "YYYY-MM-DD" 显示的日期格式。

    class Datetime(Date):
        """日期时间"""
        type: str = 'datetime'
        timeFormat: str = None  # 默认 "HH:mm" 时间格式，决定输入框有哪些。

    class Time(Date):
        """时间"""
        type: str = 'datetime'

    class Select(Field):
        """下拉选择"""
        type: str = 'select'
        options: OptionsNode = None  # 选项列表，Array<{label: string, value: any}>
        source: API = None  # 动态选项，请配置 api。
        searchable: bool = None  # 是否可以搜索
        autoComplete: API = None  # 自动提示补全，每次输入新内容后，将调用接口，根据接口返回更新选项。

    type: str = 'condition-builder'
    fields: List[Field] = None  # 为数组类型，每个成员表示一个可选字段，支持多个层，配置示例
    className: str = None  # 外层 dom 类名
    fieldClassName: str = None  # 输入字段的类名
    source: str = None  # 通过远程拉取配置项


class Editor(FormItem):
    """代码编辑器"""
    type: str = 'editor'
    language: str = None  # "javascript"  # 编辑器高亮的语言，支持通过 ${xxx} 变量获取
    # bat、 c、 coffeescript、 cpp、 csharp、 css、 dockerfile、 fsharp、 go、 handlebars、 html、 ini、 java、 javascript、 json、 less、 lua、 markdown、 msdax、 objective-c、 php、 plaintext、 postiats、 powershell、 pug、 python、 r、 razor、 ruby、 sb、 scss、shell、 sol、 sql、 swift、 typescript、 vb、 xml、 yaml
    size: str = None  # "md"  # 编辑器高度，取值可以是 md、lg、xl、xxl
    allowFullscreen: bool = None  # False  # 是否显示全屏模式开关
    options: dict = None  # monaco 编辑器的其它配置，比如是否显示行号等，请参考这里，不过无法设置 readOnly，只读模式需要使用 disabled: true


class InputFile(FormItem):
    """文件上传"""
    type: str = 'input-file'
    receiver: API = None  # 上传文件接口
    accept: str = None  # "text/plain"  # 默认只支持纯文本，要支持其他类型，请配置此属性为文件后缀.xxx
    asBase64: bool = None  # False  # 将文件以base64的形式，赋值给当前组件
    asBlob: bool = None  # False  # 将文件以二进制的形式，赋值给当前组件
    maxSize: int = None  # 默认没有限制，当设置后，文件大小大于此值将不允许上传。单位为B
    maxLength: int = None  # 默认没有限制，当设置后，一次只允许上传指定数量文件。
    multiple: bool = None  # False  # 是否多选。
    joinValues: bool = None  # True  # 拼接值
    extractValue: bool = None  # False  # 提取值
    delimiter: str = None  # ","  # 拼接符
    autoUpload: bool = None  # True  # 否选择完就自动开始上传
    hideUploadButton: bool = None  # False  # 隐藏上传按钮
    stateTextMap: dict = None  # {init: '', pending: '等待上传', uploading: '上传中', error: '上传出错', uploaded: '已上传',ready: ''}  # 上传状态文案
    fileField: str = None  # "file"  # 如果你不想自己存储，则可以忽略此属性。
    nameField: str = None  # "name"  # 接口返回哪个字段用来标识文件名
    valueField: str = None  # "value"  # 文件的值用那个字段来标识。
    urlField: str = None  # "url"  # 文件下载地址的字段名。
    btnLabel: str = None  # 上传按钮的文字
    downloadUrl: Union[
        str, bool] = None  # 1.1.6 版本开始支持 post:http://xxx.com/${value} 这种写法 # 默认显示文件路径的时候会支持直接下载，可以支持加前缀如：http://xx.dom/filename= ，如果不希望这样，可以把当前配置项设置为 false。
    useChunk: bool = None  # amis 所在服务器，限制了文件上传大小不得超出 10M，所以 amis 在用户选择大文件的时候，自动会改成分块上传模式。
    chunkSize: int = None  # 5 * 1024 * 1024  # 分块大小
    startChunkApi: API = None  # startChunkApi
    chunkApi: API = None  # chunkApi
    finishChunkApi: API = None  # finishChunkApi


class InputImage(FormItem):
    """图片上传"""

    class CropInfo(BaseAmisModel):
        aspectRatio: float = None  # 裁剪比例。浮点型，默认 1 即 1:1，如果要设置 16:9 请设置 1.7777777777777777 即 16 / 9。。
        rotatable: bool = None  # False  # 裁剪时是否可旋转
        scalable: bool = None  # False  # 裁剪时是否可缩放
        viewMode: int = None  # 1  # 裁剪时的查看模式，0 是无限制

    class Limit(BaseAmisModel):
        width: int = None  # 限制图片宽度。
        height: int = None  # 限制图片高度。
        minWidth: int = None  # 限制图片最小宽度。
        minHeight: int = None  # 限制图片最小高度。
        maxWidth: int = None  # 限制图片最大宽度。
        maxHeight: int = None  # 限制图片最大高度。
        aspectRatio: float = None  # 限制图片宽高比，格式为浮点型数字，默认 1 即 1:1，如果要设置 16:9 请设置 1.7777777777777777 即 16 / 9。 如果不想限制比率，请设置空字符串。

    type: str = 'input-image'
    receiver: API = None  # 上传文件接口
    accept: str = None  # ".jpeg,.jpg,.png,.gif"  # 支持的图片类型格式，请配置此属性为图片后缀，例如.jpg,.png
    maxSize: int = None  # 默认没有限制，当设置后，文件大小大于此值将不允许上传。单位为B
    maxLength: int = None  # 默认没有限制，当设置后，一次只允许上传指定数量文件。
    multiple: bool = None  # False  # 是否多选。
    joinValues: bool = None  # True  # 拼接值
    extractValue: bool = None  # False  # 提取值
    delimeter: str = None  # ","  # 拼接符
    autoUpload: bool = None  # True  # 否选择完就自动开始上传
    hideUploadButton: bool = None  # False  # 隐藏上传按钮
    fileField: str = None  # "file"  # 如果你不想自己存储，则可以忽略此属性。
    crop: Union[bool, CropInfo] = None  # 用来设置是否支持裁剪。
    cropFormat: str = None  # "image/png"  # 裁剪文件格式
    cropQuality: int = None  # 1  # 裁剪文件格式的质量，用于 jpeg/webp，取值在 0 和 1 之间
    limit: Limit = None  # 限制图片大小，超出不让上传。
    frameImage: str = None  # 默认占位图地址
    fixedSize: bool = None  # 是否开启固定尺寸,若开启，需同时设置 fixedSizeClassName
    fixedSizeClassName: str = None  # 开启固定尺寸时，根据此值控制展示尺寸。例如h-30,即图片框高为 h-30,AMIS 将自动缩放比率设置默认图所占位置的宽度，最终上传图片根据此尺寸对应缩放。


class LocationPicker(FormItem):
    """地理位置"""
    type: str = 'location-picker'
    vendor: str = 'baidu'  # 地图厂商，目前只实现了百度地图
    ak: str = ''  # 百度地图的 ak  # 注册地址: http://lbsyun.baidu.com/
    clearable: bool = None  # False  # 输入框是否可清空
    placeholder: str = None  # "请选择位置"  # 默认提示
    coordinatesType: str = None  # "bd09"  # 默为百度坐标，可设置为'gcj02'


class InputNumber(FormItem):
    """数字输入框"""
    type: str = 'input-number'
    min: Union[int, Template] = None  # 最小值
    max: Union[int, Template] = None  # 最大值
    step: int = None  # 步长
    precision: int = None  # 精度，即小数点后几位
    showSteps: bool = True  # 是否显示上下点击按钮
    prefix: str = None  # 前缀
    suffix: str = None  # 后缀
    kilobitSeparator: bool = None  # 千分分隔


class Picker(FormItem):
    """列表选择器"""
    type: str = 'picker'  # 列表选取，在功能上和 Select 类似，但它能显示更复杂的信息。
    size: Union[str, SizeEnum] = None  # 支持: xs、sm、md、lg、xl、 full
    options: OptionsNode = None  # 选项组
    source: API = None  # 动态选项组
    multiple: bool = None  # 是否为多选。
    delimeter: bool = None  # False # 拼接符
    labelField: str = None  # "label" # 选项标签字段
    valueField: str = None  # "value" # 选项值字段
    joinValues: bool = None  # True # 拼接值
    extractValue: bool = None  # False # 提取值
    autoFill: dict = None  # 自动填充
    modalMode: Literal["dialog", "drawer"] = None  # "dialog" # 设置 dialog 或者 drawer，用来配置弹出方式。
    pickerSchema: Union[
        "CRUD", SchemaNode] = None  # "{mode: 'list', listItem: {title: '${label}'}}" # 即用 List 类型的渲染，来展示列表信息。更多配置参考 CRUD
    embed: bool = None  # False # 是否使用内嵌模式


class Switch(FormItem):
    """开关"""
    type: str = 'switch'
    option: str = None  # 选项说明
    onText: str = None  # 开启时的文本
    offText: str = None  # 关闭时的文本
    trueValue: Any = None  # "True"  # 标识真值
    falseValue: Any = None  # "false"  # 标识假值


class Static(FormItem):
    """静态展示/标签"""
    type: str = 'static'  # 支持通过配置type为static-xxx的形式，展示其他 非表单项 组件 static-json|static-datetime

    class Json(FormItem):
        type: str = 'static-json'
        value: Union[dict, str]

    class Datetime(FormItem):
        """显示日期"""
        type: str = 'static-datetime'
        value: Union[int, str]  # 支持10位时间戳: 1593327764


class InputText(FormItem):
    """输入框"""
    type: str = 'input-text'  # input-text | input-url | input-email | input-password | divider
    options: Union[List[str], List[dict]] = None  # 选项组
    source: Union[str, API] = None  # 动态选项组
    autoComplete: Union[str, API] = None  # 自动补全
    multiple: bool = None  # 是否多选
    delimeter: str = None  # 拼接符 ","
    labelField: str = None  # 选项标签字段 "label"
    valueField: str = None  # 选项值字段 "value"
    joinValues: bool = True  # 拼接值
    extractValue: bool = None  # 提取值
    addOn: SchemaNode = None  # 输入框附加组件，比如附带一个提示文字，或者附带一个提交按钮。
    trimContents: bool = None  # 是否去除首尾空白文本。
    creatable: bool = None  # 是否可以创建，默认为可以，除非设置为 false 即只能选择选项中的值
    clearable: bool = None  # 是否可清除
    resetValue: str = None  # 清除后设置此配置项给定的值。
    prefix: str = None  # 前缀
    suffix: str = None  # 后缀
    showCounter: bool = None  # 是否显示计数器
    minLength: int = None  # 限制最小字数
    maxLength: int = None  # 限制最大字数


class InputPassword(InputText):
    """密码输框"""
    type: str = 'input-password'


class InputRichText(FormItem):
    """富文本编辑器"""
    type: str = 'input-rich-text'
    saveAsUbb: bool = None  # 是否保存为 ubb 格式
    receiver: API = None  # ''  # 默认的图片保存 API
    videoReceiver: API = None  # ''  # 默认的视频保存 API
    size: str = None  # 框的大小，可设置为 md 或者 lg
    options: dict = None  # 需要参考 tinymce 或 froala 的文档
    buttons: List[str] = None  # froala 专用，配置显示的按钮，tinymce 可以通过前面的 options 设置 toolbar 字符串


class Select(FormItem):
    """下拉框"""
    type: str = 'select'
    options: OptionsNode = None  # 选项组
    source: API = None  # 动态选项组
    autoComplete: API = None  # 自动提示补全
    delimeter: Union[bool, str] = False  # 拼接符
    labelField: str = "label"  # 选项标签字段
    valueField: str = "value"  # 选项值字段
    joinValues: bool = True  # 拼接值
    extractValue: bool = False  # 提取值
    checkAll: bool = False  # 是否支持全选
    checkAllLabel: str = "全选"  # 全选的文字
    checkAllBySearch: bool = False  # 有检索时只全选检索命中的项
    defaultCheckAll: bool = False  # 默认是否全选
    creatable: bool = False  # 新增选项
    multiple: bool = False  # 多选
    searchable: bool = False  # 检索
    createBtnLabel: str = "新增选项"  # 新增选项
    addControls: List[FormItem] = None  # 自定义新增表单项
    addApi: API = None  # 配置新增选项接口
    editable: bool = False  # 编辑选项
    editControls: List[FormItem] = None  # 自定义编辑表单项
    editApi: API = None  # 配置编辑选项接口
    removable: bool = False  # 删除选项
    deleteApi: API = None  # 配置删除选项接口
    autoFill: dict = None  # 自动填充
    menuTpl: str = None  # 支持配置自定义菜单
    clearable: bool = None  # 单选模式下是否支持清空
    hideSelected: bool = False  # 隐藏已选选项
    mobileClassName: str = None  # 移动端浮层类名
    selectMode: str = None  # 可选：group、table、tree、chained、associated。分别为：列表形式、表格形式、树形选择形式、级联选择形式，关联选择形式（与级联选择的区别在于，级联是无限极，而关联只有一级，关联左边可以是个 tree）。
    searchResultMode: str = None  # 如果不设置将采用 selectMode 的值，可以单独配置，参考 selectMode，决定搜索结果的展示形式。
    columns: List[dict] = None  # 当展示形式为 table 可以用来配置展示哪些列，跟 table 中的 columns 配置相似，只是只有展示功能。
    leftOptions: List[dict] = None  # 当展示形式为 associated 时用来配置左边的选项集。
    leftMode: str = None  # 当展示形式为 associated 时用来配置左边的选择形式，支持 list 或者 tree。默认为 list。
    rightMode: str = None  # 当展示形式为 associated 时用来配置右边的选择形式，可选：list、table、tree、chained。


class Textarea(FormItem):
    """多行文本输入框"""
    type: str = 'textarea'
    minRows: int = None  # 最小行数
    maxRows: int = None  # 最大行数
    trimContents: bool = None  # 是否去除首尾空白文本
    readOnly: bool = None  # 是否只读
    showCounter: bool = True  # 是否显示计数器
    minLength: int = None  # 限制最小字数
    maxLength: int = None  # 限制最大字数


class InputMonth(FormItem):
    """月份"""
    type: str = 'input-month'
    value: str = None  # 默认值
    format: str = None  # "X"  # 月份选择器值格式，更多格式类型请参考 moment
    inputFormat: str = None  # "YYYY-MM"  # 月份选择器显示格式，即时间戳格式，更多格式类型请参考 moment
    placeholder: str = None  # "请选择月份"  # 占位文本
    clearable: bool = None  # True  # 是否可清除


class InputTime(FormItem):
    """时间"""
    type: str = 'input-time'
    value: str = None  # 默认值
    timeFormat: str = None  # "HH:mm"  # 时间选择器值格式，更多格式类型请参考 moment
    format: str = None  # "X"  # 时间选择器值格式，更多格式类型请参考 moment
    inputFormat: str = None  # "HH:mm"  # 时间选择器显示格式，即时间戳格式，更多格式类型请参考 moment
    placeholder: str = None  # "请选择时间"  # 占位文本
    clearable: bool = None  # True  # 是否可清除
    timeConstraints: dict = None  # True  # 请参考： react-datetime


class InputDatetime(FormItem):
    """日期"""
    type: str = 'input-datetime'
    value: str = None  # 默认值
    format: str = None  # "X"  # 日期时间选择器值格式，更多格式类型请参考 文档
    inputFormat: str = None  # "YYYY-MM-DD HH:mm:ss"  # 日期时间选择器显示格式，即时间戳格式，更多格式类型请参考 文档
    placeholder: str = None  # "请选择日期以及时间"  # 占位文本
    shortcuts: str = None  # 日期时间快捷键
    minDate: str = None  # 限制最小日期时间
    maxDate: str = None  # 限制最大日期时间
    utc: bool = None  # False  # 保存 utc 值
    clearable: bool = None  # True  # 是否可清除
    embed: bool = None  # False  # 是否内联
    timeConstraints: dict = None  # True  # 请参考： react-datetime


class InputDate(FormItem):
    """日期"""
    type: str = 'input-date'
    value: str = None  # 默认值
    format: str = None  # "X"  # 日期选择器值格式，更多格式类型请参考 文档
    inputFormat: str = None  # "YYYY-DD-MM"  # 日期选择器显示格式，即时间戳格式，更多格式类型请参考 文档
    placeholder: str = None  # "请选择日期"  # 占位文本
    shortcuts: str = None  # 日期快捷键
    minDate: str = None  # 限制最小日期
    maxDate: str = None  # 限制最大日期
    utc: bool = None  # False  # 保存 utc 值
    clearable: bool = None  # True  # 是否可清除
    embed: bool = None  # False  # 是否内联模式
    timeConstraints: dict = None  # True  # 请参考： react-datetime
    closeOnSelect: bool = None  # False  # 点选日期后，是否马上关闭选择框
    schedules: Union[list, str] = None  # 日历中展示日程，可设置静态数据或从上下文中取数据，className参考背景色
    scheduleClassNames: List[
        str] = None  # "['bg-warning', 'bg-danger', 'bg-success', 'bg-info', 'bg-secondary']"  # 日历中展示日程的颜色，参考背景色
    scheduleAction: SchemaNode = None  # 自定义日程展示
    largeMode: bool = None  # False  # 放大模式


class InputTimeRange(FormItem):
    """时间范围"""
    type: str = 'input-time-range'
    timeFormat: str = None  # "HH:mm"  # 时间范围选择器值格式
    format: str = None  # "HH:mm"  # 时间范围选择器值格式
    inputFormat: str = None  # "HH:mm"  # 时间范围选择器显示格式
    placeholder: str = None  # "请选择时间范围"  # 占位文本
    clearable: bool = None  # True  # 是否可清除
    embed: bool = None  # False  # 是否内联模式


class InputDatetimeRange(InputTimeRange):
    """日期时间范围"""
    type: str = 'input-datetime-range'
    ranges: Union[str, List[
        str]] = None  # "yesterday,7daysago,prevweek,thismonth,prevmonth,prevquarter"  # 日期范围快捷键，可选：today, yesterday, 1dayago, 7daysago, 30daysago, 90daysago, prevweek, thismonth, thisquarter, prevmonth, prevquarter
    minDate: str = None  # 限制最小日期时间，用法同 限制范围
    maxDate: str = None  # 限制最大日期时间，用法同 限制范围
    utc: bool = None  # False  # 保存 UTC 值


class InputDateRange(InputDatetimeRange):
    """日期范围"""
    type: str = 'input-date-range'
    minDuration: str = None  # 限制最小跨度，如： 2days
    maxDuration: str = None  # 限制最大跨度，如：1year


class InputMonthRange(InputDateRange):
    """月份范围"""
    type: str = 'input-month-range'


class Transfer(FormItem):
    """穿梭器"""
    type: Literal['transfer', 'transfer-picker', 'tabs-transfer', 'tabs-transfer-picker'] = 'transfer'
    options: OptionsNode = None  # 选项组
    source: API = None  # 动态选项组
    delimeter: str = None  # "False"  # 拼接符
    joinValues: bool = None  # True  # 拼接值
    extractValue: bool = None  # False  # 提取值
    searchable: bool = None  # False  # 当设置为 true 时表示可以通过输入部分内容检索出选项。
    searchApi: API = None  # 如果想通过接口检索，可以设置个 api。
    statistics: bool = None  # True  # 是否显示统计数据
    selectTitle: str = None  # "请选择"  # 左侧的标题文字
    resultTitle: str = None  # "当前选择"  # 右侧结果的标题文字
    sortable: bool = None  # False  # 结果可以进行拖拽排序
    selectMode: str = None  # "list"  # 可选：list、table、tree、chained、associated。分别为：列表形式、表格形式、树形选择形式、级联选择形式，关联选择形式（与级联选择的区别在于，级联是无限极，而关联只有一级，关联左边可以是个 tree）。
    searchResultMode: str = None  # 如果不设置将采用 selectMode 的值，可以单独配置，参考 selectMode，决定搜索结果的展示形式。
    columns: List[dict] = None  # 当展示形式为 table 可以用来配置展示哪些列，跟 table 中的 columns 配置相似，只是只有展示功能。
    leftOptions: List[dict] = None  # 当展示形式为 associated 时用来配置左边的选项集。
    leftMode: str = None  # 当展示形式为 associated 时用来配置左边的选择形式，支持 list 或者 tree。默认为 list。
    rightMode: str = None  # 当展示形式为 associated 时用来配置右边的选择形式，可选：list、table、tree、chained。
    menuTpl: SchemaNode = None  # 用来自定义选项展示
    valueTpl: SchemaNode = None  # 用来自定义值的展示


class TransferPicker(Transfer):
    """穿梭选择器"""
    type: str = 'transfer-picker'


class TabsTransfer(Transfer):
    """组合穿梭器"""
    type: str = 'tabs-transfer'


class TabsTransferPicker(Transfer):
    """组合穿梭选择器"""
    type: str = 'tabs-transfer-picker'


class InputTree(FormItem):
    """树形选择框"""
    type: str = 'input-tree'
    options: OptionsNode = None  # 选项组
    source: API = None  # 动态选项组
    autoComplete: API = None  # 自动提示补全
    multiple: bool = None  # False  # 是否多选
    delimeter: str = None  # "False"  # 拼接符
    labelField: str = None  # "label"  # 选项标签字段
    valueField: str = None  # "value"  # 选项值字段
    iconField: str = None  # "icon"  # 图标值字段
    joinValues: bool = None  # True  # 拼接值
    extractValue: bool = None  # False  # 提取值
    creatable: bool = None  # False  # 新增选项
    addControls: List[FormItem] = None  # 自定义新增表单项
    addApi: API = None  # 配置新增选项接口
    editable: bool = None  # False  # 编辑选项
    editControls: List[FormItem] = None  # 自定义编辑表单项
    editApi: API = None  # 配置编辑选项接口
    removable: bool = None  # False  # 删除选项
    deleteApi: API = None  # 配置删除选项接口
    searchable: bool = None  # False  # 是否可检索，仅在 type 为 tree-select 的时候生效
    hideRoot: bool = None  # True  # 如果想要显示个顶级节点，请设置为 false
    rootLabel: bool = None  # "顶级"  # 当 hideRoot 不为 false 时有用，用来设置顶级节点的文字。
    showIcon: bool = None  # True  # 是否显示图标
    showRadio: bool = None  # False  # 是否显示单选按钮，multiple 为 false 是有效。
    initiallyOpen: bool = None  # True  # 设置是否默认展开所有层级。
    unfoldedLevel: int = None  # 0  # 设置默认展开的级数，只有initiallyOpen不是true时生效。
    cascade: bool = None  # False  # 当选中父节点时不自动选择子节点。
    withChildren: bool = None  # False  # 选中父节点时，值里面将包含子节点的值，否则只会保留父节点的值。
    onlyChildren: bool = None  # False  # 多选时，选中父节点时，是否只将其子节点加入到值中。
    rootCreatable: bool = None  # False  # 是否可以创建顶级节点
    rootCreateTip: str = None  # "添加一级节点"  # 创建顶级节点的悬浮提示
    minLength: int = None  # 最少选中的节点数
    maxLength: int = None  # 最多选中的节点数
    treeContainerClassName: str = None  # tree 最外层容器类名
    enableNodePath: bool = None  # False  # 是否开启节点路径模式
    pathSeparator: str = None  # "/"  # 节点路径的分隔符，enableNodePath为true时生效


class TreeSelect(InputTree):
    """树形选择器"""
    type: str = 'tree-select'
    hideNodePathLabel: bool = None  # 是否隐藏选择框中已选择节点的路径 label 信息


class Image(AmisNode):
    """图片"""
    type: str = 'image'  # 如果在 Table、Card 和 List 中，为"image"；在 Form 中用作静态展示，为"static-image"
    className: str = None  # 外层 CSS 类名
    imageClassName: str = None  # 图片 CSS 类名
    thumbClassName: str = None  # 图片缩率图 CSS 类名
    height: int = None  # 图片缩率高度
    width: int = None  # 图片缩率宽度
    title: str = None  # 标题
    imageCaption: str = None  # 描述
    placeholder: str = None  # 占位文本
    defaultImage: str = None  # 无数据时显示的图片
    src: str = None  # 缩略图地址
    href: Template = None  # 外部链接地址
    originalSrc: str = None  # 原图地址
    enlargeAble: bool = None  # 支持放大预览
    enlargeTitle: str = None  # 放大预览的标题
    enlargeCaption: str = None  # 放大预览的描述
    thumbMode: str = None  # "contain"  # 预览图模式，可选：'w-full', 'h-full', 'contain', 'cover'
    thumbRatio: str = None  # "1:1"  # 预览图比例，可选：'1:1', '4:3', '16:9'
    imageMode: str = None  # "thumb"  # 图片展示模式，可选：'thumb', 'original' 即：缩略图模式 或者 原图模式


class Images(AmisNode):
    """图片集"""
    type: str = "images"  # 如果在 Table、Card 和 List 中，为"images"；在 Form 中用作静态展示，为"static-images"
    className: str = None  # 外层 CSS 类名
    defaultImage: str = None  # 默认展示图片
    value: Union[str, List[str], List[dict]] = None  # 图片数组
    source: str = None  # 数据源
    delimiter: str = None  # ","  # 分隔符，当 value 为字符串时，用该值进行分隔拆分
    src: str = None  # 预览图地址，支持数据映射获取对象中图片变量
    originalSrc: str = None  # 原图地址，支持数据映射获取对象中图片变量
    enlargeAble: bool = None  # 支持放大预览
    thumbMode: str = None  # "contain"  # 预览图模式，可选：'w-full', 'h-full', 'contain', 'cover'
    thumbRatio: str = None  # "1:1"  # 预览图比例，可选：'1:1', '4:3', '16:9'


class Carousel(AmisNode):
    """轮播图"""

    class Item(AmisNode):
        image: str = None  # 图片链接
        href: str = None  # 图片打开网址的链接
        imageClassName: str = None  # 图片类名
        title: str = None  # 图片标题
        titleClassName: str = None  # 图片标题类名
        description: str = None  # 图片描述
        descriptionClassName: str = None  # 图片描述类名
        html: str = None  # HTML 自定义，同Tpl一致

    type: str = "carousel"  # 指定为 Carousel 渲染器
    className: str = None  # "panel-default"  # 外层 Dom 的类名
    options: List[Item] = None  # "[]"  # 轮播面板数据
    itemSchema: dict = None  # 自定义schema来展示数据
    auto: bool = True  # 是否自动轮播
    interval: str = None  # "5s"  # 切换动画间隔
    duration: str = None  # "0.5s"  # 切换动画时长
    width: str = None  # "auto"  # 宽度
    height: str = None  # "200px"  # 高度
    controls: List[str] = None  # "['dots', 'arrows']"  # 显示左右箭头、底部圆点索引
    controlsTheme: str = None  # "light"  # 左右箭头、底部圆点索引颜色，默认light，另有dark模式
    animation: str = None  # "fade"  # 切换动画效果，默认fade，另有slide模式
    thumbMode: str = None  # "cover" | "contain"  # 图片默认缩放模式


##########################数据展示########################
class CRUD(AmisNode):
    """增删改查"""

    class Messages(AmisNode):
        fetchFailed: str = None  # 获取失败时提示
        saveOrderFailed: str = None  # 保存顺序失败提示
        saveOrderSuccess: str = None  # 保存顺序成功提示
        quickSaveFailed: str = None  # 快速保存失败提示
        quickSaveSuccess: str = None  # 快速保存成功提示

    type: str = "crud"  # type 指定为 CRUD 渲染器
    mode: str = None  # "table"  # "table" 、 "cards" 或者 "list"
    title: str = None  # ""  # 可设置成空，当设置成空时，没有标题栏
    className: str = None  # 表格外层 Dom 的类名
    api: API = None  # CRUD 用来获取列表数据的 api。
    loadDataOnce: bool = None  # 是否一次性加载所有数据（前端分页）
    loadDataOnceFetchOnFilter: bool = None  # True  # 在开启 loadDataOnce 时，filter 时是否去重新请求 api
    source: str = None  # 数据映射接口返回某字段的值，不设置会默认使用接口返回的${items}或者${rows}，也可以设置成上层数据源的内容
    filter: Union[SchemaNode, Form] = None  # 设置过滤器，当该表单提交后，会把数据带给当前 mode 刷新列表。
    filterTogglable: bool = None  # False  # 是否可显隐过滤器
    filterDefaultVisible: bool = None  # True  # 设置过滤器默认是否可见。
    initFetch: bool = None  # True  # 是否初始化的时候拉取数据, 只针对有 filter 的情况, 没有 filter 初始都会拉取数据
    interval: int = None  # 刷新时间(最低 1000)
    silentPolling: bool = None  # 配置刷新时是否隐藏加载动画
    stopAutoRefreshWhen: str = None  # 通过表达式来配置停止刷新的条件
    stopAutoRefreshWhenModalIsOpen: bool = None  # 当有弹框时关闭自动刷新，关闭弹框又恢复
    syncLocation: bool = None  # False  # 是否将过滤条件的参数同步到地址栏, !!!开启后可能改变数据类型,无法通过fastpi数据校验
    draggable: bool = None  # 是否可通过拖拽排序
    itemDraggableOn: bool = None  # 用表达式来配置是否可拖拽排序
    saveOrderApi: API = None  # 保存排序的 api。
    quickSaveApi: API = None  # 快速编辑后用来批量保存的 API。
    quickSaveItemApi: API = None  # 快速编辑配置成及时保存时使用的 API。
    bulkActions: List[Action] = None  # 批量操作列表，配置后，表格可进行选中操作。
    defaultChecked: bool = None  # 当可批量操作时，默认是否全部勾选。
    messages: Messages = None  # 覆盖消息提示，如果不指定，将采用 api 返回的 message
    primaryField: str = None  # 设置 ID 字段名。'id'
    perPage: int = None  # 设置一页显示多少条数据。10
    defaultParams: dict = None  # 设置默认 filter 默认参数，会在查询的时候一起发给后端
    pageField: str = None  # 设置分页页码字段名。 "page"
    perPageField: str = None  # "perPage"  # 设置分页一页显示的多少条数据的字段名。注意：最好与 defaultParams 一起使用，请看下面例子。
    perPageAvailable: List[int] = None  # [5, 10, 20, 50, 100]  # 设置一页显示多少条数据下拉框可选条数。
    orderField: str = None  # 设置用来确定位置的字段名，设置后新的顺序将被赋值到该字段中。
    hideQuickSaveBtn: bool = None  # 隐藏顶部快速保存提示
    autoJumpToTopOnPagerChange: bool = None  # 当切分页的时候，是否自动跳顶部。
    syncResponse2Query: bool = None  # True  # 将返回数据同步到过滤器上。
    keepItemSelectionOnPageChange: bool = None  # True  # 保留条目选择，默认分页、搜素后，用户选择条目会被清空，开启此选项后会保留用户选择，可以实现跨页面批量操作。
    labelTpl: str = None  # 单条描述模板，keepItemSelectionOnPageChange设置为true后会把所有已选择条目列出来，此选项可以用来定制条目展示文案。
    headerToolbar: list = None  # ['bulkActions', 'pagination']  # 顶部工具栏配置
    footerToolbar: list = None  # ['statistics', 'pagination']  # 底部工具栏配置
    alwaysShowPagination: bool = None  # 是否总是显示分页
    affixHeader: bool = None  # True  # 是否固定表头(table 下)
    autoGenerateFilter: bool = None  # 是否开启查询区域，开启后会根据列元素的 searchable 属性值，自动生成查询条件表单


class TableColumn(AmisNode):
    """列配置"""
    type: str = None  # Literal['text', 'audio','image', 'link', 'tpl', 'mapping','carousel','date', 'progress','status','switch','list','json','operation']
    label: Template = None  # 表头文本内容
    name: str = None  # 通过名称关联数据
    tpl: Template = None  # 模板
    fixed: str = None  # 是否固定当前列 left | right | none
    popOver: bool = None  # 弹出框
    quickEdit: bool = None  # 快速编辑
    copyable: Union[bool, dict] = None  # 是否可复制  boolean 或 {icon: string, content:string}
    sortable: bool = None  # False  # 是否可排序
    searchable: Union[bool, SchemaNode] = None  # False  # 是否可快速搜索  boolean | Schema
    width: Union[str, int] = None  # 列宽
    remark: Remark = None  # 提示信息
    breakpoint: str = None  # *,ls


class ColumnOperation(TableColumn):
    """操作列"""
    type: str = 'operation'
    label: Template = "操作"
    toggled: bool = True
    buttons: List[Union[Action, AmisNode]] = None


class ColumnImage(Image, TableColumn):
    """图片列"""
    pass


class ColumnImages(Images, TableColumn):
    """图片集列"""
    pass


class Table(AmisNode):
    """表格"""

    type: str = "table"  # 指定为 table 渲染器
    title: str = None  # 标题
    source: str = None  # "${items}"  # 数据源, 绑定当前环境变量
    affixHeader: bool = None  # True  # 是否固定表头
    columnsTogglable: Union[str, bool] = None  # "auto"  # 展示列显示开关, 自动即：列数量大于或等于 5 个时自动开启
    placeholder: str = None  # "暂无数据"  # 当没数据的时候的文字提示
    className: str = None  # "panel-default"  # 外层 CSS 类名
    tableClassName: str = None  # "table-db table-striped"  # 表格 CSS 类名
    headerClassName: str = None  # "Action.md-table-header"  # 顶部外层 CSS 类名
    footerClassName: str = None  # "Action.md-table-footer"  # 底部外层 CSS 类名
    toolbarClassName: str = None  # "Action.md-table-toolbar"  # 工具栏 CSS 类名
    columns: List[Union[TableColumn, SchemaNode]] = None  # 用来设置列信息
    combineNum: int = None  # 自动合并单元格
    itemActions: List[Action] = None  # 悬浮行操作按钮组
    itemCheckableOn: Expression = None  # 配置当前行是否可勾选的条件，要用 表达式
    itemDraggableOn: Expression = None  # 配置当前行是否可拖拽的条件，要用 表达式
    checkOnItemClick: bool = False  # 点击数据行是否可以勾选当前行
    rowClassName: str = None  # 给行添加 CSS 类名
    rowClassNameExpr: Template = None  # 通过模板给行添加 CSS 类名
    prefixRow: list = None  # 顶部总结行
    affixRow: list = None  # 底部总结行
    itemBadge: "Badge" = None  # 行角标配置
    autoFillHeight: bool = None  # 内容区域自适应高度
    footable: Union[
        bool, dict] = None  # 列太多时，内容没办法全部显示完，可以让部分信息在底部显示，可以让用户展开查看详情。配置很简单，只需要开启 footable 属性，同时将想在底部展示的列加个 breakpoint 属性为 * 即可。


class Chart(AmisNode):
    """图表: https://echarts.apache.org/zh/option.html#title"""
    type: str = "chart"  # 指定为 chart 渲染器
    className: str = None  # 外层 Dom 的类名
    body: SchemaNode = None  # 内容容器
    api: API = None  # 配置项接口地址
    source: dict = None  # 通过数据映射获取数据链中变量值作为配置
    initFetch: bool = None  # 组件初始化时，是否请求接口
    interval: int = None  # 刷新时间(最小 1000)
    config: Union[dict, str] = None  # 设置 eschars 的配置项,当为string的时候可以设置 function 等配置项
    style: dict = None  # 设置根元素的 style
    width: str = None  # 设置根元素的宽度
    height: str = None  # 设置根元素的高度
    replaceChartOption: bool = None  # False  # 每次更新是完全覆盖配置项还是追加？
    trackExpression: str = None  # 当这个表达式的值有变化时更新图表


class Code(AmisNode):
    """代码高亮"""
    type: str = "code"
    className: str = None  # 外层 CSS 类名
    value: str = None  # 显示的颜色值
    name: str = None  # 在其他组件中，时，用作变量映射
    language: str = None  # 所使用的高亮语言，默认是 plaintext
    tabSize: int = None  # 4  # 默认 tab 大小
    editorTheme: str = None  # "'vs'"  # 主题，还有 'vs-dark'
    wordWrap: str = None  # "True"  # 是否折行


class Json(AmisNode):
    """JSON 展示组件"""
    type: str = "json"  # 如果在 Table、Card 和 List 中，为"json"；在 Form 中用作静态展示，为"static-json"
    className: str = None  # 外层 CSS 类名
    value: Union[dict, str] = None  # json 值，如果是 string 会自动 parse
    source: str = None  # 通过数据映射获取数据链中的值
    placeholder: str = None  # 占位文本
    levelExpand: int = None  # 1  # 默认展开的层级
    jsonTheme: str = None  # "twilight"  # 主题，可选twilight和eighties
    mutable: bool = None  # False  # 是否可修改
    displayDataTypes: bool = None  # False  # 是否显示数据类型


class Link(AmisNode):
    """链接"""
    type: str = "link"  # 如果在 Table、Card 和 List 中，为"link"；在 Form 中用作静态展示，为"static-link"
    body: str = None  # 标签内文本
    href: str = None  # 链接地址
    blank: bool = None  # 是否在新标签页打开
    htmlTarget: str = None  # a 标签的 target，优先于 blank 属性
    title: str = None  # a 标签的 title
    disabled: bool = None  # 禁用超链接
    icon: str = None  # 超链接图标，以加强显示
    rightIcon: str = None  # 右侧图标


class Log(AmisNode):
    """实时日志"""
    type: str = "log"
    source: API = None  # 支持变量,可以初始设置为空，这样初始不会加载，而等这个变量有值的时候再加载
    height: int = None  # 500  # 展示区域高度
    className: str = None  # 外层 CSS 类名
    autoScroll: bool = None  # True  # 是否自动滚动
    placeholder: str = None  # 加载中的文字
    encoding: str = None  # "utf-8"  # 返回内容的字符编码


class Mapping(AmisNode):
    """映射"""
    type: str = "mapping"  # 如果在 Table、Card 和 List 中，为"mapping"；在 Form 中用作静态展示，为"static-mapping"
    className: str = None  # 外层 CSS 类名
    placeholder: str = None  # 占位文本
    map: dict = None  # 映射配置
    source: API = None  # API 或 数据映射


class Property(AmisNode):
    """属性表"""

    class Item(AmisNode):
        label: Template = None  # 属性名
        content: Template = None  # 属性值
        span: int = None  # 属性值跨几列
        visibleOn: Expression = None  # 显示表达式
        hiddenOn: Expression = None  # 隐藏表达式

    type: str = 'property'
    className: str = None  # 外层 dom 的类名
    style: dict = None  # 外层 dom 的样式
    labelStyle: dict = None  # 属性名的样式
    contentStyle: dict = None  # 属性值的样式
    column: int = None  # 3  # 每行几列
    mode: str = None  # 'table'  # 显示模式，目前只有 'table' 和 'simple'
    separator: str = None  # ','  # 'simple' 模式下属性名和值之间的分隔符
    source: Template = None  # 数据源
    title: str = None  # 标题
    items: List[Item] = None  # 数据项


class QRCode(AmisNode):
    """二维码"""
    type: str = "qr-code"  # 指定为 QRCode 渲染器
    value: Template  # 扫描二维码后显示的文本，如果要显示某个页面请输入完整 url（"http://..."或"https://..."开头），支持使用 模板
    className: str = None  # 外层 Dom 的类名
    qrcodeClassName: str = None  # 二维码 SVG 的类名
    codeSize: int = None  # 128  # 二维码的宽高大小
    backgroundColor: str = None  # "#fff"  # 二维码背景色
    foregroundColor: str = None  # "#000"  # 二维码前景色
    level: str = None  # "L"  # 二维码复杂级别，有（'L' 'M' 'Q' 'H'）四种


class Video(AmisNode):
    """视频"""
    type: str = "video"  # 指定为 video 渲染器
    className: str = None  # 外层 Dom 的类名
    src: str = None  # 视频地址
    isLive: bool = None  # False  # 是否为直播，视频为直播时需要添加上，支持flv和hls格式
    videoType: str = None  # 指定直播视频格式
    poster: str = None  # 视频封面地址
    muted: bool = None  # 是否静音
    autoPlay: bool = None  # 是否自动播放
    rates: List[float] = None  # 倍数，格式为[1.0, 1.5, 2.0]


##########################反馈########################
class Alert(AmisNode):
    """提示"""
    type: str = "alert"  # 指定为 alert 渲染器
    className: str = None  # 外层 Dom 的类名
    level: str = None  # "info"  # 级别，可以是：info、success、warning 或者 danger
    body: SchemaNode = None  # 显示内容
    showCloseButton: bool = None  # False  # 是否显示关闭按钮
    closeButtonClassName: str = None  # 关闭按钮的 CSS 类名
    showIcon: bool = None  # False  # 是否显示 icon
    icon: str = None  # 自定义 icon
    iconClassName: str = None  # icon 的 CSS 类名


class Dialog(AmisNode):
    """对话框"""
    type: str = "dialog"  # 指定为 Dialog 渲染器
    title: SchemaNode = None  # 弹出层标题
    body: SchemaNode = None  # 往 Dialog 内容区加内容
    size: Union[str, SizeEnum] = None  # 指定 dialog 大小，支持: xs、sm、md、lg、xl、full
    bodyClassName: str = None  # "modal-body"  # Dialog body 区域的样式类名
    closeOnEsc: bool = None  # False  # 是否支持按 Esc 关闭 Dialog
    showCloseButton: bool = None  # True  # 是否显示右上角的关闭按钮
    showErrorMsg: bool = None  # True  # 是否在弹框左下角显示报错信息
    disabled: bool = None  # False  # 如果设置此属性，则该 Dialog 只读没有提交操作。
    actions: List[Action] = None  # 如果想不显示底部按钮，可以配置：[]  "【确认】和【取消】"
    data: dict = None  # 支持数据映射，如果不设定将默认将触发按钮的上下文中继承数据。


class Drawer(AmisNode):
    """抽屉"""
    type: str = "drawer"  # "drawer" 指定为 Drawer 渲染器
    title: SchemaNode = None  # 弹出层标题
    body: SchemaNode = None  # 往 Drawer 内容区加内容
    size: Union[str, SizeEnum] = None  # 指定 Drawer 大小，支持: xs、sm、md、lg
    position: str = None  # 'left'  # 位置
    bodyClassName: str = None  # "modal-body"  # Drawer body 区域的样式类名
    closeOnEsc: bool = None  # False  # 是否支持按 Esc 关闭 Drawer
    closeOnOutside: bool = None  # False  # 点击内容区外是否关闭 Drawer
    overlay: bool = None  # True  # 是否显示蒙层
    resizable: bool = None  # False  # 是否可通过拖拽改变 Drawer 大小
    actions: List[Action] = None  # 可以不设置，默认只有两个按钮。 "【确认】和【取消】"
    data: dict = None  # 支持 数据映射，如果不设定将默认将触发按钮的上下文中继承数据。


class Iframe(AmisNode):
    """Iframe"""
    type: str = "iframe"  # 指定为 iFrame 渲染器
    className: str = None  # iFrame 的类名
    frameBorder: list = None  # frameBorder
    style: dict = None  # 样式对象
    src: str = None  # iframe 地址
    height: Union[int, str] = None  # iframe 高度
    width: Union[int, str] = None  # iframe 宽度


class Spinner(AmisNode):
    """加载中"""
    type: str = "spinner"


##########################常用组件########################

class TableCRUD(CRUD, Table):
    """表格CRUD"""


class Avatar(AmisNode):
    """头像"""
    type: str = "avatar"
    className: str = None  # 外层 dom 的类名
    fit: str = None  # "cover"  # 图片缩放类型
    src: str = None  # 图片地址
    text: str = None  # 文字
    icon: str = None  # 图标
    shape: str = None  # "circle"  # 形状，也可以是 square
    size: int = None  # 40  # 大小
    style: dict = None  # 外层 dom 的样式


class Audio(AmisNode):
    """音频"""
    type: str = "audio"  # 指定为 audio 渲染器
    className: str = None  # 外层 Dom 的类名
    inline: bool = None  # True  # 是否是内联模式
    src: str = None  # 音频地址
    loop: bool = None  # False  # 是否循环播放
    autoPlay: bool = None  # False  # 是否自动播放
    rates: List[float] = None  # "[]"  # 可配置音频播放倍速如：[1.0, 1.5, 2.0]
    controls: List[str] = None  # "['rates', 'play', 'time', 'process', 'volume']"  # 内部模块定制化


class Tasks(AmisNode):
    """任务操作集合"""

    class Item(AmisNode):
        label: str = None  # 任务名称
        key: str = None  # 任务键值，请唯一区分
        remark: str = None  # 当前任务状态，支持 html
        status: str = None  # 任务状态： 0: 初始状态，不可操作。1: 就绪，可操作状态。2: 进行中，还没有结束。3：有错误，不可重试。4: 已正常结束。5：有错误，且可以重试。

    type: str = "tasks"  # 指定为 Tasks 渲染器
    className: str = None  # 外层 Dom 的类名
    tableClassName: str = None  # table Dom 的类名
    items: List[Item] = None  # 任务列表
    checkApi: API = None  # 返回任务列表，返回的数据请参考 items。
    submitApi: API = None  # 提交任务使用的 API
    reSubmitApi: API = None  # 如果任务失败，且可以重试，提交的时候会使用此 API
    interval: int = None  # 3000  # 当有任务进行中，会每隔一段时间再次检测，而时间间隔就是通过此项配置，默认 3s。
    taskNameLabel: str = None  # "任务名称"  # 任务名称列说明
    operationLabel: str = None  # "操作"  # 操作列说明
    statusLabel: str = None  # "状态"  # 状态列说明
    remarkLabel: str = None  # "备注"  # 备注列说明
    btnText: str = None  # "上线"  # 操作按钮文字
    retryBtnText: str = None  # "重试"  # 重试操作按钮文字
    btnClassName: str = None  # "btn-sm btn-default"  # 配置容器按钮 className
    retryBtnClassName: str = None  # "btn-sm btn-danger"  # 配置容器重试按钮 className
    statusLabelMap: List[
        str] = None  # "["label-warning", "label-info", "label-success", "label-danger", "label-default", "label-danger"]" # 状态显示对应的类名配置
    statusTextMap: List[str] = None  # "["未开始", "就绪", "进行中", "出错", "已完成", "出错"]" # 状态显示对应的文字显示配置


class Wizard(AmisNode):
    """向导"""

    class Step(AmisNode):
        title: str = None  # 步骤标题
        mode: str = None  # 展示默认，跟 Form 中的模式一样，选择： normal、horizontal或者inline。
        horizontal: Horizontal = None  # 当为水平模式时，用来控制左右占比
        api: API = None  # 当前步骤保存接口，可以不配置。
        initApi: API = None  # 当前步骤数据初始化接口。
        initFetch: bool = None  # 当前步骤数据初始化接口是否初始拉取。
        initFetchOn: Expression = None  # 当前步骤数据初始化接口是否初始拉取，用表达式来决定。
        body: List[FormItem] = None  # 当前步骤的表单项集合，请参考 FormItem。

    type: str = "wizard"  # 指定为 Wizard 组件
    mode: str = None  # "horizontal"  # 展示模式，选择：horizontal 或者 vertical
    api: API = None  # 最后一步保存的接口。
    initApi: API = None  # 初始化数据接口
    initFetch: API = None  # 初始是否拉取数据。
    initFetchOn: Expression = None  # 初始是否拉取数据，通过表达式来配置
    actionPrevLabel: str = None  # "上一步"  # 上一步按钮文本
    actionNextLabel: str = None  # "下一步"  # 下一步按钮文本
    actionNextSaveLabel: str = None  # "保存并下一步"  # 保存并下一步按钮文本
    actionFinishLabel: str = None  # "完成"  # 完成按钮文本
    className: str = None  # 外层 CSS 类名
    actionClassName: str = None  # "btn-sm btn-default"  # 按钮 CSS 类名
    reload: str = None  # 操作完后刷新目标对象。请填写目标组件设置的 name 值，如果填写为 window 则让当前页面整体刷新。
    redirect: Template = None  # "3000"  # 操作完后跳转。
    target: str = None  # "False"  # 可以把数据提交给别的组件而不是自己保存。请填写目标组件设置的 name 值，如果填写为 window 则把数据同步到地址栏上，同时依赖这些数据的组件会自动重新刷新。
    steps: List[Step] = None  # 数组，配置步骤信息
    startStep: int = None  # "1"  # 起始默认值，从第几步开始。可支持模版，但是只有在组件创建时渲染模版并设置当前步数，在之后组件被刷新时，当前 step 不会根据 startStep 改变


PageSchema.update_forward_refs()
ActionType.Dialog.update_forward_refs()
ActionType.Drawer.update_forward_refs()
TableCRUD.update_forward_refs()
Form.update_forward_refs()
Tpl.update_forward_refs()
InputText.update_forward_refs()
InputNumber.update_forward_refs()
Picker.update_forward_refs()
