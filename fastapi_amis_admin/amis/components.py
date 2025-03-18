"""Detailed document reading address: https://baidu.gitee.io/amis/zh-CN/components"""
import os
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import Field
from typing_extensions import Literal

try:
    from pydantic import SerializeAsAny
except ImportError:
    from typing import Union as SerializeAsAny
from .constants import (
    BarcodeEnum,
    DisplayModeEnum,
    LevelEnum,
    PlacementEnum,
    ProgressEnum,
    SizeEnum,
    StepStatusEnum,
    TabsModeEnum,
    TriggerEnum,
)
from .types import (
    API,
    AmisNode,
    BaseAmisModel,
    Expression,
    OptionsNode,
    SchemaNode,
    Template,
    Tpl,
)
from .utils import amis_templates

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RemarkT = Union[str, "Remark"]


class Html(AmisNode):
    """Html"""

    type: str = "html"  # specify as html component
    html: str  # html When you need to get variables in the data field, use Tpl.


class Icon(AmisNode):
    """icon"""

    type: str = "icon"  # specify the component type
    className: Optional[str] = None  # Outer CSS class name
    icon: Optional[str] = None  # icon name, support fontawesome v4 or use url
    vendor: Optional[str] = None  # icon vendor, icon supports fontawesome v4 by default, if you want to support fontawesome v5
    # and v6, please set vendor to an empty string.


class Remark(AmisNode):
    """mark"""

    type: str = "remark"  # remark
    className: Optional[str] = None  # Outer CSS class name
    content: Optional[str] = None  # prompt text
    placement: Optional[str] = None  # Popup position
    trigger: Optional[str] = None  # Trigger condition['hover','focus']
    icon: Optional[str] = None  # "fa fa-question-circle" # icon


class Badge(AmisNode):
    """Subscript"""

    mode: str = "dot"  # Corner type, can be dot/text/ribbon
    text: Union[int, str, None] = None  # Corner text, supports strings and numbers, invalid when mode='dot'
    size: Optional[int] = None  # Angular size
    level: Optional[str] = None  # The level of the corner label, which can be info/success/warning/danger, after setting the
    # background color of the corner label is different
    overflowCount: Optional[int] = None  # 99 # Set the capped number value
    position: Optional[str] = None  # "top-right" # Corner position, can be top-right/top-left/bottom-right/bottom-left
    offset: Optional[int] = None  # The position of the corner label, the priority is greater than the position, when the
    # offset is set, the position is positioned as the top-right reference number[top, left]
    className: Optional[str] = None  # The class name of the outer dom
    animation: Optional[bool] = None  # whether the corner icon displays animation
    style: Optional[dict] = None  # Custom style for corner labels
    visibleOn: Optional[Expression] = None  # Controls the display and hiding of corner labels


class Page(AmisNode):
    """page"""

    __default_template_path__: str = f"{BASE_DIR}/templates/page.html"

    type: str = "page"  # Specify as Page component
    title: SerializeAsAny[Optional[SchemaNode]] = None  # page title
    subTitle: SerializeAsAny[Optional[SchemaNode]] = None  # Page subtitle
    remark: Optional[RemarkT] = None  # A prompt icon will appear near the title, and the content will be prompted when the
    # mouse is placed on it.
    aside: SerializeAsAny[Optional[SchemaNode]] = None  # Add content to the sidebar area of the page
    asideResizor: Optional[bool] = None  # whether the width of the sidebar area of the page can be adjusted
    asideMinWidth: Optional[int] = None  # The minimum width of the sidebar area of the page
    asideMaxWidth: Optional[int] = None  # The maximum width of the sidebar area of the page
    toolbar: SerializeAsAny[Optional[SchemaNode]] = None  # Add content to the upper right corner of the page.
    # It should be noted that when there is a title, the area is in the upper right corner,
    # and when there is no title, the area is at the top
    body: SerializeAsAny[Optional[SchemaNode]] = None  # Add content to the content area of the page
    className: Optional[str] = None  # Outer dom class name
    cssVars: Optional[dict] = None  # Custom CSS variables, please refer to styles
    css: Optional[str] = None  # Custom CSS styles, please refer to used theme styles
    mobileCSS: Optional[str] = None  # Custom mobile CSS styles, please refer to used theme styles
    toolbarClassName: Optional[str] = None  # "v-middle wrapper text-right bg-light bb" # Toolbar dom class name
    bodyClassName: Optional[str] = None  # "wrapper" # Body dom class name
    asideClassName: Optional[str] = None  # "w page-aside-region bg-auto" # Aside dom class name
    headerClassName: Optional[str] = None  # "bg-light bb wrapper" # Header area dom class name
    initApi: Optional[API] = None  # The api that Page uses to get initial data. The returned data can be used at the entire
    # page level.
    initFetch: Optional[bool] = None  # True # whether to start pulling initApi
    initFetchOn: Optional[Expression] = None  # whether to start pulling initApi, configure by expression
    interval: Optional[int] = None  # refresh time (minimum 1000)
    silentPolling: Optional[bool] = None  # False # whether to show the loading animation when the configuration is refreshed
    stopAutoRefreshWhen: Optional[Expression] = None  # Configure the conditions for stopping refresh through expressions
    regions: Optional[List[str]] = None

    def amis_html(
        self,
        template_path: str = "",
        locale: str = "zh_CN",
        cdn: str = "https://unpkg.com",
        pkg: str = "amis@1.10.2",
        site_title: str = "Amis",
        site_icon: str = "",
        theme: str = "cxd",
    ):
        """Render html template"""
        template_path = template_path or self.__default_template_path__
        theme_css = f'<link href="{cdn}/{pkg}/sdk/{theme}.css" rel="stylesheet"/>' if theme != "cxd" else ""
        return amis_templates(template_path).safe_substitute(
            {
                "AmisSchemaJson": self.amis_json(),
                "locale": locale.replace("_", "-"),  # Fix #50
                "cdn": cdn,
                "pkg": pkg,
                "site_title": site_title,
                "site_icon": site_icon,
                "theme": theme,
                "theme_css": theme_css,
            }
        )


class Divider(AmisNode):
    """Dividing line"""

    type: str = "divider"  # "Divider"
    className: Optional[str] = None  # The class name of the outer Dom
    lineStyle: Optional[str] = None  # Split line style, supports dashed and solid


class Flex(AmisNode):
    """layout"""

    type: str = "flex"  # Specify as Flex renderer
    className: Optional[str] = None  # css class name
    justify: Optional[str] = None  # "start", "flex-start", "center", "end", "flex-end", "space-around", "space-between",
    # "space-evenly"
    alignItems: Optional[str] = None  # "stretch", "start", "flex-start", "flex-end", "end", "center", "baseline"
    style: Optional[dict] = None  # custom style
    items: SerializeAsAny[Optional[List[SchemaNode]]] = None  #


class Grid(AmisNode):
    """Horizontal layout"""

    class Column(AmisNode):
        """Column configuration"""

        xs: Optional[int] = None  # "auto" # Width ratio: 1 - 12
        ClassName: Optional[str] = None  # column class name
        sm: Optional[int] = None  # "auto" # Width ratio: 1 - 12
        md: Optional[int] = None  # "auto" # Width ratio: 1 - 12
        lg: Optional[int] = None  # "auto" # Width ratio: 1 - 12
        valign: Optional[str] = None  # 'top'|'middle'|'bottom'|'between = None # Vertical alignment of the current column content
        body: SerializeAsAny[Optional[List[SchemaNode]]] = None  #

    type: str = "grid"  # Specify as Grid renderer
    className: Optional[str] = None  # The class name of the outer Dom
    gap: Optional[str] = None  # 'xs'|'sm'|'base'|'none'|'md'|'lg = None # Horizontal gap
    valign: Optional[str] = None  # 'top'|'middle'|'bottom'|'between = None # Vertical alignment
    align: Optional[str] = None  # 'left'|'right'|'between'|'center = None # Horizontal alignment
    columns: SerializeAsAny[Optional[List[SchemaNode]]] = None  #


class Panel(AmisNode):
    """panel"""

    type: str = "panel"  # Specify as the Panel renderer
    className: Optional[str] = None  # "panel-default" # The class name of the outer Dom
    headerClassName: Optional[str] = None  # "panel-heading" # The class name of the header area
    footerClassName: Optional[str] = None  # "panel-footer bg-light lter wrapper" # The class name of the footer area
    actionsClassName: Optional[str] = None  # "panel-footer" # The class name of the actions area
    bodyClassName: Optional[str] = None  # "panel-body" # The class name of the body area
    title: SerializeAsAny[Optional[SchemaNode]] = None  # title
    header: SerializeAsAny[Optional[SchemaNode]] = None  # header container
    body: SerializeAsAny[Optional[SchemaNode]] = None  # Content container
    footer: SerializeAsAny[Optional[SchemaNode]] = None  # bottom container
    affixFooter: Optional[bool] = None  # whether to fix the bottom container
    actions: SerializeAsAny[Optional[List["Action"]]] = None  # Button area


class Tabs(AmisNode):
    """Tab"""

    class Item(AmisNode):
        title: Optional[Optional[str]] = None  # Tab title
        icon: Union[str, Icon, None] = None  # Icon for Tab
        tab: SerializeAsAny[Optional[SchemaNode]] = None  # Content area
        hash: Optional[str] = None  # After setting, it will correspond to the hash of the url
        reload: Optional[bool] = None  # After setting, the content will be re-rendered every time, which is useful for
        # re-pulling crud
        unmountOnExit: Optional[bool] = None  # Each exit will destroy the current tab bar content
        className: Optional[str] = None  # "bg-white bl br bb wrapper-md" # Tab area style
        iconPosition: Optional[str] = None  # "left" # Tab's icon position left / right
        closable: Optional[bool] = None  # False # whether to support deletion, the priority is higher than the closable of the
        # component
        disabled: Optional[bool] = None  # False # whether to disable

    type: str = "tabs"  # Specify as Tabs renderer
    className: Optional[str] = None  # The class name of the outer Dom
    mode: Optional[str] = None  # Display mode, the value can be line, card, radio, vertical, chrome, simple, strong, tiled,
    # sidebar
    tabsClassName: Optional[str] = None  # Class name of Tabs Dom
    tabs: SerializeAsAny[Optional[List[Item]]] = None  # tabs content
    source: Optional[str] = None  # tabs associated data, tabs can be generated repeatedly after association
    toolbar: SerializeAsAny[Optional[SchemaNode]] = None  # toolbar in tabs
    toolbarClassName: Optional[str] = None  # The class name of the toolbar in the tabs
    mountOnEnter: Optional[bool] = None  # False # Render only when the tab is clicked
    unmountOnExit: Optional[bool] = None  # False # Destroyed when switching tabs
    scrollable: Optional[bool] = None  # False # whether the navigation supports content overflow scrolling, this property is
    # not supported in vertical and chrome modes; chrome mode defaults to compress tags (property discarded)
    tabsMode: Optional[TabsModeEnum] = None  # Display mode, the value can be line, card, radio, vertical, chrome, simple,
    # strong, tiled, sidebar
    addable: Optional[bool] = None  # False # whether to support adding
    addBtnText: Optional[str] = None  # "Add" # Add button text
    closable: Optional[bool] = None  # False # whether to support delete
    draggable: Optional[bool] = None  # False # whether to support draggable
    showTip: Optional[bool] = None  # False # whether to support tips
    showTipClassName: Optional[str] = None  # "'' " # Tip class
    editable: Optional[bool] = None  # False # whether to edit the tag name
    sidePosition: Optional[str] = None  # "left" # In sidebar mode, the position of the tab bar is left / right


class Portlet(Tabs):
    """Portal column"""

    class Item(Tabs.Item):
        toolbar: SerializeAsAny[Optional[SchemaNode]] = None  # The toolbar in tabs, which changes with tab switching

    type: str = "portlet"  # specify as portlet renderer
    contentClassName: Optional[str] = None  # Class name of Tabs content Dom
    tabs: SerializeAsAny[Optional[List[Item]]] = None  # tabs content
    style: Union[str, dict, None] = None  # custom style
    description: Optional[Template] = None  # Information on the right side of the title
    hideHeader: Optional[bool] = None  # False # hide the header
    divider: Optional[bool] = None  # False # remove divider


class Horizontal(AmisNode):
    left: Optional[int] = None  # The width ratio of the left label
    right: Optional[int] = None  # The width ratio of the right controller.
    offset: Optional[int] = None  # When the label is not set, the offset of the right controller


class Action(AmisNode):
    """Behavior button"""

    type: str = "button"  # Specify as the Page renderer. button action
    actionType: Optional[str] = None  # [Required] This is the core configuration of the action to specify the action type of
    # the action. Support: ajax, link, url, drawer, dialog, confirm, cancel, prev, next, copy, close.
    label: Optional[str] = None  # Button text. Available ${xxx} values.
    level: Optional[LevelEnum] = None  # Button style, support: link, primary, secondary, info, success, warning, danger,
    # light, dark, default.
    size: Optional[str] = None  # Button size, support: xs, sm, md, lg.
    icon: Optional[str] = None  # Set the icon, eg fa fa-plus.
    iconClassName: Optional[str] = None  # Add a class name to the icon.
    rightIcon: Optional[str] = None  # Set the icon to the right of the button text, eg fa fa-plus.
    rightIconClassName: Optional[str] = None  # Add a class name to the right icon.
    active: Optional[bool] = None  # whether the button is highlighted.
    activeLevel: Optional[str] = None  # The style when the button is highlighted, the configuration supports the same level.
    activeClassName: Optional[str] = None  # Add a class name to the button highlight. "is-active"
    block: Optional[bool] = None  # Use display:"block" to display the button.
    confirmText: Optional[Template] = None  # When set, the action will ask the user before starting. Available ${xxx} values.
    reload: Optional[str] = None  # Specify the name of the target component that needs to be refreshed after this operation (
    # the name value of the component, configured by yourself), please separate multiple ones with , signs.
    tooltip: Optional[str] = None  # This text pops up when the mouse stays, and the object type can also be configured: the
    # fields are title and content. Available ${xxx} values.
    disabledTip: Optional[str] = None  # The text will pop up when the mouse stays after it is disabled. You can also configure
    # the object type: the fields are title and content. Available ${xxx} values.
    tooltipPlacement: Optional[str] = None  # If tooltip or disabledTip is configured, specify the location of the prompt
    # information, and you can configure top, bottom, left, and right.
    close: Union[bool, str, None] = None  # When the action is configured in the actions of the dialog or drawer, configure
    # it to true to close the current dialog or drawer after the operation. When the value is a string and is the
    # name of the ancestor layer popup, the ancestor popup will be closed.
    required: Optional[List[str]] = None  # Configure an array of strings, specifying that the form items with the specified
    # field name must pass validation before performing operations in the form primary:bool=None
    onClick: Optional[str] = None  # The custom click event defines the click event through onClick in the form of a string,
    # which will be converted into a JavaScript function
    componentId: Optional[str] = None  # target component ID
    args: Union[dict, str, None] = None  # event parameters
    script: Optional[str] = None  # Customize JS script code, any action can be performed by calling doAction in the code,
    # and event action intervention can be realized through the event object event


class ActionType:
    """Behavior button type"""

    class Ajax(Action):
        actionType: str = "ajax"  # Show a popup after clicking
        api: Optional[API] = None  # Request address, refer to api format description.
        redirect: Optional[Template] = None  # Specify the path to redirect to after the current request ends, which can be
        # valued by ${xxx}.
        feedback: SerializeAsAny[
            Optional["Dialog"]
        ] = None  # If it is of ajax type, when ajax returns to normal, a dialog can be popped up
        # for other interactions. The returned data can be used in this dialog. For the format, please refer to Dialog
        messages: Optional[dict] = None  # success: a message will be displayed after the ajax operation is successful. It can
        # be left unspecified. If it is not specified, the api return shall prevail. failed: Ajax operation failure
        # message.

    class Dialog(Action):
        actionType: str = "dialog"  # Show a popup when clicked
        dialog: SerializeAsAny[
            Union["Dialog", "Service", SchemaNode]
        ]  # Specify the content of the pop-up box, the format can refer to Dialog
        nextCondition: Optional[bool] = None  # Can be used to set the condition of the next data, the default is true.

    class Drawer(Action):
        actionType: str = "drawer"  # Show a sidebar when clicked
        drawer: SerializeAsAny[
            Union["Drawer", "Service", SchemaNode]
        ]  # Specify the content of the popup box, the format can refer to Drawer

    class Copy(Action):
        actionType: str = "copy"  # Copy a piece of content to the clipboard
        content: Template  # Specify the copied content. Available ${xxx} values.
        copyFormat: Optional[str] = None  # You can set the copy format through copyFormat, the default is text text/html

    class Url(Action):
        """Jump directly"""

        actionType: str = "url"  # Jump directly
        url: str  # When the button is clicked, the specified page will be opened. Available ${xxx} values.
        blank: Optional[bool] = None  # false If true will open in a new tab page.

    class Link(Action):
        """Single page jump"""

        actionType: str = "link"  # Single page jump
        link: str  # is used to specify the jump address. Unlike url, this is a single-page jump method, which will
        # not render the browser. Please specify the page in the amis platform. Available ${xxx} values.

    class Toast(Action):
        """Toast light"""

        class ToastItem(AmisNode):
            title: SerializeAsAny[Optional[SchemaNode]] = None  # Toast Item Title
            body: SerializeAsAny[Optional[SchemaNode]] = None  # Toast Item Content
            level: Optional[str] = None  # default 'info', Display icon, optional 'info', 'success', 'error', 'warning'
            position: Optional[str] = None  # default 'top-center', display position,
            # 'top-right', 'top-center', 'top-left', 'bottom-center', 'bottom-left', 'bottom-right', 'center'
            closeButton: Optional[bool] = None  # default False, whether to show the close button
            showIcon: Optional[bool] = None  # default True, whether to display the icon
            timeout: Optional[int] = None  # default 5000

        actionType: str = "toast"  # Single page jump
        items: SerializeAsAny[Optional[List[ToastItem]]] = None  # List of ToastItems
        position: Optional[str] = None  # display position,
        # available 'top-right', 'top-center', 'top-left', 'bottom-center', 'bottom-left', 'bottom-right', 'center'
        closeButton: Optional[bool] = None  # default False, whether to display the close button, not in mobile
        showIcon: Optional[bool] = None  # default = True, whether to display the icon
        timeout: Optional[int] = None  # default 5000


class PageSchema(AmisNode):
    """Page configuration"""

    label: Optional[str] = None  # Menu name.
    icon: str = "fa fa-flash"  # Menu icon, for example: 'fa fa-file'. For detailed icon reference:
    # http://www.fontawesome.com.cn/faicons/
    url: Optional[str] = None  # The page routing path, when the route hits the path, the current page is enabled. When the
    # path does not start with /, the parent path is concatenated. For example: the path of the parent is folder,
    # and pageA is configured at this time, then this page will be hit only when the page address is /folder/pageA.
    # When the path starts with / such as: /crud/list, the parent path will not be spliced. In addition, routes with
    # parameters such as /crud/view/:id are supported. This value can be obtained from the page through ${params.id}.
    schema_: SerializeAsAny[Union[Page, "Iframe"]] = Field(
        None, alias="schema"
    )  # The configuration of the page, please go to the
    # page page for specific configuration
    schemaApi: Optional[API] = None  # If you want to pull through the interface, please configure. The return path is
    # json>data. Only one of schema and schemaApi can be selected.
    link: Optional[str] = None  # If you want to configure an external link menu, you only need to configure link.
    redirect: Optional[str] = None  # Jump, when hitting the current page, jump to the target page.
    rewrite: Optional[str] = None  # Change to rendering pages of other paths, the page address will not be modified in this way.
    isDefaultPage: Union[bool, str, None] = None  # Useful when you need a custom 404 page, don't have multiple such pages,
    # because only the first one will be useful.
    visible: Union[
        bool, str, None
    ] = None  # Some pages may not want to appear in the menu, you can configure it to false, and the
    # route with parameters does not need to be configured, it is directly invisible.
    className: Optional[str] = None  # Menu class name.
    children: SerializeAsAny[Optional[List["PageSchema"]]] = None  # Submenu
    sort: Optional[int] = None  # Unofficial attribute. sort
    tabsMode: Optional[TabsModeEnum] = None  # Unofficial attribute. Display mode, the value can be line, card, radio, vertical,

    # chrome, simple, strong, tiled, sidebar, collapse

    def as_page_body(self, group_extra: Optional[Dict[str, Any]] = None, item_extra: Optional[Dict[str, Any]] = None):
        if self.children:
            exclude = {"type", "url", "schema_", "schemaApi", "link", "redirect", "rewrite", "isDefaultPage", "children"}
            if self.tabsMode is None:
                body = App(pages=[PageSchema(children=self.children)])
            elif self.tabsMode == TabsModeEnum.collapse:
                body = (
                    CollapseGroup.parse_obj(self.dict(exclude=exclude, exclude_defaults=True))
                    .update_from_kwargs(
                        body=[
                            CollapseGroup.CollapseItem.parse_obj(item.dict(exclude=exclude, exclude_defaults=True))
                            .update_from_kwargs(
                                header=item.label,
                                body=item.as_page_body(group_extra, item_extra),
                            )
                            .update_from_dict(item_extra or {})
                            for item in self.children
                        ],
                    )
                    .update_from_dict(group_extra or {})
                )
            else:
                body = (
                    Tabs.parse_obj(self.dict(exclude=exclude, exclude_defaults=True))
                    .update_from_kwargs(
                        mountOnEnter=True,
                        tabs=[
                            Tabs.Item.parse_obj(item.dict(exclude=exclude, exclude_defaults=True))
                            .update_from_kwargs(
                                title=item.label,
                                tab=item.as_page_body(group_extra, item_extra),
                            )
                            .update_from_dict(item_extra or {})
                            for item in self.children
                        ],
                    )
                    .update_from_dict(group_extra or {})
                )
        elif self.schema_:
            body = self.schema_
            if isinstance(body, Iframe):
                body.height = body.height or 1080
        elif self.schemaApi:
            body = Service(schemaApi=self.schemaApi)
        elif self.link:
            body = Page(body=Link(href=self.link, body=self.label, blank=True))
        else:
            body = None
        return body


class App(Page):
    """Multi-page application"""

    __default_template_path__: str = f"{BASE_DIR}/templates/app.html"
    type: str = "app"
    api: Optional[API] = None  # The page configuration interface, if you want to pull the page configuration remotely,
    # please configure it. Return to the configuration path json>data>pages, please refer to the pages property for
    # the specific format.
    brandName: Optional[Template] = None  # app name
    logo: Optional[str] = None  # Support image address, or svg.
    className: Optional[str] = None  # css class name
    header: SerializeAsAny[Optional[Template]] = None  # header
    asideBefore: SerializeAsAny[Optional[Template]] = None  # The front area on the page menu.
    asideAfter: SerializeAsAny[Optional[Template]] = None  # The front area under the page menu.
    footer: SerializeAsAny[Optional[Template]] = None  # The page.
    pages: SerializeAsAny[
        Optional[List[Union[PageSchema, dict]]]
    ] = None  # Array<page configuration> specific page configuration.
    # Usually in an array, the first layer of the array is a group, generally you only need to configure the label set,
    # if you don't want to group, don't configure it directly, the real page should be configured in the second
    # layer, that is, in the children of the first layer.


class ButtonGroup(AmisNode):
    """Button group"""

    type: str = "button-group"
    buttons: SerializeAsAny[List[Action]]  # Behavior button group
    className: Optional[str] = None  # The class name of the outer Dom
    vertical: Optional[bool] = None  # whether to use vertical mode
    tiled: Optional[bool] = None  # whether to use tile mode
    btnLevel: Optional[LevelEnum] = None  # button style
    btnActiveLevel: Optional[LevelEnum] = None  # Active button style


class Custom(AmisNode):
    """Custom Components"""

    type: str = "custom"
    id: Optional[str] = None  # node id
    name: Optional[str] = None  # node name
    className: Optional[str] = None  # node class
    inline: bool = False  # use div tag by default, if true use span tag
    html: Optional[str] = None  # initialize node html
    onMount: Optional[str] = None  # "Function" # Function called after node initialization
    onUpdate: Optional[str] = None  # "Function" # The function called when the data is updated
    onUnmount: Optional[str] = None  # "Function" # The function called when the node is destroyed


class Service(AmisNode):
    """Functional container"""

    type: str = "service"  # designate as service renderer
    name: Optional[str] = None  # node name
    data: Optional[dict] = None  #
    className: Optional[str] = None  # The class name of the outer Dom
    body: SerializeAsAny[Optional[SchemaNode]] = None  # Content container
    api: Optional[API] = None  # Initialize data domain interface address
    ws: Optional[str] = None  # WebScocket address
    dataProvider: Optional[str] = None  # Data acquisition function
    initFetch: Optional[bool] = None  # whether to pull by default
    schemaApi: Optional[API] = None  # Used to get the remote schema interface address
    initFetchSchema: Optional[bool] = None  # whether to pull Schema by default
    messages: Optional[dict] = None  # Message prompt override, the default message reads the toast prompt text returned by the
    # interface, but it can be overridden here.
    # messages.fetchSuccess: Optional[str] = None # Toast prompt text when the interface request is successful
    # messages.fetchFailed: str = "Initialization failed" # Toast prompt text when interface request fails
    interval: Optional[int] = None  # Polling interval (minimum 3000)
    silentPolling: Optional[bool] = None  # False # whether to display the loading animation during polling
    stopAutoRefreshWhen: Optional[Expression] = None  # Configure the condition to stop polling


class Nav(AmisNode):
    """navigation"""

    class Link(AmisNode):
        label: Optional[str] = None  # name
        to: Optional[Template] = None  # Link address
        target: Optional[str] = None  # "Link relationship" #
        icon: Optional[str] = None  # icon
        children: SerializeAsAny[Optional[List["Link"]]] = None  # child links
        unfolded: Optional[bool] = None  # whether to unfold initially
        active: Optional[bool] = None  # whether to highlight
        activeOn: Optional[Expression] = None  # whether to highlight the condition, leaving it blank will automatically
        # analyze the link address
        defer: Optional[bool] = None  # mark whether it is a lazy add-in
        deferApi: Optional[API] = None  # Can not be configured, if the configuration priority is higher

    type: str = "nav"  # specify as Nav renderer
    className: Optional[str] = None  # The class name of the outer Dom
    stacked: bool = True  # Set to false to display in the form of tabs
    source: Optional[API] = None  # Navigation can be created dynamically via variable or API interface
    deferApi: Optional[API] = None  # The interface used to delay loading option details. It can be left unconfigured,
    # and the public source interface cannot be configured.
    itemActions: SerializeAsAny[Optional[SchemaNode]] = None  # More operations related configuration
    draggable: Optional[bool] = None  # whether to support drag and drop sorting
    dragOnSameLevel: Optional[bool] = None  # Only allow dragging within the same level
    saveOrderApi: Optional[API] = None  # save order api
    itemBadge: Optional[Badge] = None  # Badge
    links: Optional[list] = None  # link collection


class AnchorNav(AmisNode):
    """Anchor Navigation"""

    class Link(AmisNode):
        label: Optional[str] = None  # name
        title: Optional[Optional[str]] = None  # area title
        href: Optional[str] = None  # Region ID
        body: SerializeAsAny[Optional[SchemaNode]] = None  # area content area
        className: Optional[str] = None  # "bg-white bl br bb wrapper-md" # Area member style

    type: str = "anchor-nav"  # Specify as AnchorNav renderer
    className: Optional[str] = None  # The class name of the outer Dom
    linkClassName: Optional[str] = None  # Class name of the navigation Dom
    sectionClassName: Optional[str] = None  # The class name of the anchor area Dom
    links: Optional[list] = None  # links content
    direction: Optional[str] = None  # "vertical" # You can configure whether the navigation is displayed horizontally or
    # vertically. The corresponding configuration items are: vertical, horizontal
    active: Optional[str] = None  # The area that needs to be located


class ButtonToolbar(AmisNode):
    """Button Toolbar"""

    type: str = "button-toolbar"
    buttons: SerializeAsAny[List[Action]]  # Behavior button group


class Validation(BaseAmisModel):
    isEmail: Optional[bool] = None  # Must be Email.
    isUrl: Optional[bool] = None  # Must be a Url.
    isNumeric: Optional[bool] = None  # Must be a number.
    isAlpha: Optional[bool] = None  # Must be an alpha.
    isAlphanumeric: Optional[bool] = None  # Must be a letter or a number.
    isInt: Optional[bool] = None  # Must be an integer.
    isFloat: Optional[bool] = None  # Must be a float.
    isLength: Optional[int] = None  # whether the length is exactly equal to the set value.
    minLength: Optional[int] = None  # Minimum length.
    maxLength: Optional[int] = None  # Maximum length.
    maximum: Optional[int] = None  # Maximum value.
    minimum: Optional[int] = None  # Minimum value.
    equals: Optional[str] = None  # The current value must be exactly equal to xxx.
    equalsField: Optional[str] = None  # The current value must be the same as the xxx variable value.
    isJson: Optional[bool] = None  # Is it a valid Json string.
    isUrlPath: Optional[bool] = None  # is the url path.
    isPhoneNumber: Optional[bool] = None  # Is it a legal phone number
    isTelNumber: Optional[bool] = None  # Is it a valid phone number
    isZipcode: Optional[bool] = None  # whether it is a zip code
    isId: Optional[bool] = None  # whether it is an ID number, no verification is done
    matchRegexp: Optional[str] = None  # Must hit a certain regexp. /foo/


class FormItem(AmisNode):
    """Form item common"""

    class AutoFill(BaseAmisModel):
        showSuggestion: Optional[bool] = None  # true refers to input, false automatically fills
        api: Optional[
            API
        ] = None  # Automatically populate the interface/filter the CRUD request configuration with reference to entry
        silent: Optional[bool] = None  # Whether to display a data format error message. The default value is true
        fillMappinng: SerializeAsAny[
            Optional[SchemaNode]
        ] = None  # Auto-fill/reference input data mapping configuration, key-value pair form,
        # value support variable acquisition and expression
        trigger: Optional[str] = None  # ShowSuggestion to true, the reference input support way of trigger,
        # currently supports change "value change" | focus "form focus"
        mode: Optional[str] = None  # When showSuggestion is true, refer to the popOver mode: dialog, drawer, popOver
        labelField: Optional[str] = None  # When showSuggestion is true, set the popup dialog,drawer,popOver picker's labelField
        position: Optional[str] = None  # If showSuggestion is true, set the popOver location as shown in the input mode Popover
        size: Optional[str] = None  # If showSuggestion is true, set the value as shown in dialog mode
        columns: SerializeAsAny[
            Optional[List["TableColumn"]]
        ] = None  # When showSuggestion is true, the data display column configuration
        filter: SerializeAsAny[Optional[SchemaNode]] = None  # When showSuggestion is true, data query filter condition

    type: str = "input-text"  # Specify the form item type
    className: Optional[str] = None  # The outermost class name of the form
    inputClassName: Optional[str] = None  # Form controller class name
    labelClassName: Optional[str] = None  # class name of label
    name: Optional[str] = None  # Field name, specifying the key when the form item is submitted
    label: Union[bool, Template, None] = None  # form item label template or false
    labelAlign: Optional[str] = None  # "right" # Form item label alignment, default right alignment, only effective when mode is
    labelRemark: Optional[RemarkT] = None  # Form item label description
    description: Optional[Template] = None  # Form item description
    placeholder: Optional[str] = None  # Form item description
    inline: Optional[bool] = None  # whether it is inline mode
    submitOnChange: Optional[bool] = None  # whether to submit the current form when the value of the form item changes.
    disabled: Optional[bool] = None  # whether the current form item is disabled
    disabledOn: Optional[Expression] = None  # The condition for whether the current form item is disabled
    visible: Optional[bool] = None  # whether the current form item is disabled or not
    visibleOn: Optional[Expression] = None  # The condition for whether the current form item is disabled
    required: Optional[bool] = None  # whether it is required.
    requiredOn: Optional[Expression] = None  # Use an expression to configure whether the current form item is required.
    validations: SerializeAsAny[
        Optional[Union[Validation, Expression]]
    ] = None  # Validation of the form item value format, multiple settings
    # are supported, and multiple rules are separated by commas.
    validateApi: Optional[API] = None  # Form validation interface
    copyable: Union[bool, dict, None] = None  # whether to copy boolean or {icon: string, content:string}
    autoFill: Optional[AutoFill] = None  # Data entry configuration, automatic filling or reference entry
    static: Optional[bool] = None  # 2.4.0 Whether the current form item is static display,
    staticOn: Optional[Expression] = None  # 2.4.0 The condition for whether the current form item is static display
    # the current support static display of the form item
    staticClassName: Optional[str] = None  # 2.4.0 The class name for static display
    staticLabelClassName: Optional[str] = None  # 2.4.0 The class name of the Label for static display
    staticInputClassName: Optional[str] = None  # 2.4.0 The class name of value when static display
    staticSchema: Union[str, list, None] = None  # SchemaNode


class ButtonGroupSelect(FormItem):
    """Button group select"""

    type: str = "button-group-select"
    vertical: Optional[bool] = None  # Default False, use vertical mode
    tiled: Optional[bool] = None  # Default False, use tile mode
    btnLevel: LevelEnum = LevelEnum.default  # button style
    btnActiveLevel: LevelEnum = LevelEnum.default  # Check button style
    options: Optional[OptionsNode] = None  # option group
    source: Optional[API] = None  # dynamic group
    multiple: Optional[bool] = None  # Default False, multiple choice
    labelField: Optional[str] = None  # Default "label"
    valueField: Optional[str] = None  # Default "value"
    joinValues: Optional[bool] = None  # Default True
    extractValue: Optional[bool] = None  # Default False
    autoFill: Optional[dict] = None  # autofill


class ListSelect(FormItem):
    """List select, allows images"""

    type: str = "list-select"
    options: Optional[OptionsNode] = None  # option group
    source: Optional[API] = None  # dynamic group
    multiple: Optional[bool] = None  # Default False, multiple choice
    labelField: Optional[str] = None  # Default "label"
    valueField: Optional[str] = None  # Default "value"
    joinValues: Optional[bool] = None  # Default True
    extractValue: Optional[bool] = None  # Default False
    autoFill: Optional[dict] = None  # autofill
    listClassName: Optional[
        str
    ] = None  # Supports configuring the css class name of the list div. for example:flex justify-between


class Form(AmisNode):
    """Form"""

    class Messages(AmisNode):
        fetchSuccess: Optional[str] = None  # Prompt when fetch is successful
        fetchFailed: Optional[str] = None  # Prompt when fetch fails
        saveSuccess: Optional[str] = None  # Prompt when saving is successful
        saveFailed: Optional[str] = None  # Prompt when saving fails

    type: str = "form"  # "form" specifies the Form renderer
    name: Optional[str] = None  # After setting a name, it is convenient for other components to communicate with it
    mode: Optional[DisplayModeEnum] = None  # Form display mode, can be: normal, horizontal or inline
    horizontal: Optional[Horizontal] = None  # Useful when mode is horizontal,
    # Used to control label {"left": "col-sm-2", "right": "col-sm-10", "offset": "col-sm-offset-2"}
    title: Optional[Optional[str]] = None  # Title of the Form
    submitText: Optional[Optional[str]] = None  # "Submit" # Default submit button name, if it is set to empty, the default
    # button can be removed.
    className: Optional[str] = None  # The class name of the outer Dom
    body: SerializeAsAny[Optional[List[Union[FormItem, SchemaNode]]]] = None  # Form item collection
    actions: SerializeAsAny[Optional[List["Action"]]] = None  # Form submit button, the member is Action
    actionsClassName: Optional[str] = None  # class name of actions
    messages: SerializeAsAny[
        Optional[Messages]
    ] = None  # The message prompts to be overridden. The default message reads the message returned
    # by the API, but it can be overridden here.
    wrapWithPanel: Optional[bool] = None  # whether to wrap the Form with panel, if set to false, actions will be invalid.
    panelClassName: Optional[str] = None  # The class name of the outer panel
    api: Optional[API] = None  # The api that Form uses to save data.
    initApi: Optional[API] = None  # The api that Form uses to get initial data.
    rules: Optional[list] = None  # Form combination validation rules Array<{rule:string;message:string}>
    interval: Optional[int] = None  # refresh time (minimum 3000)
    silentPolling: Optional[bool] = None  # False # whether to show the loading animation when the configuration is refreshed
    stopAutoRefreshWhen: Optional[str] = None  # Configure the condition for stopping refresh by expression
    initAsyncApi: Optional[API] = None  # The api that Form uses to obtain initial data, which is different from initApi,
    # will keep polling and request this interface until the returned finished attribute is true.
    initFetch: Optional[bool] = None  # After initApi or initAsyncApi is set, the request will be sent by default, and if it is
    # set to false, the interface will not be requested at the beginning
    initFetchOn: Optional[str] = None  # Use expression to configure
    initFinishedField: Optional[Optional[str]] = None  # After setting initAsyncApi, by default, the data.finished of the
    # returned data will be used to judge whether it is completed.
    # Can also be set to other xxx, it will be obtained from data.xxx
    initCheckInterval: Optional[int] = None  # After setting initAsyncApi, the default pull interval
    asyncApi: Optional[API] = None  # After setting this property, after the form is submitted and sent to save the interface,
    # it will continue to poll and request the interface, and it will not end until the returned finished property is
    # true.
    checkInterval: Optional[int] = None  # The time interval for polling requests, the default is 3 seconds. Setting asyncApi
    # is valid
    finishedField: Optional[Optional[str]] = None  # Set this property if the field name that decides to end is not finished,
    # such as is_success
    submitOnChange: Optional[bool] = None  # Form modification is submitted
    submitOnInit: Optional[bool] = None  # Submit once initially
    resetAfterSubmit: Optional[bool] = None  # whether to reset the form after submitting
    primaryField: Optional[str] = None  # Set the primary key id. When set, it will only carry this data when checking whether
    # the form is completed (asyncApi).
    target: Optional[str] = None  # The default form submission itself will save the data by sending the api, but you can also
    # set the name value of another form, or another CRUD model name value. If the target target is a Form,
    # the target Form will trigger initApi again, and the api can get the current form data. If the target is a CRUD
    # model, the target model will re-trigger the search with the current Form data as the parameter. When the target
    # is window, the data of the current form will be attached to the page address.
    redirect: Optional[str] = None  # After setting this attribute, after the Form is saved successfully, it will automatically
    # jump to the specified page. Support relative addresses, and absolute addresses (relative to the group).
    reload: Optional[str] = None  # Refresh the target object after the operation. Please fill in the name value set by the
    # target component. If it is filled in window, the current page will be refreshed as a whole.
    autoFocus: Optional[bool] = None  # whether to auto focus.
    canAccessSuperData: Optional[bool] = None  # Specify whether the upper layer data can be automatically obtained and mapped
    # to the form item
    persistData: Optional[str] = None  # Specify a unique key to configure whether to enable local caching for the current form
    clearPersistDataAfterSubmit: Optional[bool] = None  # Specify whether to clear the local cache after the form is submitted
    # successfully
    preventEnterSubmit: Optional[bool] = None  # Disable EnterSubmit form submission
    trimValues: Optional[bool] = None  # trim each value of the current form item
    promptPageLeave: Optional[bool] = None  # The form has not been saved, whether to confirm with a pop-up box before leaving
    # the page.
    columnCount: Optional[int] = None  # The form item is displayed as several columns
    debug: Optional[bool] = None
    inheritData: Optional[bool] = None  # true # The default form is to create its own data field in the form of a data link,
    # and only the data in this data field will be sent when the form is submitted. If you want to share the
    # upper layer data field, you can set this attribute to false, so that the data in the upper layer data field
    # does not need to be sent in the form with hidden fields or explicit mapping.
    static: Optional[bool] = None  # false # 2.4.0. The entire form is displayed statically.
    # For details, please refer to the:https://aisuda.bce.baidu.com/amis/examples/form/switchDisplay.
    staticClassName: Optional[str] = None  # 2.4.0. The name of the class used when the form is statically displayed
    labelAlign: Optional[Literal["right", "left"]] = None  # "right"  # 表单项标签对齐方式，默认右对齐，
    # 仅在 mode为horizontal 时生效
    labelWidth: Union[int, str, None] = None  # 表单项标签自定义宽度
    persistDataKeys: Optional[List[str]] = None  # 指指定只有哪些 key 缓存
    closeDialogOnSubmit: Optional[bool] = None  # 提交的时候是否关闭弹窗


class InputSubForm(FormItem):
    """Subform"""

    type: str = "input-sub-form"
    multiple: Optional[bool] = None  # False # whether it is multiple selection mode
    labelField: Optional[str] = None  # When this field exists in the value, the button name will be displayed using the value
    # of this field.
    btnLabel: Optional[str] = None  # "Settings" # Default button name
    minLength: Optional[int] = None  # 0 # Limit the minimum number.
    maxLength: Optional[int] = None  # 0 # Limit the maximum number.
    draggable: Optional[bool] = None  # whether it can be draggable and sorted
    addable: Optional[bool] = None  # whether it can be added
    removable: Optional[bool] = None  # whether it can be removed
    addButtonClassName: Optional[str] = None  # "``" # Add button CSS class name
    itemClassName: Optional[str] = None  # "``" # Value element CSS class name
    itemsClassName: Optional[str] = None  # "``" # Value wrapping element CSS class name
    form: Optional[Form] = None  # Subform configuration, same as Form
    addButtonText: Optional[str] = None  # "``" # Customize the text of the new item
    showErrorMsg: Optional[bool] = None  # True # whether to display the error message in the lower left corner


class Button(FormItem):
    """Button"""

    type: str = "button"
    className: Optional[str] = None  # Specify the add button class name
    url: Optional[str] = None  # Click the jump address, specify the behavior of this attribute button is consistent with the
    # a link
    size: Optional[str] = None  # Set button size 'xs'|'sm'|'md'|'lg'
    actionType: Optional[str] = None  # Set the button type 'button'|'reset'|'submit'| 'clear'| 'url'
    level: Optional[LevelEnum] = None  # Set button style 'link'|'primary'|'enhance'|'secondary'|'info'|'success'|'warning
    # '|'danger'|'light'| 'dark'|'default'
    tooltip: Union[str, dict, None] = None  # Bubble tip content TooltipObject
    tooltipPlacement: Optional[str] = None  # Balloon positioner 'top'|'right'|'bottom'|'left'
    tooltipTrigger: Optional[str] = None  # trigger tootip 'hover'|'focus'
    disabled: Optional[bool] = None  # button disabled state
    block: Optional[bool] = None  # Option to adjust button width to its parent width
    loading: Optional[bool] = None  # Show button loading effect
    loadingOn: Optional[str] = None  # Display button loading expression


class InputFormula(FormItem):
    """Input Formula Editor"""

    type: str = "input-formula"
    title: Optional[Optional[str]] = None  # title
    header: Optional[str] = None  # Editor header title, if not set, the form item labelfield is used by default
    evalMode: Optional[bool] = None  # default True, Expression mode or template mode (False),
    # template mode requires the expression to be written between ${and }.
    variables: Optional[List[dict]] = None  # Available variables, {label: string; value: string; children?: any[]; tag?: string}
    variableMode: Literal["tabs", "tree", "list"] = "list"  # Can be configured as tabs or tree ,
    # defaults to a list, which supports grouping.
    inputMode: Optional[Literal["button", "input-button", "input-group"]] = None  # Display mode of the control
    icon: Optional[str] = None  # fa icon
    btnLabel: Optional[str] = None  # The button text, which inputModetakesbutton
    level: LevelEnum = LevelEnum.default  # button stlye
    allowInput: Optional[bool] = None  # default -, Whether the input box can be entered
    btnSize: Optional[Literal["xs", "sm", "md", "lg"]] = None  # button size
    borderMode: Optional[Literal["full", "half", "none"]] = None  # Input box border mode
    placeholder: Optional[str] = None  # input box placeholder
    className: Optional[str] = None  # Control outer CSS style class name
    variableClassName: Optional[str] = None  # Variable panel CSS style class name
    functionClassName: Optional[str] = None  # Function panel CSS style class name
    mixedMode: Optional[bool] = None  # default False, if True it supports values in both text and formula formats


class InputArray(FormItem):
    """Array input box"""

    type: str = "input-array"
    items: SerializeAsAny[Optional[FormItem]] = None  # Configure single item form type
    addable: Optional[bool] = None  # whether it can be added.
    removable: Optional[bool] = None  # whether it can be removed
    draggable: Optional[bool] = None  # False # whether drag sorting is possible, it should be noted that when drag sorting is
    # enabled, there will be an additional $id field
    draggableTip: Optional[str] = None  # Draggable prompt text, the default is: "Order can be adjusted by dragging the [Swap]
    # button in each row"
    addButtonText: Optional[str] = None  # "Add" # Add button text
    minLength: Optional[int] = None  # Limit the minimum length
    maxLength: Optional[int] = None  # limit max length
    scaffold: Optional[Any] = None  # 新增成员时的默认值，一般根据items的数据类型指定需要的默认值


class Hidden(FormItem):
    """Hidden fields"""

    type: str = "hidden"


class Checkbox(FormItem):
    """Check box"""

    type: str = "checkbox"
    option: Optional[str] = None  # option description
    trueValue: Optional[Any] = None  # identifies the true value
    falseValue: Optional[Any] = None  # identifies a false value
    optionType: Optional[Literal["default", "button"]] = None  # 设置 option 类型


class Radios(FormItem):
    """Single box"""

    type: str = "radios"
    options: Optional[List[Union[dict, str]]] = None  # Option group
    source: Optional[API] = None  # Dynamic option group
    labelField: Optional[bool] = None  # "label" # option label field
    valueField: Optional[bool] = None  # "value" # option value field
    columnsCount: Optional[int] = None  # 1 # options are displayed in several columns, default is one column
    inline: Optional[bool] = None  # True # whether to display as one line
    selectFirst: Optional[bool] = None  # False # whether to select the first one by default
    autoFill: Optional[dict] = None  # autofill


class ChartRadios(Radios):
    """Single box"""

    type: str = "chart-radios"
    config: Optional[dict] = None  # echart chart configuration
    showTooltipOnHighlight: Optional[bool] = None  # False # whether to show tooltip when highlighted
    chartValueField: Optional[str] = None  # "value" # Chart value field name


class Checkboxes(FormItem):
    """Checkbox"""

    type: str = "checkboxes"
    options: Optional[OptionsNode] = None  # option group
    source: Optional[API] = None  # Dynamic option group
    delimiter: Optional[str] = None  # "," # splicer
    labelField: Optional[str] = None  # "label" # option label field
    valueField: Optional[str] = None  # "value" # option value field
    joinValues: Optional[bool] = None  # True # join values
    extractValue: Optional[bool] = None  # False # extract value
    columnsCount: Optional[int] = None  # 1 # options are displayed in several columns, default is one column
    checkAll: Optional[bool] = None  # False # whether to support select all
    inline: Optional[bool] = None  # True # whether to display as one line
    defaultCheckAll: Optional[bool] = None  # False # whether to check all by default
    creatable: Optional[bool] = None  # False # New option
    createBtnLabel: Optional[str] = None  # "Add option" # Add option
    addControls: SerializeAsAny[Optional[List[FormItem]]] = None  # Customize new form items
    addApi: Optional[API] = None  # Configure the new option interface
    editable: Optional[bool] = None  # False # edit options
    editControls: SerializeAsAny[Optional[List[FormItem]]] = None  # Customize edit form items
    editApi: Optional[API] = None  # Configure editing options interface
    removable: Optional[bool] = None  # False # remove option
    deleteApi: Optional[API] = None  # Configure delete option interface
    optionType: Optional[Literal["default", "button"]] = None  # "default"  # 按钮模式
    itemClassName: Optional[str] = None  # 选项样式类名
    labelClassName: Optional[str] = None  # 选项标签样式类名


class InputCity(FormItem):
    """City selector"""

    type: str = "input-city"
    allowCity: Optional[bool] = None  # True # Allow city selection
    allowDistrict: Optional[bool] = None  # True # Allow region selection
    searchable: Optional[bool] = None  # False # whether to display the search box
    extractValue: Optional[bool] = None  # True# whether to extract the value, if set to false, the value format will become an
    # object, including code, province, city and district text information.


class InputColor(FormItem):
    """Color picker"""

    type: str = "input-color"
    format: Optional[str] = None  # "hex" # Please choose hex, hls, rgb or rgba.
    presetColors: Optional[List[str]] = None  # "Selector preset color value" # The default color at the bottom of the selector,
    # if the array is empty, the default color will not be displayed
    allowCustomColor: Optional[bool] = None  # True # When false, only colors can be selected, use presetColors to set the
    # color selection range
    clearable: Optional[bool] = None  # "label" # whether to display the clear button
    resetValue: Optional[str] = None  # "" # After clearing, the form item value is adjusted to this value


class Combo(FormItem):
    """combination"""

    type: str = "combo"
    formClassName: Optional[str] = None  # The class name of a single group of form items
    addButtonClassName: Optional[str] = None  # Add button CSS class name
    items: SerializeAsAny[Optional[List[FormItem]]] = None  # Form items displayed in combination
    # items[x].columnClassName: Optional[str] = None # The class name of the column, which can be used to configure the column
    # width. The default is evenly distributed. items[x].unique: Optional[bool] = None # Set whether the current column value
    # is unique, that is, repeated selection is not allowed.
    noBorder: bool = False  # whether to display a border for a single group of form items
    scaffold: dict = {}  # initial value for a single set of form items
    multiple: bool = False  # whether to select multiple
    multiLine: bool = False  # The default is to display a row horizontally, after setting it will be displayed
    # vertically
    minLength: Optional[int] = None  # Minimum number of added bars
    maxLength: Optional[int] = None  # The maximum number of bars to add
    flat: bool = False  # whether to flatten the result (remove the name), only valid when the length of items is 1
    # and multiple is true.
    joinValues: bool = True  # The default is true When flattening is enabled, whether to send it to the backend in
    # the form of a delimiter, otherwise it is in the form of an array.
    delimiter: Optional[str] = None  # "False" # What delimiter to use when flattening is on and joinValues is true.
    addable: bool = False  # whether it can be added
    addButtonText: Optional[str] = None  # "Add" # Add button text
    removable: bool = False  # whether it can be removed
    deleteApi: Optional[API] = None  # If configured, an api will be sent before deletion, and the deletion will be completed
    # after the request is successful
    deleteConfirmText: Optional[str] = None  # "Confirm to delete?" # It only takes effect when deleteApi is configured! Used
    # for user confirmation when deleting
    draggable: bool = False  # whether drag sorting is possible, it should be noted that when drag sorting is
    # enabled, there will be an additional $id field
    draggableTip: Optional[str] = None  # "Order can be adjusted by dragging the [Exchange] button in each row" # Draggable
    # prompt text
    subFormMode: Optional[str] = None  # "normal" # optional normal, horizontal, inline
    placeholder: Optional[str] = None  # "``" # Displayed when there is no member.
    canAccessSuperData: bool = False  # Specify whether the upper layer data can be automatically obtained and mapped
    # to the form item
    conditions: Optional[dict] = None  # The form of an array contains the rendering types of all conditions. The test in a
    # single array is the judgment condition, and the items in the array are the schema rendered after meeting the
    # condition.
    typeSwitchable: bool = False  # whether to switch conditions, use with conditions
    strictMode: bool = True  # The default is strict mode. When set to false, when other form items are updated,
    # the form items in them can also be obtained in time, otherwise they will not.
    syncFields: List[str] = []  # Configure sync fields. Only valid when strictMode is false.
    # If the Combo level is deep, the data from the bottom layer may be out of sync. But configuring this property
    # for combo can be synchronized. Input format: ["os"]
    nullable: bool = False  # Allow null, if the validator is configured in the sub-form item, and it is a single
    # mode. You can allow the user to choose to clear (do not fill).
    subFormHorizontal: Optional[dict] = None  # The horizontal configuration of the sub-form item, which is the same as the
    # horizontal configuration of the form item.


class ConditionBuilder(FormItem):
    """Combined conditions"""

    class Field(AmisNode):
        type: str = "text"  # The field configuration is configured as "text"
        label: Optional[str] = None  # Field name.
        placeholder: Optional[str] = None  # placeholder
        operators: Optional[List[str]] = None  # If not so many, you can configure overrides.
        # Default is ['equal','not_equal','is_empty','is_not_empty','like','not_like','starts_with','ends_with']
        defaultOp: Optional[str] = None  # defaults to "equal"

    class Text(Field):
        """text"""

    class Number(Field):
        """number"""

        type: str = "number"
        minimum: Optional[float] = None  # minimum value
        maximum: Optional[float] = None  # maximum value
        step: Optional[float] = None  # step size

    class Date(Field):
        """date"""

        type: str = "date"
        defaultValue: Optional[str] = None  # default value
        format: Optional[str] = None  # Default "YYYY-MM-DD" value format
        inputFormat: Optional[str] = None  # Default "YYYY-MM-DD" display date format.

    class Datetime(Date):
        """Date Time"""

        type: str = "datetime"
        timeFormat: Optional[str] = None  # The default "HH:mm" time format determines which input boxes are available.

    class Time(Date):
        """time"""

        type: str = "time"

    class Select(Field):
        """Drop down to select"""

        type: str = "select"
        options: Optional[OptionsNode] = None  # options list, Array<{label: string, value: any}>
        source: Optional[API] = None  # Dynamic options, please configure api.
        searchable: Optional[bool] = None  # whether it can be searched
        autoComplete: Optional[API] = None  # Automatically prompt for completion, each time new content is entered,
        # the interface will be called, and the update options will be returned according to the interface.

    type: str = "condition-builder"
    fields: SerializeAsAny[
        Optional[List[Field]]
    ] = None  # It is an array type, each member represents an optional field, supports multiple
    # layers, configuration example
    className: Optional[str] = None  # Outer dom class name
    fieldClassName: Optional[str] = None  # The class name of the input field
    source: Optional[str] = None  # Pull configuration items remotely


class Editor(FormItem):
    """Code Editor"""

    type: str = "editor"
    language: Optional[str] = None  # "javascript" # The language highlighted by the editor, which can be obtained through the
    # ${xxx} variable
    # bat, c, coffeescript, cpp, csharp, css, dockerfile, fsharp, go, handlebars, html, ini, java,
    # javascript, json, less, lua, markdown, msdax, objective-c, php, plaintext, postiats, powershell,
    # pug, python, r, razor, ruby, sb, scss, shell, sol, sql, swift, typescript, vb, xml, yaml
    size: Optional[str] = None  # "md" # Editor height, the value can be md, lg, xl, xxl
    allowFullscreen: Optional[bool] = None  # False # whether to display the full screen mode switch
    options: Optional[dict] = None  # Other configurations of the monaco editor, such as whether to display line numbers, etc.,
    # please refer to here, but readOnly cannot be set, read-only mode needs to use disabled: true


class DiffEditor(FormItem):
    """Code Editor"""

    type: str = "diff-editor"
    language: Optional[str] = None  # "javascript" # The language highlighted by the editor, which can be obtained through the
    # ${xxx} variable
    # bat, c, coffeescript, cpp, csharp, css, dockerfile, fsharp, go, handlebars, html, ini, java,
    # javascript, json, less, lua, markdown, msdax, objective-c, php, plaintext, postiats, powershell,
    # pug, python, r, razor, ruby, sb, scss, shell, sol, sql, swift, typescript, vb, xml, yaml
    diffValue: Optional[Template] = None  # the diff value or reference to other data entry like '${value1}'


class Formula(AmisNode):
    """Formula for fields, linked by 'name'"""

    type: str = "formula"
    name: Optional[str] = None  # The formula result will be applied to the variable (name) specified here.
    formula: Optional[Expression] = None  # the formula itself
    condition: Optional[Expression] = None  # condition for the formula
    initSet: Optional[bool] = None  # Default True, whether to set at initialization
    autoSet: Optional[bool] = None  # Default True, Observe the formula result, if the calculation result changes,
    # it will be automatically applied to the variable
    id: Optional[bool] = None  # Default True, Define a name. When a button's target is specified, it will trigger a formula.


class DropDownButton(AmisNode):
    """Formula for fields, linked by 'name'"""

    type: str = "dropdown-button"
    label: Optional[str] = None  # button text
    className: Optional[str] = None  # Outer CSS class name
    btnClassName: Optional[str] = None  # Button CSS class name
    menuClassName: Optional[str] = None  # Dropdown menu CSS class name
    block: Optional[bool] = None  # Default False, block style
    size: Optional[Literal["xs", "sm", "md", "lg"]] = None  # size, support 'xs', 'sm', 'md','lg'
    align: Optional[Literal["left", "right"]] = None  # location align
    buttons: SerializeAsAny[List[Button]] = []  # List of buttons
    iconOnly: Optional[bool] = None  # default False, show only icon
    defaultIsOpened: Optional[bool] = None  # default False, whether to open by default
    closeOnOutside: Optional[bool] = None  # default True, Click whether to collapse the outer area
    closeOnClick: Optional[bool] = None  # default False, automatically close dropdown menu after button click
    trigger: TriggerEnum = TriggerEnum.click  # trigger method
    hideCaret: Optional[bool] = None  # default False, Hide drop down icon


class EachLoop(AmisNode):
    """Each loop renderer"""

    type: str = "each"
    value: list = []  # value for the loop
    name: Optional[str] = None  # Data field name
    source: Optional[str] = None  # Data mapping source
    items: Optional[dict] = None  # {"type": "tpl", "tpl": "< span ..."}
    placeholder: Optional[str] = None  # placeholder text when valuevalue does not exist or is an empty array


class GridNav(AmisNode):
    """Grid navigation
    menu navigation, does not support the configuration of the initialization interface to initialize the data field,
    so you need to work with similar to Service, Form or CRUD, with the configuration of the interface to initialize
    the data field components, or manually initialize the data field, and then through the source property,
    to obtain the data in the data chain to complete the menu display.
    """

    class OptionsItem(AmisNode):
        icon: Optional[str] = None  # default '', list item icon
        text: Optional[str] = None  # default '', list item text
        badge: Optional[Badge] = None  # Bade Schema, list item badge
        link: Optional[str] = None  # default '', Internal page path or external URL address, takes precedence over clickAction
        blank: Optional[bool] = None  # default False, Whether a new page is opened, valid when link is url
        clickAction: SerializeAsAny[Optional[Action]] = None  # ActionSchema

    type: str = "grid-nav"
    className: Optional[str] = None  # outer dom classname
    itemClassName: Optional[str] = None  # item custom css classname
    value: Optional[List] = None  # array of images
    source: Optional[str] = None  # data source
    square: Optional[bool] = None  # default False, whether to fix list items to be square
    center: Optional[bool] = None  # default False, whether to center the content of the list item
    border: Optional[bool] = None  # default False, whether to show the list item border
    gutter: Optional[int] = None  # default -, px, the spacing between list items
    reverse: Optional[bool] = None  # default False, whether to swap the position of the icon and text
    iconRatio: Optional[int] = None  # default 60, Icon width ratio, in %
    direction: Literal["horizontal", "vertical"] = "vertical"  # The direction in which the list items are arranged
    columnNum: Optional[int] = None  # default 4,
    options: SerializeAsAny[Optional[List[OptionsItem]]] = None  # the option items


class CollapseGroup(AmisNode):
    """Grid navigation
    menu navigation, does not support the configuration of the initialization interface to initialize the data field,
    so you need to work with similar to Service, Form or CRUD, with the configuration of the interface to initialize
    the data field components, or manually initialize the data field, and then through the source property,
    to obtain the data in the data chain to complete the menu display.
    """

    class CollapseItem(AmisNode):
        type: str = "collapse"
        disabled: Optional[bool] = None  # default False
        collapsed: Optional[bool] = None  # default True
        key: Union[int, str, None] = None  # default -, logo
        header: SerializeAsAny[Optional[SchemaNode]] = None  # default -, title
        body: SerializeAsAny[Optional[SchemaNode]] = None  # default -, content

    type: str = "collapse-group"
    activeKey: Union[str, int, List[Union[int, str, None]], None] = None  # Initialize the key to activate the panel
    disabled: Optional[bool] = None  # default False
    accordion: Optional[bool] = None  # default False, accordion mode
    expandIcon: SerializeAsAny[Optional[SchemaNode]] = None  # Custom toggle icon
    expandIconPosition: Literal["left", "right"] = "left"  # icon position
    body: SerializeAsAny[Optional[List[Union[CollapseItem, SchemaNode]]]] = None  # group content


class Markdown(AmisNode):
    """Markdown rendering"""

    type: str = "markdown"
    name: Optional[str] = None  # Field name, specifying the key when the form item is submitted
    value: Union[int, str, None] = None  # field value
    className: Optional[str] = None  # The outermost class name of the form
    src: Optional[API] = None  # external address
    options: Optional[dict] = None  # html, whether to support html tags, default false;
    # linkify, whether to automatically identify the link, the default value is true; breaks, whether the carriage
    # return is a newline, the default value is false


class OfficeViewer(AmisNode):
    """Office Viewer：https://aisuda.bce.baidu.com/amis/zh-CN/components/office-viewer"""

    type: str = "office-viewer"
    src: Optional[API] = None  # Document address
    loading: Optional[bool] = None  # Whether to display the loading icon
    enableVar: Optional[bool] = None  # Whether to enable variable replacement function
    wordOptions: Optional[dict] = None  # Word rendering configuration


class InputFile(FormItem):
    """File Upload"""

    type: str = "input-file"
    receiver: Optional[API] = None  # Upload file interface
    accept: Optional[str] = None  # "text/plain" # Only plain text is supported by default. To support other types,
    # please configure this property as the file suffix .xxx
    asBase64: Optional[bool] = None  # False # Assign the file to the current component in the form of base64
    asBlob: Optional[bool] = None  # False # Assign the file to the current component in binary form
    maxSize: Optional[int] = None  # There is no limit by default, when set, the file size larger than this value will not be
    # allowed to upload. unit is B
    maxLength: Optional[int] = None  # There is no limit by default. When set, only the specified number of files can be
    # uploaded at a time.
    multiple: Optional[bool] = None  # False # whether to select multiple.
    joinValues: Optional[bool] = None  # True # join values
    extractValue: Optional[bool] = None  # False # extract value
    delimiter: Optional[str] = None  # "," # splicer
    autoUpload: Optional[bool] = None  # True # No selection will automatically start uploading
    hideUploadButton: Optional[bool] = None  # False # hide the upload button
    stateTextMap: Optional[dict] = None  # Upload state text Default: {init: '', pending: 'Waiting to upload', uploading:
    # 'Uploading', error: 'Upload error', uploaded: 'Uploaded',ready: ''}
    fileField: Optional[str] = None  # "file" # You can ignore this attribute if you don't want to store it yourself.
    nameField: Optional[str] = None  # "name" # Which field is returned by the interface to identify the file name
    valueField: Optional[str] = None  # "value" # The value of the file is identified by that field.
    urlField: Optional[str] = None  # "url" # The field name of the file download address.
    btnLabel: Optional[str] = None  # The text of the upload button
    downloadUrl: Union[bool, str, None] = None  # Version 1.1.6 supports post:http://xxx.com/${value}
    # When the file path is displayed by default, it will support direct download. It can support adding a prefix
    # such as: http://xx.dom/filename= . If you don't want this, you can set the current configuration item to false.
    useChunk: Optional[bool] = None  # The server where amis is located limits the file upload size to no more than 10M,
    # so when amis selects a large file, it will automatically change to the chunked upload mode.
    chunkSize: Optional[int] = None  # 5 * 1024 * 1024 # chunk size
    startChunkApi: Optional[API] = None  # startChunkApi
    chunkApi: Optional[API] = None  # chunkApi
    finishChunkApi: Optional[API] = None  # finishChunkApi
    autoFill: Optional[Dict[str, str]] = None  # After the upload is successful, the value returned by the upload interface can
    # be filled into a form item by configuring autoFill (not supported under non-form)


class InputExcel(FormItem):
    """Parse Excel"""

    type: str = "input-excel"
    allSheets: Optional[bool] = None  # False # whether to parse all sheets
    parseMode: Optional[str] = None  # 'array' or 'object' parsing mode
    includeEmpty: Optional[bool] = None  # True # whether to include empty values
    plainText: Optional[bool] = None  # True # whether to parse as plain text


class InputTable(FormItem):
    """sheet"""

    type: str = "input-table"  # Specify as Table renderer
    showIndex: Optional[bool] = None  # False # Show index
    perPage: Optional[int] = None  # Set how many pieces of data are displayed on one page. 10
    addable: Optional[bool] = None  # False # whether to add a line
    editable: Optional[bool] = None  # False # whether editable
    removable: Optional[bool] = None  # False # whether it can be removed
    showAddBtn: Optional[bool] = None  # True # whether to show the add button
    addApi: Optional[API] = None  # API submitted when adding
    updateApi: Optional[API] = None  # API submitted when modified
    deleteApi: Optional[API] = None  # API submitted when deleting
    addBtnLabel: Union[bool, Template, None] = None  # Add button name
    addBtnIcon: Union[bool, str, None] = None  # "plus" # Add button icon
    copyBtnLabel: Union[bool, Template, None] = None  # Copy button text
    copyBtnIcon: Union[bool, str, None] = None  # "copy" # Copy button icon
    editBtnLabel: Union[bool, Template, None] = None  # "" # Edit button name
    editBtnIcon: Union[bool, str, None] = None  # "pencil" # edit button icon
    deleteBtnLabel: Union[bool, Template, None] = None  # "" # delete button name
    deleteBtnIcon: Union[bool, str, None] = None  # "minus" # delete button icon
    confirmBtnLabel: Union[bool, Template, None] = None  # "" # Confirm edit button name
    confirmBtnIcon: Optional[str] = None  # "check" # Confirm edit button icon
    cancelBtnLabel: Union[bool, Template, None] = None  # "" # Cancel edit button name
    cancelBtnIcon: Optional[str] = None  # "times" # Cancel edit button icon
    needConfirm: Optional[bool] = None  # True # whether to confirm the operation, it can be used to control the operation
    # interaction of the control table
    canAccessSuperData: Optional[bool] = None  # False # whether you can access the parent data, that is, the same level data
    # in the form, usually need to be used with strictMode
    strictMode: Optional[bool] = None  # True # For performance, the default value of other form items will not update the
    # current table. Sometimes, in order to obtain other form item fields synchronously, you need to enable this.
    columns: Optional[list] = None  # "[]" # Column information
    # columns[x].quickEdit: Optional[boolean|object] = None # Use with editable as true columns[x].quickEditOnUpdate:
    # boolean|object = None # Edit configuration that can be used to distinguish between new mode and update mode


class InputGroup(FormItem):
    """Combination of input boxes"""

    type: str = "input-group"
    className: Optional[str] = None  # CSS class name
    body: SerializeAsAny[Optional[List[Union[FormItem, AmisNode]]]] = None  # Form item collection


class Group(InputGroup):
    """Form item group"""

    type: str = "group"
    mode: Optional[DisplayModeEnum] = None  # Display the default, the same as the mode in Form
    gap: Optional[str] = None  # Gap between form items, optional: xs, sm, normal
    direction: Optional[str] = None  # "horizontal" # Can be configured to display horizontally or vertically. The
    # corresponding configuration items are: vertical, horizontal


class InputImage(FormItem):
    """upload picture"""

    class CropInfo(BaseAmisModel):
        aspectRatio: Optional[float] = None  # Crop ratio. Floating point, the default is 1, which is 1:1. If you want to set
        # 16:9, please set 1.7777777777777777, which is 16/9. .
        rotatable: Optional[bool] = None  # False # whether to rotate when cropping
        scalable: Optional[bool] = None  # False # whether it can be scaled when cropping
        viewMode: Optional[int] = None  # 1 # View mode when cropping, 0 is unlimited

    class Limit(BaseAmisModel):
        width: Optional[int] = None  # Limit image width.
        height: Optional[int] = None  # Limit image height.
        minWidth: Optional[int] = None  # Limit image minimum width.
        minHeight: Optional[int] = None  # Limit image minimum height.
        maxWidth: Optional[int] = None  # Limit the maximum width of the image.
        maxHeight: Optional[int] = None  # Limit the maximum height of the image.
        aspectRatio: Optional[float] = None  # Limit the aspect ratio of the image, the format is a floating-point number,
        # the default is 1, which is 1:1, If you want to set 16:9, please set 1.7777777777777777 which is 16/9. If
        # you don't want to limit the ratio, set an empty string.

    type: str = "input-image"
    receiver: Optional[API] = None  # Upload file interface
    accept: Optional[str] = None  # ".jpeg,.jpg,.png,.gif" # Supported picture types and formats, please configure this
    # property as picture suffix, such as .jpg,.png
    maxSize: Optional[int] = None  # There is no limit by default, when set, the file size larger than this value will not be
    # allowed to upload. unit is B
    maxLength: Optional[int] = None  # There is no limit by default. When set, only the specified number of files can be
    # uploaded at a time.
    multiple: Optional[bool] = None  # False # whether to select multiple.
    joinValues: Optional[bool] = None  # True # join values
    extractValue: Optional[bool] = None  # False # extract value
    delimiter: Optional[str] = None  # "," # splicer
    autoUpload: Optional[bool] = None  # True # No selection will automatically start uploading
    hideUploadButton: Optional[bool] = None  # False # hide the upload button
    fileField: Optional[str] = None  # "file" # You can ignore this attribute if you don't want to store it yourself.
    crop: Union[bool, CropInfo, None] = None  # Used to set whether to support cropping.
    cropFormat: Optional[str] = None  # "image/png" # crop file format
    cropQuality: Optional[int] = None  # 1 # The quality of the crop file format, for jpeg/webp, between 0 and 1
    limit: Optional[Limit] = None  # Limit the size of the image, beyond which it will not be allowed to upload.
    frameImage: Optional[str] = None  # Default placeholder image address
    fixedSize: Optional[bool] = None  # whether to enable fixed size, if enabled, set fixedSizeClassName at the same time
    fixedSizeClassName: Optional[
        str
    ] = None  # When the fixed size is turned on, the display size is controlled according to this value.
    # For example, h-30, that is, the height of the picture frame is h-30, AMIS will automatically set the zoom ratio
    # to the width of the position occupied by the default image, and the final uploaded image will be scaled
    # accordingly according to this size.
    autoFill: Optional[Dict[str, str]] = None  # After the upload is successful, the value returned by the upload interface can
    # be filled into a form item by configuring autoFill (not supported under non-form)
    initAutoFill: Optional[bool] = None  # False  # 表单反显时是否执行 autoFill
    uploadBtnText: SerializeAsAny[Optional[SchemaNode]] = None  # 上传按钮文案。支持tpl、schema形式配置。
    dropCrop: Optional[bool] = None  # True  # 图片上传后是否进入裁剪模式
    initCrop: Optional[bool] = None  # False  # 图片选择器初始化后是否立即进入裁剪模式


class LocationPicker(FormItem):
    """Location"""

    type: str = "location-picker"
    vendor: str = "baidu"  # Map vendor, currently only Baidu map is implemented
    ak: str = ...  # ak # registered address of Baidu map: http://lbsyun.baidu.com/
    clearable: Optional[bool] = None  # False # whether the input box can be cleared
    placeholder: Optional[str] = None  # "Please select a location" # Default prompt
    coordinatesType: Optional[str] = None  # "bd09" # Default is Baidu coordinates, can be set to 'gcj02'


class InputNumber(FormItem):
    """Number input box"""

    type: str = "input-number"
    min: Union[int, Template, None] = None  # minimum value
    max: Union[int, Template, None] = None  # maximum value
    step: Optional[int] = None  # step size
    precision: Optional[int] = None  # Precision, i.e. a few decimal places
    showSteps: Optional[bool] = None  # True # whether to show up and down click buttons
    prefix: Optional[str] = None  # prefix
    suffix: Optional[str] = None  # suffix
    kilobitSeparator: Optional[bool] = None  # Kilobit Separator


class Picker(FormItem):
    """List selector"""

    type: str = "picker"  # List pick, similar in function to Select, but it can display more complex information.
    size: Union[str, SizeEnum, None] = None  # Supports: xs, sm, md, lg, xl, full
    options: Optional[OptionsNode] = None  # option group
    source: Optional[API] = None  # Dynamic option group
    multiple: Optional[bool] = None  # whether it is multiple choice.
    delimiter: Optional[bool] = None  # False # splicer
    labelField: Optional[str] = None  # "label" # option label field
    valueField: Optional[str] = None  # "value" # option value field
    joinValues: Optional[bool] = None  # True # join values
    extractValue: Optional[bool] = None  # False # extract value
    autoFill: Optional[dict] = None  # autofill
    modalMode: Optional[Literal["dialog", "drawer"]] = None  # "dialog" # Set dialog or drawer to configure the popup mode.
    pickerSchema: SerializeAsAny[Optional[Union[SchemaNode, "CRUD"]]] = None  # "{mode: 'list', listItem: {title: '${label}'}}"
    # That is to use the rendering of the List type to display the list information. More configuration reference CRUD
    embed: Optional[bool] = None  # False # whether to use embedded mode


class Switch(FormItem):
    """switch"""

    type: str = "switch"
    option: Optional[str] = None  # option description
    onText: Optional[str] = None  # Text when it is turned on
    offText: Optional[str] = None  # text when off
    trueValue: Optional[Any] = None  # "True" # identifies the true value
    falseValue: Optional[Any] = None  # "false" # identifies a false value


class Static(FormItem):
    """Static display/label"""

    type: str = "static"  # Support to display other non-form item components static-json|static-datetime by

    # configuring type as static-xxx

    class Json(FormItem):
        type: str = "static-json"
        value: Union[dict, str]

    class Datetime(FormItem):
        """Display date"""

        type: str = "static-datetime"
        value: Union[int, str]  # support 10-bit timestamp: 1593327764


class InputText(FormItem):
    """Input box"""

    type: str = "input-text"  # input-text|input-url|input-email|input-password|divider
    options: Union[List[str], List[dict], None] = None  # Option group
    source: Optional[API] = None  # Dynamic option group
    autoComplete: Optional[API] = None  # autocomplete
    multiple: Optional[bool] = None  # whether to select multiple
    delimiter: Optional[str] = None  # Splice ","
    labelField: Optional[str] = None  # option label field "label"
    valueField: Optional[str] = None  # option value field "value"
    joinValues: Optional[bool] = None  # True # join values
    extractValue: Optional[bool] = None  # extract value
    addOn: SerializeAsAny[Optional[SchemaNode]] = None  # Input box add-ons, such as with a prompt text, or with a submit button.
    trimContents: Optional[bool] = None  # whether to remove leading and trailing blank text.
    creatable: Optional[bool] = None  # whether it can be created, the default is yes, unless it is set to false, only the
    # value in the option can be selected
    clearable: Optional[bool] = None  # whether it can be cleared
    resetValue: Optional[str] = None  # Set the value given by this configuration item after clearing.
    prefix: Optional[str] = None  # prefix
    suffix: Optional[str] = None  # suffix
    showCounter: Optional[bool] = None  # whether to show the counter
    minLength: Optional[int] = None  # Limit the minimum number of words
    maxLength: Optional[int] = None  # Limit the maximum number of characters


class InputPassword(InputText):
    """Password input box"""

    type: str = "input-password"


class InputRichText(FormItem):
    """Rich Text Editor"""

    type: str = "input-rich-text"
    saveAsUbb: Optional[bool] = None  # whether to save in ubb format
    receiver: Optional[API] = None  # '' # Default image save API
    videoReceiver: Optional[API] = None  # '' # Default video save API
    size: Optional[str] = None  # The size of the box, which can be set to md or lg
    options: Optional[dict] = None  # Need to refer to tinymce or froala documentation
    buttons: Optional[List[str]] = None  # froala dedicated, configure the displayed buttons, tinymce can set the toolbar
    # string through the previous options
    vendor: Optional[str] = None  # "vendor": "froala" , configure to use froala editor


class InputRating(FormItem):
    """Input Rating"""

    type: str = "input-rating"
    half: Optional[bool] = None  # default False, whether to use half star selection
    count: Optional[int] = None  # default 5, amount of total stars
    readOnly: Optional[bool] = None  # default False, is it read only
    allowClear: Optional[bool] = None  # default True, allow clearing after another click
    colors: Union[str, dict, None] = None  # default {'2': '#abadb1', '3': '#787b81', '5': '#ffa900' }, The color in which
    # the stars are displayed. If a string is passed in, there is only one color.
    # If an dict is passed in, each level can be customized.
    # The key name is the limit value of the segment, and the key value is the corresponding class name.
    inactiveColor: Optional[str] = None  # default #e7e7e8, color of unselected stars
    texts: Optional[dict] = None  # default -, The tooltip text when the star is selected.
    # key name is the level of the segment, and the value is the corresponding text
    textPosition: Literal["right", "left"] = "right"  # position of Tooltip
    char: Optional[str] = None  # default '*', custom character
    charClassNme: Optional[str] = None  # default -, custom char class name
    textClassName: Optional[str] = None  # default -, custom text class name


class InputRange(FormItem):
    """Input Range"""

    type: str = "input-range"
    min: Optional[int] = None  # default 0, min value
    max: Optional[int] = None  # default 100, max value
    step: Optional[int] = None  # default 1, step size
    showSteps: Optional[bool] = None  # default False, show step size
    parts: Union[int, List[int], None] = None  # default 1, Number of blocks to split
    marks: Union[str, dict, None] = None  # Tick Marks, Support Custom Styles, Set Percentages
    # { [number | string]: ReactNode }or{ [number | string]: { style: CSSProperties, label: ReactNode } }
    tooltipVisible: Optional[bool] = None  # default False, whether to show slider labels
    tooltipPlacement: Optional[PlacementEnum] = None  # defualt 'top', tooltip placement 'top'|'right'|'bottom'|'left'
    multiple: Optional[bool] = None  # default False, support selection range
    joinValues: Optional[bool] = None  # default True, show step size
    delimiter: Optional[str] = None  # dfeault ',', value delimiter
    unit: Optional[str] = None  # unit
    clearable: Optional[bool] = None  # default False, whether the precondition can be cleared : showInputValid when enabled
    showInput: Optional[bool] = None  # default False, whether to display the input box


class Timeline(AmisNode):
    """Timeline"""

    class TimelineItem(AmisNode):
        time: str  # Node Time
        title: Optional[SchemaNode] = None  # Node Title
        detail: Optional[str] = None  # Node detailed description (collapsed)
        detailCollapsedText: Optional[str] = None  # default 'Expand'
        detailExpandedText: Optional[str] = None  # default 'Collapse'
        color: Union[str, LevelEnum, None] = None  # default #DADBDD, Timeline node color
        icon: Optional[str] = None  # Icon name, support fontawesome v4 or use url (priority is higher than color)

    type: str = "timeline"
    items: Optional[List[TimelineItem]] = None  # default [], Nodes
    source: Optional[API] = None  # Data source, you can obtain current variables through data mapping, or configure API objects
    mode: Literal["left", "right", "alternate"] = "right"  # Position of the text relative to the timeline,
    # only supported when direction=vertical
    direction: Literal["vertical", "horizontal"] = "vertical"  # Direction of the Timeline
    reverse: Optional[bool] = None  # default False, Reverse chronological order


class Steps(AmisNode):
    """Steps Bar"""

    class StepItem(AmisNode):
        title: SerializeAsAny[Optional[SchemaNode]] = None  # Title
        subTitle: SerializeAsAny[Optional[SchemaNode]] = None  # Sub Heading
        description: SerializeAsAny[Optional[SchemaNode]] = None  # Detail Description
        value: Optional[str] = None  # Step Value
        icon: Optional[str] = None  # Icon name, support fontawesome v4 or use url (priority is higher than color)
        className: Optional[str] = None  # Custom CSS class name

    type: str = "steps"
    steps: SerializeAsAny[Optional[List[StepItem]]] = None  # default [], List of Steps
    source: Optional[API] = None  # Data source, you can obtain current variables through data mapping, or configure API objects
    name: Optional[str] = None  # Associated context variable
    value: Union[int, str, None] = None  # default -, Set the default value, expressions are not supported
    status: Union[StepStatusEnum, dict, None] = None  # default -, State of the steps
    className: Optional[str] = None  # Custom CSS class name
    mode: Literal["vertical", "horizontal"] = "horizontal"  # Specifies the step bar direction.
    labelPlacement: Literal["vertical", "horizontal"] = "horizontal"  # Specify the label placement position.
    # The default is to place it horizontally to the right of the icon, and optional (vertical) below the icon.
    progressDot: Optional[bool] = None  # Default False, show dotted step bar


class TooltipWrapper(AmisNode):
    type: str = "tooltip-wrapper"
    className: Optional[str] = None  # Content area class name
    tooltipClassName: Optional[str] = None  # Text prompt floating layer class name
    style: Union[str, dict, None] = None  # Custom style (inline style), highest priority
    tooltipStyle: Union[str, dict, None] = None  # floating layer custom style
    body: SerializeAsAny[Optional[SchemaNode]] = None  # Content container
    wrapperComponent: Optional[str] = None  # "div" | "span"
    inline: Optional[bool] = None  # default False, whether the content area is displayed inline
    rootClose: Optional[bool] = None  # default True, whether to click the non-content area to close the prompt
    mouseEnterDelay: Optional[int] = None  # default 0, Floating layer delay display time, in ms
    mouseLeaveDelay: Optional[int] = None  # default 300, Floating layer delay hiding time, in ms
    trigger: Union[
        TriggerEnum, List[TriggerEnum], None
    ] = None  # default 'hover', Floating layer trigger mode, support array writing
    # "hover" | "click" | "focus" | List["hover", "click", "focus"]
    disabled: Optional[bool] = None  # default False, whether to disable overlay prompts
    enterable: Optional[bool] = None  # default True, whether the mouse can move into the floating layer
    showArrow: Optional[bool] = None  # default True, whether to display the overlay pointing arrow
    offset: Optional[Tuple[int, int]] = None  # default [0, 0], relative offset of the position of the text prompt, in px
    tooltipTheme: Literal["light", "dark"] = "light"  # default light, Theme style
    placement: PlacementEnum = PlacementEnum.top  # text prompts position of the floating layer
    content: Optional[str] = None  # default '',  Text prompt content
    title: Optional[Optional[str]] = None  # default '', tooltip title


class InputTag(FormItem):
    """Input Tag"""

    type: str = "input-tag"
    options: Optional[List[Union[str, dict]]] = None  # default option group
    optionsTip: Optional[List[Union[str, dict]]] = None  # default "Your most recent tags", option hint
    source: Optional[API] = None  # default 	Dynamic option group
    delimiter: Optional[str] = None  # default False, delimiter option
    labelField: Optional[str] = None  # default "label", option label field
    valueField: Optional[str] = None  # default "value", option value field
    joinValues: Optional[bool] = None  # default True, Splice value
    extractValue: Optional[bool] = None  # default False, extract value
    clearable: Optional[bool] = None  # default False, whether to show a delete icon on the right when there is a value.
    resetValue: Optional[str] = None  # default "", Set the value given by this configuration item after deletion.
    max: Optional[int] = None  # Maximum number of tags allowed to be added
    maxTagLength: Optional[int] = None  # Maximum text length for a single label
    maxTagCount: Optional[int] = None  # The maximum number of labels to be displayed. If the number is exceeded,
    # it will be displayed in the form of a floating layer.
    # It will only take effect when the multi-selection mode is enabled.
    overflowTagPopover: Optional[TooltipWrapper] = None  # default {"placement": "top", "trigger": "hover", "showArrow": false,
    # "offset": [0, -10]}	Store the configuration properties of the floating layer,
    # please refer to Tooltip for detailed configuration
    enableBatchAdd: Optional[bool] = None  # default 	False, whether to enable batch add mode
    separator: Optional[str] = None  # default "-", After batch adding is enabled, enter the delimiter of multiple labels,
    # support multiple symbols


class Select(FormItem):
    """Drop down box"""

    type: str = "select"
    options: Optional[OptionsNode] = None  # option group
    source: Optional[API] = None  # Dynamic option group
    autoComplete: Optional[API] = None  # Automatic prompt completion
    delimiter: Union[bool, str, None] = None  # False # Splice
    labelField: Optional[str] = None  # "label" # option label field
    valueField: Optional[str] = None  # "value" # option value field
    joinValues: Optional[bool] = None  # True # join values
    extractValue: Optional[bool] = None  # False # extract value
    checkAll: Optional[bool] = None  # False # whether to support select all
    checkAllLabel: Optional[str] = None  # "Select All" # Text to be selected
    checkAllBySearch: Optional[bool] = None  # False # When there is a search, only all items hit by the search are selected
    defaultCheckAll: Optional[bool] = None  # False # whether to check all by default
    creatable: Optional[bool] = None  # False # New option
    multiple: Optional[bool] = None  # False # Multiple choice
    searchable: Optional[bool] = None  # False # search
    createBtnLabel: Optional[str] = None  # "Add option" # Add option
    addControls: SerializeAsAny[Optional[List[FormItem]]] = None  # Customize new form items
    addApi: Optional[API] = None  # Configure the new option interface
    editable: Optional[bool] = None  # False # edit options
    editControls: SerializeAsAny[Optional[List[FormItem]]] = None  # Customize edit form items
    editApi: Optional[API] = None  # Configure editing options interface
    removable: Optional[bool] = None  # False # remove option
    deleteApi: Optional[API] = None  # Configure delete option interface
    autoFill: Optional[dict] = None  # autofill
    menuTpl: Optional[str] = None  # Supports configuring custom menus
    clearable: Optional[bool] = None  # whether to support clearing in radio mode
    hideSelected: Optional[bool] = None  # False # hide the selected option
    mobileClassName: Optional[str] = None  # Mobile floating class name
    selectMode: Optional[str] = None  # Optional: group, table, tree, chained, associated. They are: list form, table form,
    # tree selection form, Cascade selection form, association selection form (the difference from cascading
    # selection is that the cascade is infinite, while the association has only one level, and the left side of the
    # association can be a tree).
    searchResultMode: Optional[str] = None  # If the value of selectMode is not set, it can be configured separately. Refer to
    # selectMode to determine the display form of search results.
    columns: Optional[List[dict]] = None  # When the display form is table, it can be used to configure which columns are
    # displayed, which is similar to the columns configuration in table, but only has the display function.
    leftOptions: Optional[List[dict]] = None  # Used to configure the left option set when the display form is associated.
    leftMode: Optional[str] = None  # When the display form is associated, it is used to configure the left selection form,
    # support list or tree. Default is list.
    rightMode: Optional[str] = None  # When the display form is associated, it is used to configure the right selection form,
    # optional: list, table, tree, chained.


class ChainedSelect(FormItem):
    """Chained Drop down boxs"""

    type: str = "chained-select"
    options: Optional[OptionsNode] = None  # option group
    source: Optional[API] = None  # Dynamic option group
    autoComplete: Optional[API] = None  # Automatic prompt completion
    delimiter: Optional[str] = None  # Default ',', Splice
    labelField: Optional[str] = None  # Default "label", option label field
    valueField: Optional[str] = None  # Default "value", option value field
    joinValues: Optional[bool] = None  # Default True, join values
    extractValue: Optional[bool] = None  # Default False, extract value


class NestedSelect(Select):
    """Cascade selector"""

    type: str = "nested-select"
    cascade: Optional[bool] = None  # False # When set to true, child nodes are not automatically selected when the parent node
    # is selected.
    withChildren: Optional[bool] = None  # False # When set to true, when the parent node is selected, the value of the child
    # node will be included in the value, otherwise only the value of the parent node will be retained.
    onlyChildren: Optional[bool] = None  # False # For multiple selections, whether to add only its child nodes to the value
    # when the parent node is selected.
    searchPromptText: Optional[str] = None  # "Enter content to search" # Search box placeholder text
    noResultsText: Optional[str] = None  # "No results found" # Text if no results
    hideNodePathLabel: Optional[bool] = None  # False # whether to hide the path label information of the selected node in the
    # selection box
    onlyLeaf: Optional[bool] = None  # False # Only leaf nodes are allowed to be selected


class Breadcrumb(AmisNode):
    """Breadcrumb line"""

    class BreadcrumbItem(AmisNode):
        label: Optional[str] = None  # label text
        href: Optional[str] = None  # link
        icon: Optional[str] = None  # fa icon
        dropdown: Optional[List] = None  # list of breadcrumbitems as dropdown, needs label, href, icon

    type: str = "breadcrumb"
    className: Optional[str] = None  # The outer class name
    itemClassName: Optional[str] = None  # Navigation item class name
    separatorClassName: Optional[str] = None  # separator class name
    dropdownClassName: Optional[str] = None  # Dropdown menu class name
    dropdownItemClassName: Optional[str] = None  # Dropdown menu item class name
    separator: str = ">"  # delimeter
    labelMaxLength: Optional[int] = None  # Default 16, max display length
    tooltipPosition: PlacementEnum = PlacementEnum.top  # tooltip position
    source: Optional[API] = None  # dynamic data
    items: SerializeAsAny[Optional[List[BreadcrumbItem]]] = None  # list of breadcrumb icons


class Card(AmisNode):
    """Card"""

    class Media(AmisNode):
        type: Literal["image", "video"] = "image"  # multimedia type
        url: Optional[str] = None  # image or video link
        position: PlacementEnum = PlacementEnum.left  # media location
        className: Optional[str] = None  # default "w-44 h-28", multimedia CSS class
        isLive: Optional[bool] = None  # default False, video is live or not
        autoPlay: Optional[bool] = None  # default False, autoplay video
        poster: Union[bool, str, None] = None  # default false

    class Header(AmisNode):
        className: Optional[str] = None  # The header class name
        title: Optional[Optional[str]] = None  # title
        titleClassName: Optional[str] = None  # title class name
        subTitle: Optional[Template] = None  # subtitle
        subTitleClassName: Optional[str] = None  # subtitle class name
        subTitlePlaceholder: Optional[str] = None  # Subtitle placeholder
        description: Optional[Template] = None  # Description
        descriptionClassName: Optional[str] = None  # Description class name
        descriptionPlaceholder: Optional[str] = None  # Description placeholder
        avatar: Optional[Template] = None  # picture
        avatarClassName: Optional[str] = None  # default "pull-left thumb avatar b-3x m-r", Image includes layer class name
        imageClassName: Optional[str] = None  # Image class name
        avatarText: Optional[Template] = None  # If no picture is configured, the text will be displayed at the picture
        avatarTextBackground: Optional[str] = None  # avatar text background color
        avatarTextClassName: Optional[str] = None  # Image text class name
        highlight: Optional[bool] = None  # default False, whether to show the active style
        highlightClassName: Optional[str] = None  # Active style class name
        href: Optional[str] = None  # external link link
        blank: Optional[bool] = None  # default True, open link in new window

    type: str = "card"
    className: Optional[str] = None  # The outer class name
    href: Optional[str] = None  # external link link
    header: SerializeAsAny[Optional[Header]] = None  # Header object
    body: List = []  # Content container, mainly used to place non-form item components
    bodyClassName: Optional[str] = None  # Content area class name
    actions: SerializeAsAny[Optional[List[Action]]] = None  # Configure button collection
    actionsCount: Optional[int] = None  # default 4, number of buttons in each row
    itemAction: SerializeAsAny[Optional[Action]] = None  # clicking on a card action
    media: SerializeAsAny[Optional[Media]] = None  # Media object
    secondary: Optional[Template] = None  # secondary note
    toolbar: SerializeAsAny[Optional[List[Action]]] = None  # toolbar buttons
    dragging: Optional[bool] = None  # default False, Whether to show the drag icon
    selectable: Optional[bool] = None  # default False, can be selected
    checkable: Optional[bool] = None  # default True, selection button is disabled or not
    selected: Optional[bool] = None  # default False, selection button is selected or not
    hideCheckToggler: Optional[bool] = None  # default False, hide the selection button
    multiple: Optional[bool] = None  # default False, multi-select or not
    useCardLabel: Optional[bool] = None  # default True, Whether the form item label in the card content area uses the
    # style inside the Card


class Cards(AmisNode):
    """Cards deck, allows to use data source to display data items as cards, or manual"""

    type: str = "cards"
    title: Optional[Optional[str]] = None  # title
    source: Optional[str] = None  # default '${items}', Data source, get the variables in the current data field
    placeholder: Optional[str] = None  # default 'No data', placeholder
    className: Optional[str] = None  # The outer CSS class name
    headerClassName: Optional[str] = None  # default 'amis-grid-header', Top outer CSS class name
    footerClassName: Optional[str] = None  # default 'amis-grid-footer', Bottom outer CSS class name
    itemClassName: Optional[str] = None  # default 'col-sm-4 col-md-3', Card CSS class name
    card: Optional[Card] = None  # configured card object for repeat


class ListDisplay(AmisNode):
    """Cards deck, allows to use data source to display data items as cards, or manual"""

    class ListItem(AmisNode):
        title: Optional[Optional[str]] = None  # title
        titleClassName: Optional[str] = None  # title class name
        subTitle: Optional[Template] = None  # subtitle
        avatar: Optional[Template] = None  # picture
        avatarClassName: Optional[str] = None  # default "thumb-sm avatar m-r", Image CSS class name
        desc: Optional[Template] = None  # Description
        body: Optional[List] = None  # Content container, mainly used to place non-form item components
        actions: SerializeAsAny[Optional[List[Action]]] = None  # action buttons area
        actionsPosition: Literal["left", "right"] = "right"  # button position

    type: str = "list"
    title: Optional[Optional[str]] = None  # title
    source: Optional[str] = None  # default '${items}', Data source, get the variables in the current data field
    placeholder: Optional[str] = None  # default 'No data', placeholder
    className: Optional[str] = None  # The outer CSS class name
    headerClassName: Optional[str] = None  # default 'amis-grid-header', Top outer CSS class name
    footerClassName: Optional[str] = None  # default 'amis-grid-footer', Bottom outer CSS class name
    listItem: SerializeAsAny[Optional[ListItem]] = None  # configured list object for repeat


class Textarea(FormItem):
    """Multi-line text input box"""

    type: str = "textarea"
    minRows: Optional[int] = None  # Minimum number of rows
    maxRows: Optional[int] = None  # maximum number of rows
    trimContents: Optional[bool] = None  # whether to remove leading and trailing blank text
    readOnly: Optional[bool] = None  # read-only
    showCounter: bool = True  # whether to show the counter
    minLength: Optional[int] = None  # Limit the minimum number of words
    maxLength: Optional[int] = None  # Limit the maximum number of characters


class InputMonth(FormItem):
    """month"""

    type: str = "input-month"
    value: Optional[str] = None  # default value
    format: Optional[str] = None  # "X" # Month selector value format, please refer to moment for more format types
    inputFormat: Optional[str] = None  # "YYYY-MM" # The display format of the month selector, that is, the timestamp format.
    # For more format types, please refer to moment
    placeholder: Optional[str] = None  # "Please select a month" # placeholder text
    clearable: Optional[bool] = None  # True # whether it can be cleared


class InputTime(FormItem):
    """time"""

    type: str = "input-time"
    value: Optional[str] = None  # default value
    timeFormat: Optional[str] = None  # "HH:mm" # Time selector value format, please refer to moment for more format types
    format: Optional[str] = None  # "X" # Time selector value format, please refer to moment for more format types
    inputFormat: Optional[str] = None  # "HH:mm" # Time selector display format, that is, timestamp format, please refer to
    # moment for more format types
    placeholder: Optional[str] = None  # "Please select a time" # placeholder text
    clearable: Optional[bool] = None  # True # whether it can be cleared
    timeConstraints: Optional[dict] = None  # True # Please refer to: react-datetime


class InputDatetime(FormItem):
    """date"""

    type: str = "input-datetime"
    value: Optional[str] = None  # default value
    format: Optional[str] = None  # "X" # Date time picker value format, please refer to the documentation for more format types
    inputFormat: Optional[str] = None  # "YYYY-MM-DD HH:mm:ss" # Date time picker display format, namely timestamp format,
    # please refer to the documentation for more format types
    placeholder: Optional[str] = None  # "Please select a date and time" # placeholder text
    shortcuts: Optional[str] = None  # datetime shortcuts
    minDate: Optional[str] = None  # Limit the minimum date and time
    maxDate: Optional[str] = None  # Limit maximum date time
    utc: Optional[bool] = None  # False # save utc value
    clearable: Optional[bool] = None  # True # whether it can be cleared
    embed: Optional[bool] = None  # False # whether to inline
    timeConstraints: Optional[dict] = None  # True # Please refer to: react-datetime


class InputDate(FormItem):
    """date"""

    type: str = "input-date"
    value: Optional[str] = None  # default value
    format: Optional[str] = None  # "X" # Date picker value format, please refer to the documentation for more format types
    inputFormat: Optional[str] = None  # "YYYY-DD-MM" # Date picker display format, that is, timestamp format, please refer to
    # the documentation for more format types
    placeholder: Optional[str] = None  # "Please select a date" # placeholder text
    shortcuts: Optional[str] = None  # date shortcuts
    minDate: Optional[str] = None  # Limit the minimum date
    maxDate: Optional[str] = None  # limit max date
    utc: Optional[bool] = None  # False # save utc value
    clearable: Optional[bool] = None  # True # whether it can be cleared
    embed: Optional[bool] = None  # False # whether to inline mode
    timeConstraints: Optional[dict] = None  # True # Please refer to: react-datetime
    closeOnSelect: Optional[bool] = None  # False # whether to close the selection box immediately after clicking the date
    schedules: Union[list, str, None] = None  # The schedule is displayed in the calendar, static data can be set or data
    # can be taken from the context, className refers to the background color
    scheduleClassNames: Optional[List[str]] = None  # "['bg-warning','bg-danger','bg-success','bg-info','bg-secondary']"
    # The color of the event displayed in the calendar, refer to the background color
    scheduleAction: SerializeAsAny[Optional[SchemaNode]] = None  # Custom schedule display
    largeMode: Optional[bool] = None  # False # zoom mode


class InputQuarter(InputDate):
    """InputQuarter"""

    type: str = "input-quarter"


class InputQuarterRange(FormItem):
    """Quarter range"""

    type: str = "input-quarter-range"
    format: Optional[str] = None  # Default X, date picker value format
    inputFormat: Optional[str] = None  # Default 'YYYY-DD', date picker display format
    placeholder: Optional[str] = None  # Default 'Please select a quarterly range', placeholder text
    minDate: Optional[str] = None  # Limit the minimum date and time, the usage is the same as the limit range
    maxDate: Optional[str] = None  # Limit the maximum date and time, the usage is the same as the limit range
    minDuration: Optional[str] = None  # Limit the minimum span, such as: 2quarter
    maxDuration: Optional[str] = None  # Limit the maximum span, such as: 4quarter
    utc: Optional[bool] = None  # Default False, save UTC value
    clearable: Optional[bool] = None  # Default True, Is it clearable
    embed: Optional[bool] = None  # Default False, inline mode
    animation: Optional[bool] = None  # Default True, Whether to enable cursor animation, needs min amis 2.2.0


class Calendar(FormItem):
    """Calendar"""

    class CalendarItem(AmisNode):
        startTime: str  # ISO 8601 string
        endTime: str  # ISO 8601 string
        content: Union[str, int, dict, None] = None  # Any, static data or get data from the context
        className: Optional[str] = None  # css background

    type: str = "calendar"
    schedules: Union[List[CalendarItem], str, None] = None  # List of schedule items
    scheduleClassNames: Optional[List[str]] = None  # default ['bg-warning', 'bg-danger', 'bg-success', 'bg-info', 'bg-secondary']
    # color of the event displayed in the calendar, refer to the background color

    scheduleAction: SerializeAsAny[Optional[SchemaNode]] = None  # custom schedule display
    largeMode: Optional[bool] = None  # Default False, zoom mode full size
    todayActiveStyle: Union[str, dict, None] = None  # Custom styles when activated today


class InputKV(FormItem):
    """Input key-value pair"""

    type: str = "input-kv"
    valueType: Optional[str] = None  # Default "input-text", value item type
    keyPlaceholder: Optional[str] = None  # key placeholder information
    valuePlaceholder: Optional[str] = None  # value placeholder information
    draggable: Optional[bool] = None  # Default True, Whether to drag and drop to sort is allowed
    defaultValue: Union[str, int, dict, None] = None  # default ''
    keySchema: SerializeAsAny[Optional[SchemaNode]] = None  # key field schema
    valueSchema: SerializeAsAny[Optional[SchemaNode]] = None  # value field schema


class InputKVS(FormItem):
    """Input key-value pair, where value can be a deep structure"""

    type: str = "input-kvs"
    addButtonText: Optional[str] = None  # default 'new field', butto text of the add button
    draggable: Optional[bool] = None  # Default True, Whether to drag and drop to sort is allowed
    keyItem: SerializeAsAny[Optional[SchemaNode]] = None  # key field
    valueItems: SerializeAsAny[Optional[List[SchemaNode]]] = None  # items for the key


class InputTimeRange(FormItem):
    """time limit"""

    type: str = "input-time-range"
    timeFormat: Optional[str] = None  # "HH:mm" # Time range selector value format
    format: Optional[str] = None  # "HH:mm" # time range selector value format
    inputFormat: Optional[str] = None  # "HH:mm" # Time range selector display format
    placeholder: Optional[str] = None  # "Please select a time range" # placeholder text
    clearable: Optional[bool] = None  # True # whether it can be cleared
    embed: Optional[bool] = None  # False # whether to inline mode


class InputDatetimeRange(InputTimeRange):
    """Date time range"""

    type: str = "input-datetime-range"
    ranges: Union[str, List[str], None] = None  # "yesterday,7daysago,prevweek,thismonth,prevmonth,prevquarter" date range
    # shortcut keys, Optional: today,yesterday,1dayago,7daysago,30daysago,90daysago,prevweek,thismonth,thisquarter,
    # prevmonth,prevquarter
    minDate: Optional[str] = None  # Limit the minimum date and time, the usage is the same as the limit range
    maxDate: Optional[str] = None  # Limit the maximum date and time, the usage is the same as the limit range
    utc: Optional[bool] = None  # False # save UTC value


class InputDateRange(InputDatetimeRange):
    """Date Range"""

    type: str = "input-date-range"
    minDuration: Optional[str] = None  # Limit the minimum span, such as: 2days
    maxDuration: Optional[str] = None  # Limit the maximum span, such as: 1year


class InputMonthRange(InputDateRange):
    """month range"""

    type: str = "input-month-range"


class Transfer(FormItem):
    """Shuttle"""

    type: Literal["transfer", "transfer-picker", "tabs-transfer", "tabs-transfer-picker"] = "transfer"
    options: Optional[OptionsNode] = None  # option group
    source: Optional[API] = None  # Dynamic option group
    delimiter: Optional[str] = None  # "False" # splicer
    joinValues: Optional[bool] = None  # True # join values
    extractValue: Optional[bool] = None  # False # extract value
    searchable: Optional[
        bool
    ] = None  # False When set to true, it means that options can be retrieved by entering partial content.
    searchApi: Optional[API] = None  # If you want to retrieve through the interface, you can set an api.
    statistics: Optional[bool] = None  # True # whether to display statistics
    selectTitle: Optional[str] = None  # "Please select" # Title text on the left
    resultTitle: Optional[str] = None  # "current selection" # title text of the result on the right
    sortable: Optional[bool] = None  # False # The result can be sorted by drag and drop
    selectMode: Optional[str] = None  # "list" # Optional: list, table, tree, chained, associated. They are: list form,
    # table form, tree selection form, Cascade selection form, association selection form (the difference from
    # cascading selection is that the cascade is infinite, while the association has only one level, and the left
    # side of the association can be a tree).
    searchResultMode: Optional[str] = None  # If the value of selectMode is not set, it can be configured separately. Refer to
    # selectMode to determine the display form of search results.
    columns: Optional[List[dict]] = None  # When the display form is table, it can be used to configure which columns are
    # displayed, which is similar to the columns configuration in table, but only has the display function.
    leftOptions: Optional[List[dict]] = None  # Used to configure the left option set when the display form is associated.
    leftMode: Optional[str] = None  # When the display form is associated, it is used to configure the left selection form,
    # support list or tree. Default is list.
    rightMode: Optional[str] = None  # When the display form is associated, it is used to configure the right selection form,
    # optional: list, table, tree, chained.
    menuTpl: SerializeAsAny[Optional[SchemaNode]] = None  # Used to customize option display
    valueTpl: SerializeAsAny[Optional[SchemaNode]] = None  # Used to customize the display of the value


class TransferPicker(Transfer):
    """Shuttle selector"""

    type: str = "transfer-picker"


class TabsTransfer(Transfer):
    """Combination shuttle"""

    type: str = "tabs-transfer"


class TabsTransferPicker(Transfer):
    """Combination shuttle selector"""

    type: str = "tabs-transfer-picker"


class InputTree(FormItem):
    """Tree selection box"""

    type: str = "input-tree"
    options: Optional[OptionsNode] = None  # option group
    source: Optional[API] = None  # Dynamic option group
    autoComplete: Optional[API] = None  # Automatic prompt completion
    multiple: Optional[bool] = None  # False # whether to select multiple
    delimiter: Optional[str] = None  # "False" # splicer
    labelField: Optional[str] = None  # "label" # option label field
    valueField: Optional[str] = None  # "value" # option value field
    iconField: Optional[str] = None  # "icon" # icon value field
    joinValues: Optional[bool] = None  # True # join values
    extractValue: Optional[bool] = None  # False # extract value
    creatable: Optional[bool] = None  # False # New option
    addControls: SerializeAsAny[Optional[List[FormItem]]] = None  # Customize new form items
    addApi: Optional[API] = None  # Configure the new option interface
    editable: Optional[bool] = None  # False # edit options
    editControls: SerializeAsAny[Optional[List[FormItem]]] = None  # Customize edit form items
    editApi: Optional[API] = None  # Configure editing options interface
    removable: Optional[bool] = None  # False # remove option
    deleteApi: Optional[API] = None  # Configure delete option interface
    searchable: Optional[bool] = None  # False # whether it is searchable, it only takes effect when type is tree-select
    hideRoot: Optional[bool] = None  # True # Set to false if you want to show a top-level node
    rootLabel: Optional[
        bool
    ] = None  # "top level" # Useful when hideRoot is not false, used to set the text of the top level node.
    showIcon: Optional[bool] = None  # True # whether to show the icon
    showRadio: Optional[bool] = None  # False # whether to show radio buttons, multiple is false is valid.
    initiallyOpen: Optional[bool] = None  # True # Set whether to expand all levels by default.
    unfoldedLevel: Optional[int] = None  # 0 # Set the default unfolded level, which only takes effect when initiallyOpen is
    # not true.
    cascade: Optional[bool] = None  # False # Do not automatically select child nodes when parent node is selected.
    withChildren: Optional[bool] = None  # False # When the parent node is selected, the value will contain the value of the
    # child node, otherwise only the value of the parent node will be retained.
    onlyChildren: Optional[bool] = None  # False # For multiple selections, whether to add only its child nodes to the value
    # when the parent node is selected.
    rootCreatable: Optional[bool] = None  # False # whether top-level nodes can be created
    rootCreateTip: Optional[str] = None  # "Add a first-level node" # Create a hovering tip for a top-level node
    minLength: Optional[int] = None  # Minimum number of selected nodes
    maxLength: Optional[int] = None  # Maximum number of nodes selected
    treeContainerClassName: Optional[str] = None  # tree outermost container class name
    enableNodePath: Optional[bool] = None  # False # whether to enable node path mode
    pathSeparator: Optional[str] = None  # "/" # The separator of the node path, it takes effect when enableNodePath is true
    deferApi: Optional[API] = None  # For lazy loading options, please configure defer to true, and then configure deferApi to
    # complete lazy loading
    selectFirst: Optional[bool] = None
    showOutline: Optional[bool] = None  # False  # 是否显示树层级展开线
    autoCheckChildren: Optional[bool] = None  # True  # 当选中父节点时级联选择子节点。
    onlyLeaf: Optional[bool] = None  # False  # 只允许选择叶子节点
    highlightTxt: Optional[str] = None  # None  # 标签中需要高亮的字符，支持变量
    itemHeight: Optional[int] = None  # 32  # 每个选项的高度，用于虚拟渲染
    virtualThreshold: Optional[int] = None  # 100  # 在选项数量超过多少时开启虚拟渲染
    menuTpl: Optional[str] = None  # 选项自定义渲染 HTML 片段
    enableDefaultIcon: Optional[bool] = None  # True  # 是否为选项添加默认的前缀 Icon，
    # 父节点默认为folder，叶节点默认为file
    heightAuto: Optional[bool] = None  # False  # 默认高度会有个 maxHeight，
    # 即超过一定高度就会内部滚动，如果希望自动增长请设置此属性


class TreeSelect(InputTree):
    """Tree selector"""

    type: str = "tree-select"
    hideNodePathLabel: Optional[
        bool
    ] = None  # whether to hide the path label information of the selected node in the selection box


class Image(AmisNode):
    """picture"""

    type: str = "image"  # "image" if used in Table, Card and List; "static-image" if used as static display in Form
    className: Optional[str] = None  # Outer CSS class name
    imageClassName: Optional[str] = None  # Image CSS class name
    thumbClassName: Optional[str] = None  # Thumbnail CSS class name
    height: Optional[int] = None  # Image reduction height
    width: Optional[int] = None  # Image reduction width
    title: Optional[Optional[str]] = None  # title
    imageCaption: Optional[str] = None  # description
    placeholder: Optional[str] = None  # placeholder text
    defaultImage: Optional[str] = None  # The image displayed when there is no data
    src: Optional[str] = None  # Thumbnail address
    href: Optional[Template] = None  # External link address
    originalSrc: Optional[str] = None  # Original image address
    enlargeAble: Optional[bool] = None  # Support zoom in preview
    enlargeTitle: Optional[str] = None  # enlarge the title of the preview
    enlargeCaption: Optional[str] = None  # Description of the enlarged preview
    thumbMode: Optional[str] = None  # "contain" # preview mode, optional: 'w-full','h-full','contain','cover'
    thumbRatio: Optional[str] = None  # "1:1" # Preview ratio, optional: '1:1','4:3','16:9'
    imageMode: Optional[str] = None  # "thumb" Image display mode, optional: 'thumb', 'original' ie: thumbnail mode or original
    # image mode


class Images(AmisNode):
    """Photo album"""

    type: str = "images"  # "images" if used in Table, Card and List; "static-images" if used as static display in Form
    className: Optional[str] = None  # Outer CSS class name
    defaultImage: Optional[str] = None  # Default display image
    value: Union[str, List[str], List[dict], None] = None  # Image array
    source: Optional[str] = None  # data source
    delimiter: Optional[str] = None  # "," # Delimiter, when value is a string, use this value to separate and split
    src: Optional[str] = None  # Preview image address, support data mapping to obtain image variables in the object
    originalSrc: Optional[str] = None  # Original image address, support data mapping to obtain image variables in the object
    enlargeAble: Optional[bool] = None  # Support zoom in preview
    thumbMode: Optional[str] = None  # "contain" # preview mode, optional: 'w-full','h-full','contain','cover'
    thumbRatio: Optional[str] = None  # "1:1" # Preview ratio, optional: '1:1','4:3','16:9'


class Carousel(AmisNode):
    """Carousel"""

    class Item(AmisNode):
        image: Optional[str] = None  # Image link
        href: Optional[str] = None  # Image open URL link
        imageClassName: Optional[str] = None  # Image class name
        title: Optional[Optional[str]] = None  # image title
        titleClassName: Optional[str] = None  # Image title class name
        description: Optional[str] = None  # Picture description
        descriptionClassName: Optional[str] = None  # Picture description class name
        html: Optional[str] = None  # HTML custom, same as Tpl

    type: str = "carousel"  # Specify as the Carousel renderer
    className: Optional[str] = None  # "panel-default" # The class name of the outer Dom
    options: SerializeAsAny[Optional[List[Item]]] = None  # "[]" # Carousel panel data
    itemSchema: Optional[dict] = None  # custom schema to display data
    auto: bool = True  # whether to rotate automatically
    interval: Optional[str] = None  # "5s" # Switch animation interval
    duration: Optional[str] = None  # "0.5s" # Switch animation duration
    width: Optional[str] = None  # "auto" # width
    height: Optional[str] = None  # "200px" # height
    controls: Optional[List[str]] = None  # "['dots','arrows']" # Display left and right arrows, bottom dot index
    controlsTheme: Optional[str] = None  # "light" # Left and right arrows, bottom dot index color, default light, and dark mode
    animation: Optional[str] = None  # "fade" # Switch animation effect, default fade, and slide mode
    thumbMode: Optional[str] = None  # "cover"|"contain" # The default zoom mode of the picture


class Mapping(AmisNode):
    """Mapping"""

    type: str = "mapping"  # "mapping" if used in Table, Card and List; "static-mapping" if used as static display in Form
    className: Optional[str] = None  # Outer CSS class name
    placeholder: Optional[str] = None  # placeholder text
    map: Optional[dict] = None  # map configuration
    source: Optional[API] = None  # API or data map


class CRUD(AmisNode):
    """Add, delete, modify, check"""

    class Messages(AmisNode):
        fetchFailed: Optional[str] = None  # Prompt when fetch fails
        saveOrderFailed: Optional[str] = None  # Failed to save order
        saveOrderSuccess: Optional[str] = None  # Save order success prompt
        quickSaveFailed: Optional[str] = None  # Quick save failure prompt
        quickSaveSuccess: Optional[str] = None  # Quick save success prompt

    type: str = "crud"  # type specifies the CRUD renderer
    mode: Optional[str] = None  # "table" # "table" , "cards" or "list"
    title: Optional[Optional[str]] = None  # "" # Can be set to empty, when set to empty, there is no title bar
    className: Optional[str] = None  # The class name of the outer Dom of the table
    api: Optional[API] = None  # The api that CRUD uses to get list data.
    loadDataOnce: Optional[bool] = None  # whether to load all data at once (front-end paging)
    loadDataOnceFetchOnFilter: Optional[bool] = None  # True # When loadDataOnce is turned on, whether to re-request the api
    # when filtering
    source: Optional[str] = None  # The data mapping interface returns the value of a field. If it is not set, the ${items} or
    # ${rows} returned by the interface will be used by default. It can also be set to the content of the upper data
    # source.
    filter: SerializeAsAny[
        Optional[Union[SchemaNode, Form]]
    ] = None  # Set the filter, when the form is submitted, it will bring the data to
    # the current mode refresh list.
    filterTogglable: Optional[bool] = None  # False # whether the filter can be displayed or hidden
    filterDefaultVisible: Optional[bool] = None  # True # Set whether the filter is visible by default.
    initFetch: Optional[bool] = None  # True # whether to pull data during initialization, only for the case with filter,
    # without filter, data will be pulled initially
    interval: Optional[int] = None  # refresh time (minimum 1000)
    silentPolling: Optional[bool] = None  # Configure whether to hide the loading animation when refreshing
    stopAutoRefreshWhen: Optional[str] = None  # Configure the condition for stopping refresh by expression
    stopAutoRefreshWhenModalIsOpen: Optional[bool] = None  # Turn off auto refresh when there is a popup, close the popup and
    # restore
    syncLocation: Optional[bool] = None  # False # whether to synchronize the parameters of the filter conditions to the
    # address bar, !!! After opening, the data type may be changed, and it cannot pass the fastpi data verification
    draggable: Optional[bool] = None  # whether it can be sorted by dragging
    itemDraggableOn: Optional[bool] = None  # Use expressions to configure whether drag and drop sorting is possible
    saveOrderApi: Optional[API] = None  # Save order api.
    quickSaveApi: Optional[API] = None  # API for batch saving after quick editing.
    quickSaveItemApi: Optional[API] = None  # API to use when quick edit is configured to save in time.
    bulkActions: SerializeAsAny[
        Optional[List[Action]]
    ] = None  # Batch operation list, after configuration, the table can be selected.
    defaultChecked: Optional[bool] = None  # When batch operations are available, whether to check all by default.
    messages: SerializeAsAny[
        Optional[Messages]
    ] = None  # Override the message prompt, if not specified, the message returned by the api will
    # be used
    primaryField: Optional[str] = None  # Set the ID field name. 'id'
    perPage: Optional[int] = None  # Set how many pieces of data are displayed on one page. 10
    defaultParams: Optional[dict] = None  # Set the default filter default parameters, which will be sent to the backend
    # together when querying
    pageField: Optional[str] = None  # Set the pagination page number field name. "page"
    perPageField: Optional[str] = None  # "perPage" # Set the field name of how many pieces of data are displayed on one page.
    # Note: Best used with defaultParams, see example below.
    perPageAvailable: Optional[List[int]] = None  # [5, 10, 20, 50, 100] # Set how many data drop-down boxes can be displayed
    # on one page.
    orderField: Optional[str] = None  # Set the field name used to determine the position. After setting, the new order will be
    # assigned to this field.
    hideQuickSaveBtn: Optional[bool] = None  # Hide the top quick save prompt
    autoJumpToTopOnPagerChange: Optional[bool] = None  # whether to automatically jump to the top when splitting pages.
    syncResponse2Query: Optional[bool] = None  # True # Synchronize the returned data to the filter.
    keepItemSelectionOnPageChange: Optional[bool] = None  # True
    # Retain item selection. After the default paging and searching, the user-selected item will be cleared. After
    # this option is enabled, the user's selection will be retained, enabling cross-page batch operations.
    labelTpl: Optional[str] = None  # Single description template, keepItemSelectionOnPageChange
    # When set to true, all selected items will be listed. This option can be used to customize the entry display copy.
    headerToolbar: Optional[list] = None  # ['bulkActions','pagination'] # Top toolbar configuration
    footerToolbar: Optional[list] = None  # ['statistics','pagination'] # Bottom toolbar configuration
    alwaysShowPagination: Optional[bool] = None  # whether to always show pagination
    affixHeader: Optional[bool] = None  # True # whether to fix the header (under table)
    autoGenerateFilter: Optional[bool] = None  # whether to open the query area, after it is enabled, the query condition form
    # will be automatically generated according to the searchable attribute value of the column element
    itemAction: Optional[Action] = None  # Implement custom actions after clicking a row, support all configurations in action,
    # such as pop-up boxes, refresh other components, etc.
    resizable: Optional[bool] = None  # 是否可以调整列宽度
    orderBy: Optional[str] = None  # 默认排序字段，这个是传给后端，需要后端接口实现
    orderDir: Optional[Literal["asc", "desc"]] = None  # 排序方向
    resetPageAfterAjaxItemAction: Optional[bool] = None  # False  # 单条数据 ajax 操作后是否重置页码为第一页
    autoFillHeight: Union[bool, Dict[str, int], None] = None  # 内容区域自适应高度


class TableColumn(AmisNode):
    """Column configuration"""

    type: Optional[str] = None  # Literal['text','audio','image','link','tpl','mapping','carousel','date',
    # 'progress','status','switch','list','json','operation','tag']
    label: Optional[Template] = None  # header text content
    name: Optional[str] = None  # Associate data by name
    tpl: Optional[Template] = None  # Template
    fixed: Optional[str] = None  # whether to fix the current column left|right|none
    popOver: Union[bool, dict, None] = None  # popover
    quickEdit: Union[bool, dict, None] = None  # quick edit
    copyable: Union[bool, dict, None] = None  # whether to copy boolean or {icon: string, content:string}
    sortable: Optional[bool] = None  # False # whether it is sortable
    searchable: SerializeAsAny[Optional[Union[bool, SchemaNode]]] = None  # False # whether to quickly search boolean|Schema
    width: Union[int, str, None] = None  # column width
    remark: Optional[RemarkT] = None  # prompt message
    breakpoint: Optional[str] = None  # *,ls. When there are too many columns, the content cannot be displayed completely,
    # some information can be displayed at the bottom, and users can expand to view the details
    filterable: Union[bool, Dict[str, Any], None] = None  # filter configuration
    toggled: Optional[bool] = None  # whether to expand by default, in the column configuration, you can configure toggled to
    # false to not display this column by default
    backgroundScale: Optional[int] = None  # Can be used to automatically assign color scales based on data control


class ColumnOperation(TableColumn):
    """Action column"""

    type: str = "operation"
    buttons: SerializeAsAny[Optional[List[Union[Action, AmisNode, dict]]]] = None


class ColumnImage(Image, TableColumn):
    """Picture column"""

    pass


class ColumnImages(Images, TableColumn):
    """Picture collection column"""

    pass


class ColumnMapping(Mapping, TableColumn):
    """Map column"""

    pass


class Table(AmisNode):
    """sheet"""

    type: str = "table"  # Specify as table renderer
    title: Optional[Optional[str]] = None  # title
    source: Optional[str] = None  # "${items}" # Data source, bind the current environment variable
    affixHeader: Optional[bool] = None  # True # whether to fix the header
    columnsTogglable: Union[bool, str, None] = None  # "auto" # Display column display switch, automatic: it is
    # automatically turned on when the number of columns is greater than or equal to 5
    placeholder: Optional[str] = None  # "No data" # Text prompt when there is no data
    className: Optional[str] = None  # "panel-default" # Outer CSS class name
    tableClassName: Optional[str] = None  # "table-db table-striped" # table CSS class name
    headerClassName: Optional[str] = None  # "Action.md-table-header" # Top outer CSS class name
    footerClassName: Optional[str] = None  # "Action.md-table-footer" # Bottom outer CSS class name
    toolbarClassName: Optional[str] = None  # "Action.md-table-toolbar" # Toolbar CSS class name
    columns: SerializeAsAny[Optional[List[Union[TableColumn, SchemaNode]]]] = None  # Used to set column information
    combineNum: Optional[int] = None  # Automatically combine cells
    itemActions: SerializeAsAny[Optional[List[Action]]] = None  # Floating row action button group
    itemCheckableOn: Optional[Expression] = None  # Configure the condition for whether the current row can be checked, use an
    # expression
    itemDraggableOn: Optional[Expression] = None  # To configure whether the current row can be dragged or not, use an expression
    checkOnItemClick: Optional[bool] = None  # False # whether clicking on the data row can check the current row
    rowClassName: Optional[str] = None  # Add CSS class name to row
    rowClassNameExpr: Optional[Template] = None  # Add CSS class name to row via template
    prefixRow: Optional[list] = None  # top summary row
    affixRow: Optional[list] = None  # Bottom summary row
    itemBadge: SerializeAsAny[Optional["Badge"]] = None  # Row badge configuration
    autoFillHeight: Optional[bool] = None  # Content area adaptive height
    footable: Union[bool, dict, None] = None  # When there are too many columns, the content cannot be fully displayed.
    # Some information can be displayed at the bottom, allowing users to expand to view the details. The
    # configuration is very simple, just turn on the footable attribute, and add a breakpoint attribute to the column
    # you want to display at the bottom as *.
    resizable: Optional[bool] = None  # 列宽度是否支持调整
    selectable: Optional[bool] = None  # 支持勾选
    multiple: Optional[bool] = None  # 勾选 icon 是否为多选样式checkbox， 默认为radio


class Chart(AmisNode):
    """Chart: https://echarts.apache.org/en/option.html#title"""

    type: str = "chart"  # specify the chart renderer
    className: Optional[str] = None  # The class name of the outer Dom
    body: SerializeAsAny[Optional[SchemaNode]] = None  # Content container
    api: Optional[API] = None  # Configuration item interface address
    source: Optional[dict] = None  # Get the variable value in the data chain as configuration through data mapping
    initFetch: Optional[bool] = None  # whether to request the interface when the component is initialized
    interval: Optional[int] = None  # refresh time (minimum 1000)
    config: Union[dict, str, None] = None  # Set the configuration item of eschars, when it is string, you can set
    # configuration items such as function
    style: Optional[dict] = None  # Set the style of the root element
    width: Optional[str] = None  # Set the width of the root element
    height: Optional[str] = None  # Set the height of the root element
    replaceChartOption: Optional[
        bool
    ] = None  # False # Does each update completely overwrite the configuration item or append it?
    trackExpression: Optional[str] = None  # Update the chart when the value of this expression changes


class Code(AmisNode):
    """Code highlighting"""

    type: str = "code"
    className: Optional[str] = None  # Outer CSS class name
    value: Optional[str] = None  # display color value
    name: Optional[str] = None  # In other components, when used as variable mapping
    language: Optional[str] = None  # The highlighted language used, the default is plaintext
    tabSize: Optional[int] = None  # 4 # Default tab size
    editorTheme: Optional[str] = None  # "'vs'" # theme, and 'vs-dark'
    wordWrap: Optional[str] = None  # "True" # whether to wrap


class Json(AmisNode):
    """JSON display component"""

    type: str = "json"  # "json" if in Table, Card and List; "static-json" if used for static display in Form
    className: Optional[str] = None  # Outer CSS class name
    value: Union[dict, str, None] = None  # json value, if it is string, it will be parsed automatically
    source: Optional[str] = None  # Get the value in the data chain through the data map
    placeholder: Optional[str] = None  # placeholder text
    levelExpand: Optional[int] = None  # 1 # Default expanded level
    jsonTheme: Optional[str] = None  # "twilight" # Theme, optional twilight and eighties
    mutable: Optional[bool] = None  # False # whether it can be modified
    displayDataTypes: Optional[bool] = None  # False # whether to display data types


class Link(AmisNode):
    """Link"""

    type: str = "link"  # "link" if used in Table, Card and List; "static-link" if used as static display in Form
    body: Optional[str] = None  # Text inside the tag
    href: Optional[str] = None  # link address
    blank: Optional[bool] = None  # whether to open in a new tab
    htmlTarget: Optional[str] = None  # The target of the a tag, which takes precedence over the blank attribute
    title: Optional[Optional[str]] = None  # the title of the a tag
    disabled: Optional[bool] = None  # disable hyperlinks
    icon: Optional[str] = None  # Hyperlink icon to enhance display
    rightIcon: Optional[str] = None  # right icon


class Log(AmisNode):
    """Real-time log"""

    type: str = "log"
    source: Optional[API] = None  # Support variables, which can be initially set to empty, so that it will not be loaded
    # initially, and will be loaded when the variable has a value
    height: Optional[int] = None  # 500 # Display area height
    className: Optional[str] = None  # Outer CSS class name
    autoScroll: Optional[bool] = None  # True # whether to scroll automatically
    placeholder: Optional[str] = None  # The text being loaded
    encoding: Optional[str] = None  # "utf-8" # The character encoding of the returned content


class Property(AmisNode):
    """Property sheet"""

    class Item(AmisNode):
        label: Optional[Template] = None  # attribute name
        content: Optional[Template] = None  # attribute value
        span: Optional[int] = None  # attribute values span several columns
        visibleOn: Optional[Expression] = None  # Display expression
        hiddenOn: Optional[Expression] = None  # hidden expression

    type: str = "property"
    className: Optional[str] = None  # The class name of the outer dom
    style: Optional[dict] = None  # The style of the outer dom
    labelStyle: Optional[dict] = None  # style of attribute name
    contentStyle: Optional[dict] = None  # style of attribute value
    column: Optional[int] = None  # 3 # several columns per row
    mode: Optional[str] = None  # 'table' # Display mode, currently only 'table' and 'simple'
    separator: Optional[str] = None  # ',' # Separator between attribute name and value in 'simple' mode
    source: Optional[Template] = None  # data source
    title: Optional[Optional[str]] = None  # title
    items: SerializeAsAny[Optional[List[Item]]] = None  # data items


class QRCode(AmisNode):
    """QR code"""

    type: str = "qr-code"  # Specify as QRCode renderer
    value: Template  # The text displayed after scanning the QR code, if you want to display a page, please enter the
    # full url (starting with "http://..." or "https://..."), templates are supported
    className: Optional[str] = None  # The class name of the outer Dom
    qrcodeClassName: Optional[str] = None  # QR code SVG class name
    codeSize: Optional[int] = None  # 128 # The width and height of the QR code
    backgroundColor: Optional[str] = None  # "#fff" # QR code background color
    foregroundColor: Optional[str] = None  # "#000" # QR code foreground color
    level: Optional[str] = None  # "L" # QR code complexity level, there are four types ('L' 'M' 'Q' 'H')


class Barcode(AmisNode):
    """Barcode"""

    class Options(AmisNode):
        format: BarcodeEnum = BarcodeEnum.auto  # The format of the barcode
        width: Optional[int] = None  # default 2 width of the barcode image
        height: Optional[int] = None  # default 100 height of the barcode image
        displayValue: Optional[bool] = None  # default True
        text: Optional[str] = None
        fontOptions: str = ""
        font: Optional[str] = None  # default "monospace"
        textAlign: Optional[str] = None  # default "center"
        textPosition: Optional[str] = None  # default "bottom"
        textMargin: Optional[int] = None  # default 2
        fontSize: Optional[int] = None  # default 20
        background: Optional[str] = None  # #ffffff CSS Color
        lineColor: Optional[str] = None  # #000000 CSS color
        margin: Optional[int] = None  # default 10
        marginTop: Optional[int] = None
        marginBottom: Optional[int] = None
        marginLeft: Optional[int] = None
        marginRight: Optional[int] = None
        flat: Optional[bool] = None  # default False, no guard bars if True

    type: str = "barcode"  # Specify as QRCode renderer
    value: Optional[str] = None  # The value of the barcode
    className: Optional[str] = None  # The class name of the outer Dom
    options: Optional[Options] = None


class Color(AmisNode):
    type: Literal["color", "static-color"] = "color"
    value: Optional[str] = None  # The value of the color CSS code
    className: Optional[str] = None  # The class name of the outer Dom
    defaultColor: Optional[str] = None  # "#ccc" default color value
    showValue: Optional[bool] = None  # default True, whether to display the color value on the right


class Progress(AmisNode):
    type: Literal["progress", "static-progress"] = "progress"
    mode: Optional[ProgressEnum] = None  # The type of progress "bar", optional
    value: Optional[Template] = None  # The value of the progress
    className: Optional[str] = None  # The class name of the outer Dom
    showLabel: Optional[bool] = None  # default True, whether to show progress text
    stripe: Optional[bool] = None  # default False
    animate: Optional[bool] = None  # default False
    map: Union[str, List[str], List[Dict], None] = None  # progress colormap, as dict = {value:number, color:string}
    # default ['bg-danger', 'bg-warning', 'bg-info', 'bg-success', 'bg-success']
    threshold: Union[Dict, List, None] = None  # default -,
    # {value: template , color?: template } | List[{value: template , color?: template }]
    showThresholdText: Optional[bool] = None  # default False, whether to display the threshold (scale) value
    valueTpl: Optional[str] = None  # default ${value}%, custom formatted content
    strokeWidth: Optional[int] = None  # default 10 by circle, 6 with dashboard
    gapDegree: Optional[int] = None  # default 75, angle of the missing corner of the instrument panel, the value can be 0 ~ 295
    gapPosition: Optional[str] = None  # default "bottom", Dashboard progress bar notch position, optional top bottom left right


class PaginationWrapper(AmisNode):
    type: str = "pagination-wrapper"
    showPageInput: Optional[bool] = None  # default False, whether to display the quick jump input box
    maxButtons: Optional[int] = None  # default 5, Maximum number of pagination buttons to display
    inputName: Optional[str] = None  # default 'items', input field name
    outputName: Optional[str] = None  # default 'items', output field name
    perPage: Optional[int] = None  # default 10, Display multiple pieces of data per page
    position: Literal["top", "none", "bottom"] = "top"  # Pagination display position, if it is configured as none,
    # you need to configure the pagination component in the content area, otherwise it will not be displayed
    body: SerializeAsAny[Optional[SchemaNode]] = None  # Display content


class Pagination(AmisNode):
    type: str = "pagination"
    mode: Literal["simple", "normal"] = "normal"  # The mini version/simple version only displays left and right arrows,
    # used with hasNext
    layout: Union[str, List[str], None] = None  # default 'pager', Adjust the paging structure layout by controlling
    # the order of the layout properties
    maxButtons: Optional[int] = None  # default 10, Display multiple pieces of data per page
    lastPage: Optional[int] = None  # lastPage will be recalculated when the total number of entries is set
    total: Optional[int] = None  # total number of pages
    activePage: Optional[int] = None  # default 1, current page number
    perPage: Optional[int] = None  # default 10, Display multiple pieces of data per page
    showPerPage: Optional[bool] = None  # default False, whether to display the perPage switcher layout
    perPageAvailable: Optional[List[int]] = None  # default [10, 20, 50, 100], how many lines can be displayed per page
    showPageInput: Optional[bool] = None  # default False, whether to display the quick jump input box layout
    disabled: Optional[bool] = None  # default False, is pagination disabled


class MatrixCheckboxes(FormItem):
    """Matrix type input box."""

    class RowItem(AmisNode):
        label: str

    class ColumnItem(AmisNode):
        label: str

    type: str = "matrix-checkboxes"
    columns: SerializeAsAny[Optional[List[ColumnItem]]] = None  # list of column items
    rows: SerializeAsAny[Optional[List[RowItem]]] = None  # list of row items
    rowLabel: Optional[str] = None  # row header description
    source: Optional[API] = None  # Api address, if the option group is not fixed.
    multiple: Optional[bool] = None  # default False, multiple choice
    singleSelectMode: Literal["false", "cell", "row", "column"] = "column"


class Wrapper(AmisNode):
    type: str = "wrapper"
    className: Optional[str] = None  # The class name of the outer Dom
    style: Union[str, dict, None] = None  # Custom style (inline style), highest priority
    body: SerializeAsAny[Optional[SchemaNode]] = None  # Display content
    size: Union[str, SizeEnum, None] = None  # Specify the wrapper size, support: xs, sm, md, lg


class WebComponent(AmisNode):
    type: str = "web-component"
    tag: Optional[str] = None  # The specific web-component tag used
    style: Union[str, dict, None] = None  # Custom style (inline style), highest priority
    body: SerializeAsAny[Optional[SchemaNode]] = None  # child node
    props: Optional[dict] = None  # attributes by their labels


class UUIDField(AmisNode):
    """Randomly generates an id that can be used to prevent repeated form submissions."""

    type: str = "uuid"
    name: Optional[str] = None  # The field name
    length: Optional[int] = None  # if set, generates short random numbers, if not set it generates a UUID


class SearchBox(AmisNode):
    type: str = "search-box"
    className: Optional[str] = None  # The class name of the outer Dom
    mini: Optional[bool] = None  # default False, whether it is in mini mode
    searchImediately: Optional[bool] = None  # default False, whether to search now


class Sparkline(AmisNode):
    type: str = "sparkline"
    width: Optional[int] = None  # width of the sparkline image
    height: Optional[int] = None  # height of the sparkline image
    value: Optional[List[Union[int, float]]] = None  #
    clickAction: SerializeAsAny[Optional[Action]] = None  # Action when clicked


class Tag(AmisNode):
    type: str = "tag"
    className: Optional[str] = None  # Custom CSS style class name
    displayMode: Literal["normal", "rounded", "status"] = "normal"  # Display mode
    closable: Optional[bool] = None  # default False, show close icon
    color: Optional[str] = None  # color theme or custom color value,
    # 'active' | 'inactive' | 'error' | 'success' | 'processing' | 'warning'
    label: Optional[str] = None  # default '-'
    icon: Optional[str] = None  # custom font icon
    style: Union[str, dict, None] = None  # Custom style (inline style), highest priority


class Video(AmisNode):
    """video"""

    type: str = "video"  # specify the video renderer
    className: Optional[str] = None  # The class name of the outer Dom
    src: Optional[str] = None  # video address
    isLive: Optional[bool] = None  # False # whether it is a live broadcast, it needs to be added when the video is live,
    # supports flv and hls formats
    videoType: Optional[str] = None  # Specify the live video format
    poster: Optional[str] = None  # Video cover address
    muted: Optional[bool] = None  # whether to mute
    autoPlay: Optional[bool] = None  # whether to play automatically
    rates: Optional[List[float]] = None  # Multiples in the format [1.0, 1.5, 2.0]


class Alert(AmisNode):
    """hint"""

    type: str = "alert"  # Specify as the alert renderer
    className: Optional[str] = None  # The class name of the outer Dom
    level: Optional[str] = None  # "info" # Level, can be: info, success, warning or danger
    body: SerializeAsAny[Optional[SchemaNode]] = None  # Display content
    showCloseButton: Optional[bool] = None  # False # whether to show the close button
    closeButtonClassName: Optional[str] = None  # CSS class name of the close button
    showIcon: Optional[bool] = None  # False # whether to show icon
    icon: Optional[str] = None  # custom icon
    iconClassName: Optional[str] = None  # CSS class name of icon


class Dialog(AmisNode):
    """Dialog"""

    type: str = "dialog"  # Specify as Dialog renderer
    title: SerializeAsAny[Optional[SchemaNode]] = None  # Popup layer title
    body: SerializeAsAny[Optional[SchemaNode]] = None  # Add content to the Dialog content area
    size: Union[str, SizeEnum, None] = None  # Specify the dialog size, support: xs, sm, md, lg, xl, full
    bodyClassName: Optional[str] = None  # "modal-body" # The style class name of the Dialog body area
    closeOnEsc: Optional[bool] = None  # False # whether to support pressing Esc to close Dialog
    showCloseButton: Optional[bool] = None  # True # whether to show the close button in the upper right corner
    showErrorMsg: Optional[bool] = None  # True # whether to display the error message in the lower left corner of the popup
    disabled: Optional[bool] = None  # False # If this property is set, the Dialog is read-only and has no submit operation.
    actions: SerializeAsAny[
        Optional[List[Action]]
    ] = None  # If you want to not display the bottom button, you can configure: [] "[Confirm]
    # and [Cancel]"
    data: Optional[dict] = None  # Support data mapping, if not set, it will inherit the data in the context of the trigger
    # button by default.
    showLoading: Optional[bool] = None  # True # 是否在弹框左下角显示 loading 动画


class Drawer(AmisNode):
    """drawer"""

    type: str = "drawer"  # "drawer" specifies the Drawer renderer
    title: SerializeAsAny[Optional[SchemaNode]] = None  # Popup layer title
    body: SerializeAsAny[Optional[SchemaNode]] = None  # Add content to the Drawer content area
    size: Union[str, SizeEnum, None] = None  # Specify Drawer size, support: xs, sm, md, lg
    position: Optional[str] = None  # 'left' # position
    bodyClassName: Optional[str] = None  # "modal-body" # The style class name of the Drawer body area
    closeOnEsc: Optional[bool] = None  # False # whether to support pressing Esc to close Drawer
    closeOnOutside: Optional[bool] = None  # False # whether to close the Drawer when clicking outside the content area
    overlay: Optional[bool] = None  # True # whether to display the overlay
    resizable: Optional[bool] = None  # False # whether the size of the Drawer can be changed by dragging and dropping
    actions: SerializeAsAny[
        Optional[List[Action]]
    ] = None  # Can not be set, there are only two buttons by default. "[Confirm] and [Cancel]"
    data: Optional[dict] = None  # Support data mapping, if not set, it will inherit the data in the context of the trigger
    # button by default.
    className: Optional[str] = None  # Drawer 最外层容器的样式类名
    headerClassName: Optional[str] = None  # Drawer 头部 区域的样式类名
    footerClassName: Optional[str] = None  # Drawer 页脚 区域的样式类名
    showCloseButton: bool = True  # 是否展示关闭按钮，当值为 false 时，默认开启 closeOnOutside
    width: Union[int, str] = "500px"  # 容器的宽度，在 position 为 left 或 right 时生效
    height: Union[int, str] = "500px"  # 容器的高度，在 position 为 top 或 bottom 时生效


class Iframe(AmisNode):
    """Iframe"""

    type: str = "iframe"  # Specify as iFrame renderer
    className: Optional[str] = None  # iFrame class name
    frameBorder: Optional[list] = None  # frameBorder
    style: Optional[dict] = None  # style object
    src: Optional[str] = None  # iframe address
    allow: Optional[str] = None  # allow configuration
    sandbox: Optional[str] = None  # sandbox configuration
    referrerpolicy: Optional[str] = None  # referrerpolicy configuration
    height: Union[int, str, None] = None  # "100%" # iframe height
    width: Union[int, str, None] = None  # "100%" # iframe width


class Spinner(AmisNode):
    """Loading"""

    type: str = "spinner"


class TableCRUD(CRUD, Table):
    """Form Table CRUD"""

    mode: str = "table"


class CardCRUD(CRUD, Cards):
    """Form Card CRUD"""

    mode: str = "cards"


class ListCRUD(CRUD, ListDisplay):
    """Form Card CRUD"""

    mode: str = "list"


class Avatar(AmisNode):
    """avatar"""

    type: str = "avatar"
    className: Optional[str] = None  # The class name of the outer dom
    fit: Optional[str] = None  # "cover" # Image zoom type
    src: Optional[str] = None  # Image address
    text: Optional[str] = None  # text
    icon: Optional[str] = None  # icon
    shape: Optional[str] = None  # "circle" # shape, can also be square
    size: Optional[int] = None  # 40 # size
    style: Optional[dict] = None  # The style of the outer dom


class Audio(AmisNode):
    """Audio"""

    type: str = "audio"  # specify the audio renderer
    className: Optional[str] = None  # The class name of the outer Dom
    inline: Optional[bool] = None  # True # whether it is inline mode
    src: Optional[str] = None  # audio address
    loop: Optional[bool] = None  # False # whether to loop playback
    autoPlay: Optional[bool] = None  # False # whether to play automatically
    rates: Optional[List[float]] = None  # "[]" # Configurable audio playback speed such as: [1.0, 1.5, 2.0]
    controls: Optional[List[str]] = None  # "['rates','play','time','process','volume']" # Internal module customization


class Status(AmisNode):
    """state"""

    type: str = "status"  # Specify as Status renderer
    className: Optional[str] = None  # The class name of the outer Dom
    placeholder: Optional[str] = None  # placeholder text
    map: Optional[dict] = None  # map icon
    labelMap: Optional[dict] = None  # map text


class Tasks(AmisNode):
    """Task operation collection"""

    class Item(AmisNode):
        label: Optional[str] = None  # task name
        key: Optional[str] = None  # Task key value, please distinguish it uniquely
        remark: Optional[str] = None  # Current task status, support html
        status: Optional[str] = None  # Task status: 0: Initial status, inoperable. 1: Ready, operational state. 2: In
        # progress, not over yet.
        # 3: There is an error, no retry. 4: Completed normally. 5: There is an error, and you can try again.

    type: str = "tasks"  # Specify as Tasks renderer
    className: Optional[str] = None  # The class name of the outer Dom
    tableClassName: Optional[str] = None  # class name of table Dom
    items: SerializeAsAny[Optional[List[Item]]] = None  # task list
    checkApi: Optional[API] = None  # Return the task list, please refer to items for the returned data.
    submitApi: Optional[API] = None  # API used for submitting tasks
    reSubmitApi: Optional[API] = None  # If the task fails and can be retried, this API will be used when submitting
    interval: Optional[int] = None  # 3000 # When there is a task in progress, it will be checked again at regular intervals,
    # and the time interval is configured through this, the default is 3s.
    taskNameLabel: Optional[str] = None  # "task name" # task name column description
    operationLabel: Optional[str] = None  # "Operation" # Operation column description
    statusLabel: Optional[str] = None  # "status" # description of status column
    remarkLabel: Optional[RemarkT] = None  # "Remark" # Remark column description
    btnText: Optional[str] = None  # "Online" # Action button text
    retryBtnText: Optional[str] = None  # "Retry" # Retry action button text
    btnClassName: Optional[str] = None  # "btn-sm btn-default" # Configure the container button className
    retryBtnClassName: Optional[str] = None  # "btn-sm btn-danger" # Configure container retry button className
    statusLabelMap: Optional[List[str]] = None  # Status display corresponding class name configuration
    # "["label-warning", "label-info", "label-success", "label-danger", "label-default", "label-danger"]"
    statusTextMap: Optional[List[str]] = None  # "["Not started", "Ready", "In progress", "Error", "Completed", "Error"]" #
    # Status display corresponding text display configuration


class Wizard(AmisNode):
    """Wizard"""

    class Step(AmisNode):
        title: Optional[Optional[str]] = None  # Step title
        mode: Optional[str] = None  # Display the default, the same as the mode in Form, choose: normal, horizontal or inline.
        horizontal: Optional[Horizontal] = None  # When in horizontal mode, it is used to control the ratio of left and right
        api: Optional[API] = None  # The current step saves the interface, which can be left unconfigured.
        initApi: Optional[API] = None  # The current step data initialization interface.
        initFetch: Optional[bool] = None  # whether the current step data initialization interface is initially fetched.
        initFetchOn: Optional[Expression] = None  # whether the current step data initialization interface is initially fetched
        # is determined by an expression.
        body: SerializeAsAny[
            Optional[List[FormItem]]
        ] = None  # The form item collection of the current step, please refer to FormItem.

    type: str = "wizard"  # Specify as Wizard component
    mode: Optional[str] = None  # "horizontal" # Display mode, choose: horizontal or vertical
    api: Optional[API] = None  # The interface saved in the last step.
    initApi: Optional[API] = None  # Initialize data interface
    initFetch: Optional[API] = None  # whether to fetch data initially.
    initFetchOn: Optional[Expression] = None  # whether to pull data initially, configure by expression
    actionPrevLabel: Optional[str] = None  # "Previous" # Previous button text
    actionNextLabel: Optional[str] = None  # "Next" # Next button text
    actionNextSaveLabel: Optional[str] = None  # "Save and Next" # Save and Next button text
    actionFinishLabel: Optional[str] = None  # "Finish" # Finish button text
    className: Optional[str] = None  # Outer CSS class name
    actionClassName: Optional[str] = None  # "btn-sm btn-default" # Button CSS class name
    reload: Optional[str] = None  # Refresh the target object after the operation. Please fill in the name value set by the
    # target component. If it is filled in window, the current page will be refreshed as a whole.
    redirect: Optional[Template] = None  # "3000" # Jump after the operation.
    target: Optional[str] = None  # "False" # You can submit data to other components instead of saving it yourself. Please
    # fill in the name value set by the target component,
    # If it is filled in as window, the data will be synchronized to the address bar, and the components that depend
    # on these data will be automatically refreshed.
    steps: Optional[List[Step]] = None  # Array, configure step information
    startStep: Optional[int] = None  # "1" # Start default value, starting from the first step. Templates can be supported,
    # but only when the component is created, the template is rendered and the current number of steps is set. When
    # the component is refreshed later,
    # The current step will not change according to startStep


class AmisRender(AmisNode):
    """Amis render"""

    type: str = "amis"  # Specify as amis renderer
    schema_: SerializeAsAny[SchemaNode] = Field(None, alias="schema")  # amis schema
    props: Optional[dict] = None  # amis props


PageSchema.update_forward_refs()
ActionType.Dialog.update_forward_refs()
ActionType.Drawer.update_forward_refs()
TableCRUD.update_forward_refs()
Form.update_forward_refs()
Tpl.update_forward_refs()
InputText.update_forward_refs()
InputNumber.update_forward_refs()
Picker.update_forward_refs()
