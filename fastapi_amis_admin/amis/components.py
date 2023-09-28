"""Detailed document reading address: https://baidu.gitee.io/amis/zh-CN/components"""
import os
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import Field
from typing_extensions import Literal

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
    className: str = None  # Outer CSS class name
    icon: str = None  # icon name, support fontawesome v4 or use url
    vendor: str = None  # icon vendor, icon supports fontawesome v4 by default, if you want to support fontawesome v5
    # and v6, please set vendor to an empty string.


class Remark(AmisNode):
    """mark"""

    type: str = "remark"  # remark
    className: str = None  # Outer CSS class name
    content: str = None  # prompt text
    placement: str = None  # Popup position
    trigger: str = None  # Trigger condition['hover','focus']
    icon: str = None  # "fa fa-question-circle" # icon


class Badge(AmisNode):
    """Subscript"""

    mode: str = "dot"  # Corner type, can be dot/text/ribbon
    text: Union[int, str] = None  # Corner text, supports strings and numbers, invalid when mode='dot'
    size: int = None  # Angular size
    level: str = None  # The level of the corner label, which can be info/success/warning/danger, after setting the
    # background color of the corner label is different
    overflowCount: int = None  # 99 # Set the capped number value
    position: str = None  # "top-right" # Corner position, can be top-right/top-left/bottom-right/bottom-left
    offset: int = None  # The position of the corner label, the priority is greater than the position, when the
    # offset is set, the position is positioned as the top-right reference number[top, left]
    className: str = None  # The class name of the outer dom
    animation: bool = None  # whether the corner icon displays animation
    style: dict = None  # Custom style for corner labels
    visibleOn: Expression = None  # Controls the display and hiding of corner labels


class Page(AmisNode):
    """page"""

    __default_template_path__: str = f"{BASE_DIR}/templates/page.html"

    type: str = "page"  # Specify as Page component
    title: SchemaNode = None  # page title
    subTitle: SchemaNode = None  # Page subtitle
    remark: RemarkT = None  # A prompt icon will appear near the title, and the content will be prompted when the
    # mouse is placed on it.
    aside: SchemaNode = None  # Add content to the sidebar area of the page
    asideResizor: bool = None  # whether the width of the sidebar area of the page can be adjusted
    asideMinWidth: int = None  # The minimum width of the sidebar area of the page
    asideMaxWidth: int = None  # The maximum width of the sidebar area of the page
    toolbar: SchemaNode = None  # Add content to the upper right corner of the page. It should be noted that when
    # there is a title, the area is in the upper right corner, and when there is no title, the area is at the top
    body: SchemaNode = None  # Add content to the content area of the page
    className: str = None  # Outer dom class name
    cssVars: dict = None  # Custom CSS variables, please refer to styles
    css: str = None  # Custom CSS styles, please refer to used theme styles
    mobileCSS: str = None  # Custom mobile CSS styles, please refer to used theme styles
    toolbarClassName: str = None  # "v-middle wrapper text-right bg-light bb" # Toolbar dom class name
    bodyClassName: str = None  # "wrapper" # Body dom class name
    asideClassName: str = None  # "w page-aside-region bg-auto" # Aside dom class name
    headerClassName: str = None  # "bg-light bb wrapper" # Header area dom class name
    initApi: API = None  # The api that Page uses to get initial data. The returned data can be used at the entire
    # page level.
    initFetch: bool = None  # True # whether to start pulling initApi
    initFetchOn: Expression = None  # whether to start pulling initApi, configure by expression
    interval: int = None  # refresh time (minimum 1000)
    silentPolling: bool = None  # False # whether to show the loading animation when the configuration is refreshed
    stopAutoRefreshWhen: Expression = None  # Configure the conditions for stopping refresh through expressions
    regions: List[str] = None

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
    className: str = None  # The class name of the outer Dom
    lineStyle: str = None  # Split line style, supports dashed and solid


class Flex(AmisNode):
    """layout"""

    type: str = "flex"  # Specify as Flex renderer
    className: str = None  # css class name
    justify: str = None  # "start", "flex-start", "center", "end", "flex-end", "space-around", "space-between",
    # "space-evenly"
    alignItems: str = None  # "stretch", "start", "flex-start", "flex-end", "end", "center", "baseline"
    style: dict = None  # custom style
    items: List[SchemaNode] = None  #


class Grid(AmisNode):
    """Horizontal layout"""

    class Column(AmisNode):
        """Column configuration"""

        xs: int = None  # "auto" # Width ratio: 1 - 12
        ClassName: str = None  # column class name
        sm: int = None  # "auto" # Width ratio: 1 - 12
        md: int = None  # "auto" # Width ratio: 1 - 12
        lg: int = None  # "auto" # Width ratio: 1 - 12
        valign: str = None  # 'top'|'middle'|'bottom'|'between = None # Vertical alignment of the current column content
        body: List[SchemaNode] = None  #

    type: str = "grid"  # Specify as Grid renderer
    className: str = None  # The class name of the outer Dom
    gap: str = None  # 'xs'|'sm'|'base'|'none'|'md'|'lg = None # Horizontal gap
    valign: str = None  # 'top'|'middle'|'bottom'|'between = None # Vertical alignment
    align: str = None  # 'left'|'right'|'between'|'center = None # Horizontal alignment
    columns: List[SchemaNode] = None  #


class Panel(AmisNode):
    """panel"""

    type: str = "panel"  # Specify as the Panel renderer
    className: str = None  # "panel-default" # The class name of the outer Dom
    headerClassName: str = None  # "panel-heading" # The class name of the header area
    footerClassName: str = None  # "panel-footer bg-light lter wrapper" # The class name of the footer area
    actionsClassName: str = None  # "panel-footer" # The class name of the actions area
    bodyClassName: str = None  # "panel-body" # The class name of the body area
    title: SchemaNode = None  # title
    header: SchemaNode = None  # header container
    body: SchemaNode = None  # Content container
    footer: SchemaNode = None  # bottom container
    affixFooter: bool = None  # whether to fix the bottom container
    actions: List["Action"] = None  # Button area


class Tabs(AmisNode):
    """Tab"""

    class Item(AmisNode):
        title: str = None  # Tab title
        icon: Union[str, Icon] = None  # Icon for Tab
        tab: SchemaNode = None  # Content area
        hash: str = None  # After setting, it will correspond to the hash of the url
        reload: bool = None  # After setting, the content will be re-rendered every time, which is useful for
        # re-pulling crud
        unmountOnExit: bool = None  # Each exit will destroy the current tab bar content
        className: str = None  # "bg-white bl br bb wrapper-md" # Tab area style
        iconPosition: str = None  # "left" # Tab's icon position left / right
        closable: bool = None  # False # whether to support deletion, the priority is higher than the closable of the
        # component
        disabled: bool = None  # False # whether to disable

    type: str = "tabs"  # Specify as Tabs renderer
    className: str = None  # The class name of the outer Dom
    mode: str = None  # Display mode, the value can be line, card, radio, vertical, chrome, simple, strong, tiled,
    # sidebar
    tabsClassName: str = None  # Class name of Tabs Dom
    tabs: List[Item] = None  # tabs content
    source: str = None  # tabs associated data, tabs can be generated repeatedly after association
    toolbar: SchemaNode = None  # toolbar in tabs
    toolbarClassName: str = None  # The class name of the toolbar in the tabs
    mountOnEnter: bool = None  # False # Render only when the tab is clicked
    unmountOnExit: bool = None  # False # Destroyed when switching tabs
    scrollable: bool = None  # False # whether the navigation supports content overflow scrolling, this property is
    # not supported in vertical and chrome modes; chrome mode defaults to compress tags (property discarded)
    tabsMode: TabsModeEnum = None  # Display mode, the value can be line, card, radio, vertical, chrome, simple,
    # strong, tiled, sidebar
    addable: bool = None  # False # whether to support adding
    addBtnText: str = None  # "Add" # Add button text
    closable: bool = None  # False # whether to support delete
    draggable: bool = None  # False # whether to support draggable
    showTip: bool = None  # False # whether to support tips
    showTipClassName: str = None  # "'' " # Tip class
    editable: bool = None  # False # whether to edit the tag name
    sidePosition: str = None  # "left" # In sidebar mode, the position of the tab bar is left / right


class Portlet(Tabs):
    """Portal column"""

    class Item(Tabs.Item):
        toolbar: SchemaNode = None  # The toolbar in tabs, which changes with tab switching

    type: str = "portlet"  # specify as portlet renderer
    contentClassName: str = None  # Class name of Tabs content Dom
    tabs: List[Item] = None  # tabs content
    style: Union[str, dict] = None  # custom style
    description: Template = None  # Information on the right side of the title
    hideHeader: bool = None  # False # hide the header
    divider: bool = None  # False # remove divider


class Horizontal(AmisNode):
    left: int = None  # The width ratio of the left label
    right: int = None  # The width ratio of the right controller.
    offset: int = None  # When the label is not set, the offset of the right controller


class Action(AmisNode):
    """Behavior button"""

    type: str = "button"  # Specify as the Page renderer. button action
    actionType: str = None  # [Required] This is the core configuration of the action to specify the action type of
    # the action. Support: ajax, link, url, drawer, dialog, confirm, cancel, prev, next, copy, close.
    label: str = None  # Button text. Available ${xxx} values.
    level: LevelEnum = None  # Button style, support: link, primary, secondary, info, success, warning, danger,
    # light, dark, default.
    size: str = None  # Button size, support: xs, sm, md, lg.
    icon: str = None  # Set the icon, eg fa fa-plus.
    iconClassName: str = None  # Add a class name to the icon.
    rightIcon: str = None  # Set the icon to the right of the button text, eg fa fa-plus.
    rightIconClassName: str = None  # Add a class name to the right icon.
    active: bool = None  # whether the button is highlighted.
    activeLevel: str = None  # The style when the button is highlighted, the configuration supports the same level.
    activeClassName: str = None  # Add a class name to the button highlight. "is-active"
    block: bool = None  # Use display:"block" to display the button.
    confirmText: Template = None  # When set, the action will ask the user before starting. Available ${xxx} values.
    reload: str = None  # Specify the name of the target component that needs to be refreshed after this operation (
    # the name value of the component, configured by yourself), please separate multiple ones with , signs.
    tooltip: str = None  # This text pops up when the mouse stays, and the object type can also be configured: the
    # fields are title and content. Available ${xxx} values.
    disabledTip: str = None  # The text will pop up when the mouse stays after it is disabled. You can also configure
    # the object type: the fields are title and content. Available ${xxx} values.
    tooltipPlacement: str = None  # If tooltip or disabledTip is configured, specify the location of the prompt
    # information, and you can configure top, bottom, left, and right.
    close: Union[bool, str] = None  # When the action is configured in the actions of the dialog or drawer, configure
    # it to true to close the current dialog or drawer after the operation. When the value is a string and is the
    # name of the ancestor layer popup, the ancestor popup will be closed.
    required: List[str] = None  # Configure an array of strings, specifying that the form items with the specified
    # field name must pass validation before performing operations in the form primary:bool=None
    onClick: str = None  # The custom click event defines the click event through onClick in the form of a string,
    # which will be converted into a JavaScript function
    componentId: str = None  # target component ID
    args: Union[dict, str] = None  # event parameters
    script: str = None  # Customize JS script code, any action can be performed by calling doAction in the code,
    # and event action intervention can be realized through the event object event


class ActionType:
    """Behavior button type"""

    class Ajax(Action):
        actionType: str = "ajax"  # Show a popup after clicking
        api: API = None  # Request address, refer to api format description.
        redirect: Template = None  # Specify the path to redirect to after the current request ends, which can be
        # valued by ${xxx}.
        feedback: "Dialog" = None  # If it is of ajax type, when ajax returns to normal, a dialog can be popped up
        # for other interactions. The returned data can be used in this dialog. For the format, please refer to Dialog
        messages: dict = None  # success: a message will be displayed after the ajax operation is successful. It can
        # be left unspecified. If it is not specified, the api return shall prevail. failed: Ajax operation failure
        # message.

    class Dialog(Action):
        actionType: str = "dialog"  # Show a popup when clicked
        dialog: Union["Dialog", "Service", SchemaNode]  # Specify the content of the pop-up box, the format can refer to Dialog
        nextCondition: bool = None  # Can be used to set the condition of the next data, the default is true.

    class Drawer(Action):
        actionType: str = "drawer"  # Show a sidebar when clicked
        drawer: Union["Drawer", "Service", SchemaNode]  # Specify the content of the popup box, the format can refer to Drawer

    class Copy(Action):
        actionType: str = "copy"  # Copy a piece of content to the clipboard
        content: Template  # Specify the copied content. Available ${xxx} values.
        copyFormat: str = None  # You can set the copy format through copyFormat, the default is text text/html

    class Url(Action):
        """Jump directly"""

        actionType: str = "url"  # Jump directly
        url: str  # When the button is clicked, the specified page will be opened. Available ${xxx} values.
        blank: bool = None  # false If true will open in a new tab page.

    class Link(Action):
        """Single page jump"""

        actionType: str = "link"  # Single page jump
        link: str  # is used to specify the jump address. Unlike url, this is a single-page jump method, which will
        # not render the browser. Please specify the page in the amis platform. Available ${xxx} values.

    class Toast(Action):
        """Toast light"""

        class ToastItem(AmisNode):
            title: Union[str, SchemaNode] = None  # Toast Item Title
            body: Union[str, SchemaNode] = None  # Toast Item Content
            level: str = None  # default 'info', Display icon, optional 'info', 'success', 'error', 'warning'
            position: str = None  # default 'top-center', display position,
            # 'top-right', 'top-center', 'top-left', 'bottom-center', 'bottom-left', 'bottom-right', 'center'
            closeButton: bool = None  # default False, whether to show the close button
            showIcon: bool = None  # default True, whether to display the icon
            timeout: int = None  # default 5000

        actionType: str = "toast"  # Single page jump
        items: List[ToastItem] = None  # List of ToastItems
        position: str = None  # display position,
        # available 'top-right', 'top-center', 'top-left', 'bottom-center', 'bottom-left', 'bottom-right', 'center'
        closeButton: bool = None  # default False, whether to display the close button, not in mobile
        showIcon: bool = None  # default = True, whether to display the icon
        timeout: int = None  # default 5000


class PageSchema(AmisNode):
    """Page configuration"""

    label: str = None  # Menu name.
    icon: str = "fa fa-flash"  # Menu icon, for example: 'fa fa-file'. For detailed icon reference:
    # http://www.fontawesome.com.cn/faicons/
    url: str = None  # The page routing path, when the route hits the path, the current page is enabled. When the
    # path does not start with /, the parent path is concatenated. For example: the path of the parent is folder,
    # and pageA is configured at this time, then this page will be hit only when the page address is /folder/pageA.
    # When the path starts with / such as: /crud/list, the parent path will not be spliced. In addition, routes with
    # parameters such as /crud/view/:id are supported. This value can be obtained from the page through ${params.id}.
    schema_: Union[Page, "Iframe"] = Field(None, alias="schema")  # The configuration of the page, please go to the
    # page page for specific configuration
    schemaApi: API = None  # If you want to pull through the interface, please configure. The return path is
    # json>data. Only one of schema and schemaApi can be selected.
    link: str = None  # If you want to configure an external link menu, you only need to configure link.
    redirect: str = None  # Jump, when hitting the current page, jump to the target page.
    rewrite: str = None  # Change to rendering pages of other paths, the page address will not be modified in this way.
    isDefaultPage: Union[bool, str] = None  # Useful when you need a custom 404 page, don't have multiple such pages,
    # because only the first one will be useful.
    visible: Union[bool, str] = None  # Some pages may not want to appear in the menu, you can configure it to false, and the
    # route with parameters does not need to be configured, it is directly invisible.
    className: str = None  # Menu class name.
    children: List["PageSchema"] = None  # Submenu
    sort: int = None  # Unofficial attribute. sort
    tabsMode: TabsModeEnum = None  # Unofficial attribute. Display mode, the value can be line, card, radio, vertical,

    # chrome, simple, strong, tiled, sidebar, collapse

    def as_page_body(self, group_extra: Dict[str, Any] = None, item_extra: Dict[str, Any] = None):
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
    api: API = None  # The page configuration interface, if you want to pull the page configuration remotely,
    # please configure it. Return to the configuration path json>data>pages, please refer to the pages property for
    # the specific format.
    brandName: str = None  # app name
    logo: str = None  # Support image address, or svg.
    className: str = None  # css class name
    header: str = None  # header
    asideBefore: str = None  # The front area on the page menu.
    asideAfter: str = None  # The front area under the page menu.
    footer: str = None  # The page.
    pages: List[PageSchema] = None  # Array<page configuration> specific page configuration.
    # Usually in an array, the first layer of the array is a group, generally you only need to configure the label set,
    # if you don't want to group, don't configure it directly, the real page should be configured in the second
    # layer, that is, in the children of the first layer.


class ButtonGroup(AmisNode):
    """Button group"""

    type: str = "button-group"
    buttons: List[Action]  # Behavior button group
    className: str = None  # The class name of the outer Dom
    vertical: bool = None  # whether to use vertical mode
    tiled: bool = None  # whether to use tile mode
    btnLevel: LevelEnum = None  # button style
    btnActiveLevel: LevelEnum = None  # Active button style


class Custom(AmisNode):
    """Custom Components"""

    type: str = "custom"
    id: str = None  # node id
    name: str = None  # node name
    className: str = None  # node class
    inline: bool = False  # use div tag by default, if true use span tag
    html: str = None  # initialize node html
    onMount: str = None  # "Function" # Function called after node initialization
    onUpdate: str = None  # "Function" # The function called when the data is updated
    onUnmount: str = None  # "Function" # The function called when the node is destroyed


class Service(AmisNode):
    """Functional container"""

    type: str = "service"  # designate as service renderer
    name: str = None  # node name
    data: dict = None  #
    className: str = None  # The class name of the outer Dom
    body: SchemaNode = None  # Content container
    api: API = None  # Initialize data domain interface address
    ws: str = None  # WebScocket address
    dataProvider: str = None  # Data acquisition function
    initFetch: bool = None  # whether to pull by default
    schemaApi: API = None  # Used to get the remote schema interface address
    initFetchSchema: bool = None  # whether to pull Schema by default
    messages: dict = None  # Message prompt override, the default message reads the toast prompt text returned by the
    # interface, but it can be overridden here.
    # messages.fetchSuccess: str = None # Toast prompt text when the interface request is successful
    # messages.fetchFailed: str = "Initialization failed" # Toast prompt text when interface request fails
    interval: int = None  # Polling interval (minimum 3000)
    silentPolling: bool = None  # False # whether to display the loading animation during polling
    stopAutoRefreshWhen: Expression = None  # Configure the condition to stop polling


class Nav(AmisNode):
    """navigation"""

    class Link(AmisNode):
        label: str = None  # name
        to: Template = None  # Link address
        target: str = None  # "Link relationship" #
        icon: str = None  # icon
        children: List["Link"] = None  # child links
        unfolded: bool = None  # whether to unfold initially
        active: bool = None  # whether to highlight
        activeOn: Expression = None  # whether to highlight the condition, leaving it blank will automatically
        # analyze the link address
        defer: bool = None  # mark whether it is a lazy add-in
        deferApi: API = None  # Can not be configured, if the configuration priority is higher

    type: str = "nav"  # specify as Nav renderer
    className: str = None  # The class name of the outer Dom
    stacked: bool = True  # Set to false to display in the form of tabs
    source: API = None  # Navigation can be created dynamically via variable or API interface
    deferApi: API = None  # The interface used to delay loading option details. It can be left unconfigured,
    # and the public source interface cannot be configured.
    itemActions: SchemaNode = None  # More operations related configuration
    draggable: bool = None  # whether to support drag and drop sorting
    dragOnSameLevel: bool = None  # Only allow dragging within the same level
    saveOrderApi: API = None  # save order api
    itemBadge: Badge = None  # Badge
    links: list = None  # link collection


class AnchorNav(AmisNode):
    """Anchor Navigation"""

    class Link(AmisNode):
        label: str = None  # name
        title: str = None  # area title
        href: str = None  # Region ID
        body: SchemaNode = None  # area content area
        className: str = None  # "bg-white bl br bb wrapper-md" # Area member style

    type: str = "anchor-nav"  # Specify as AnchorNav renderer
    className: str = None  # The class name of the outer Dom
    linkClassName: str = None  # Class name of the navigation Dom
    sectionClassName: str = None  # The class name of the anchor area Dom
    links: list = None  # links content
    direction: str = None  # "vertical" # You can configure whether the navigation is displayed horizontally or
    # vertically. The corresponding configuration items are: vertical, horizontal
    active: str = None  # The area that needs to be located


class ButtonToolbar(AmisNode):
    """Button Toolbar"""

    type: str = "button-toolbar"
    buttons: List[Action]  # Behavior button group


class Validation(BaseAmisModel):
    isEmail: bool = None  # Must be Email.
    isUrl: bool = None  # Must be a Url.
    isNumeric: bool = None  # Must be a number.
    isAlpha: bool = None  # Must be an alpha.
    isAlphanumeric: bool = None  # Must be a letter or a number.
    isInt: bool = None  # Must be an integer.
    isFloat: bool = None  # Must be a float.
    isLength: int = None  # whether the length is exactly equal to the set value.
    minLength: int = None  # Minimum length.
    maxLength: int = None  # Maximum length.
    maximum: int = None  # Maximum value.
    minimum: int = None  # Minimum value.
    equals: str = None  # The current value must be exactly equal to xxx.
    equalsField: str = None  # The current value must be the same as the xxx variable value.
    isJson: bool = None  # Is it a valid Json string.
    isUrlPath: bool = None  # is the url path.
    isPhoneNumber: bool = None  # Is it a legal phone number
    isTelNumber: bool = None  # Is it a valid phone number
    isZipcode: bool = None  # whether it is a zip code
    isId: bool = None  # whether it is an ID number, no verification is done
    matchRegexp: str = None  # Must hit a certain regexp. /foo/


class FormItem(AmisNode):
    """Form item common"""

    class AutoFill(BaseAmisModel):
        showSuggestion: bool = None  # true refers to input, false automatically fills
        api: API = None  # Automatically populate the interface/filter the CRUD request configuration with reference to entry
        silent: bool = None  # Whether to display a data format error message. The default value is true
        fillMappinng: SchemaNode = None  # Auto-fill/reference input data mapping configuration, key-value pair form,
        # value support variable acquisition and expression
        trigger: str = None  # ShowSuggestion to true, the reference input support way of trigger,
        # currently supports change "value change" | focus "form focus"
        mode: str = None  # When showSuggestion is true, refer to the popOver mode: dialog, drawer, popOver
        labelField: str = None  # When showSuggestion is true, set the popup dialog,drawer,popOver picker's labelField
        position: str = None  # If showSuggestion is true, set the popOver location as shown in the input mode Popover
        size: str = None  # If showSuggestion is true, set the value as shown in dialog mode
        columns: List["TableColumn"] = None  # When showSuggestion is true, the data display column configuration
        filter: SchemaNode = None  # When showSuggestion is true, data query filter condition

    type: str = "input-text"  # Specify the form item type
    className: str = None  # The outermost class name of the form
    inputClassName: str = None  # Form controller class name
    labelClassName: str = None  # class name of label
    name: str = None  # Field name, specifying the key when the form item is submitted
    label: Union[bool, Template] = None  # form item label template or false
    labelAlign: str = None  # "right" # Form item label alignment, default right alignment, only effective when mode is
    labelRemark: RemarkT = None  # Form item label description
    description: Template = None  # Form item description
    placeholder: str = None  # Form item description
    inline: bool = None  # whether it is inline mode
    submitOnChange: bool = None  # whether to submit the current form when the value of the form item changes.
    disabled: bool = None  # whether the current form item is disabled
    disabledOn: Expression = None  # The condition for whether the current form item is disabled
    visible: bool = None  # whether the current form item is disabled or not
    visibleOn: Expression = None  # The condition for whether the current form item is disabled
    required: bool = None  # whether it is required.
    requiredOn: Expression = None  # Use an expression to configure whether the current form item is required.
    validations: Union[Validation, Expression] = None  # Validation of the form item value format, multiple settings
    # are supported, and multiple rules are separated by commas.
    validateApi: API = None  # Form validation interface
    copyable: Union[bool, dict] = None  # whether to copy boolean or {icon: string, content:string}
    autoFill: AutoFill = None  # Data entry configuration, automatic filling or reference entry
    static: bool = None  # 2.4.0 Whether the current form item is static display,
    staticOn: Expression = None  # 2.4.0 The condition for whether the current form item is static display
    # the current support static display of the form item
    staticClassName: str = None  # 2.4.0 The class name for static display
    staticLabelClassName: str = None  # 2.4.0 The class name of the Label for static display
    staticInputClassName: str = None  # 2.4.0 The class name of value when static display
    staticSchema: Union[str, list] = None  # SchemaNode


class ButtonGroupSelect(FormItem):
    """Button group select"""

    type: str = "button-group-select"
    vertical: bool = None  # Default False, use vertical mode
    tiled: bool = None  # Default False, use tile mode
    btnLevel: LevelEnum = LevelEnum.default  # button style
    btnActiveLevel: LevelEnum = LevelEnum.default  # Check button style
    options: OptionsNode = None  # option group
    source: API = None  # dynamic group
    multiple: bool = None  # Default False, multiple choice
    labelField: str = None  # Default "label"
    valueField: str = None  # Default "value"
    joinValues: bool = None  # Default True
    extractValue: bool = None  # Default False
    autoFill: dict = None  # autofill


class ListSelect(FormItem):
    """List select, allows images"""

    type: str = "list-select"
    options: OptionsNode = None  # option group
    source: API = None  # dynamic group
    multiple: bool = None  # Default False, multiple choice
    labelField: str = None  # Default "label"
    valueField: str = None  # Default "value"
    joinValues: bool = None  # Default True
    extractValue: bool = None  # Default False
    autoFill: dict = None  # autofill
    listClassName: str = None  # Supports configuring the css class name of the list div. for example:flex justify-between


class Form(AmisNode):
    """Form"""

    class Messages(AmisNode):
        fetchSuccess: str = None  # Prompt when fetch is successful
        fetchFailed: str = None  # Prompt when fetch fails
        saveSuccess: str = None  # Prompt when saving is successful
        saveFailed: str = None  # Prompt when saving fails

    type: str = "form"  # "form" specifies the Form renderer
    name: str = None  # After setting a name, it is convenient for other components to communicate with it
    mode: DisplayModeEnum = None  # Form display mode, can be: normal, horizontal or inline
    horizontal: Horizontal = None  # Useful when mode is horizontal,
    # Used to control label {"left": "col-sm-2", "right": "col-sm-10", "offset": "col-sm-offset-2"}
    title: Optional[str] = None  # Title of the Form
    submitText: Optional[str] = None  # "Submit" # Default submit button name, if it is set to empty, the default
    # button can be removed.
    className: str = None  # The class name of the outer Dom
    body: List[Union[FormItem, SchemaNode]] = None  # Form item collection
    actions: List["Action"] = None  # Form submit button, the member is Action
    actionsClassName: str = None  # class name of actions
    messages: Messages = None  # The message prompts to be overridden. The default message reads the message returned
    # by the API, but it can be overridden here.
    wrapWithPanel: bool = None  # whether to wrap the Form with panel, if set to false, actions will be invalid.
    panelClassName: str = None  # The class name of the outer panel
    api: API = None  # The api that Form uses to save data.
    initApi: API = None  # The api that Form uses to get initial data.
    rules: list = None  # Form combination validation rules Array<{rule:string;message:string}>
    interval: int = None  # refresh time (minimum 3000)
    silentPolling: bool = None  # False # whether to show the loading animation when the configuration is refreshed
    stopAutoRefreshWhen: str = None  # Configure the condition for stopping refresh by expression
    initAsyncApi: API = None  # The api that Form uses to obtain initial data, which is different from initApi,
    # will keep polling and request this interface until the returned finished attribute is true.
    initFetch: bool = None  # After initApi or initAsyncApi is set, the request will be sent by default, and if it is
    # set to false, the interface will not be requested at the beginning
    initFetchOn: str = None  # Use expression to configure
    initFinishedField: Optional[str] = None  # After setting initAsyncApi, by default, the data.finished of the
    # returned data will be used to judge whether it is completed.
    # Can also be set to other xxx, it will be obtained from data.xxx
    initCheckInterval: int = None  # After setting initAsyncApi, the default pull interval
    asyncApi: API = None  # After setting this property, after the form is submitted and sent to save the interface,
    # it will continue to poll and request the interface, and it will not end until the returned finished property is
    # true.
    checkInterval: int = None  # The time interval for polling requests, the default is 3 seconds. Setting asyncApi
    # is valid
    finishedField: Optional[str] = None  # Set this property if the field name that decides to end is not finished,
    # such as is_success
    submitOnChange: bool = None  # Form modification is submitted
    submitOnInit: bool = None  # Submit once initially
    resetAfterSubmit: bool = None  # whether to reset the form after submitting
    primaryField: str = None  # Set the primary key id. When set, it will only carry this data when checking whether
    # the form is completed (asyncApi).
    target: str = None  # The default form submission itself will save the data by sending the api, but you can also
    # set the name value of another form, or another CRUD model name value. If the target target is a Form,
    # the target Form will trigger initApi again, and the api can get the current form data. If the target is a CRUD
    # model, the target model will re-trigger the search with the current Form data as the parameter. When the target
    # is window, the data of the current form will be attached to the page address.
    redirect: str = None  # After setting this attribute, after the Form is saved successfully, it will automatically
    # jump to the specified page. Support relative addresses, and absolute addresses (relative to the group).
    reload: str = None  # Refresh the target object after the operation. Please fill in the name value set by the
    # target component. If it is filled in window, the current page will be refreshed as a whole.
    autoFocus: bool = None  # whether to auto focus.
    canAccessSuperData: bool = None  # Specify whether the upper layer data can be automatically obtained and mapped
    # to the form item
    persistData: str = None  # Specify a unique key to configure whether to enable local caching for the current form
    clearPersistDataAfterSubmit: bool = None  # Specify whether to clear the local cache after the form is submitted
    # successfully
    preventEnterSubmit: bool = None  # Disable EnterSubmit form submission
    trimValues: bool = None  # trim each value of the current form item
    promptPageLeave: bool = None  # The form has not been saved, whether to confirm with a pop-up box before leaving
    # the page.
    columnCount: int = None  # The form item is displayed as several columns
    debug: bool = None
    inheritData: bool = None  # true # The default form is to create its own data field in the form of a data link,
    # and only the data in this data field will be sent when the form is submitted. If you want to share the
    # upper layer data field, you can set this attribute to false, so that the data in the upper layer data field
    # does not need to be sent in the form with hidden fields or explicit mapping.
    static: bool = None  # false # 2.4.0. The entire form is displayed statically.
    # For details, please refer to the:https://aisuda.bce.baidu.com/amis/examples/form/switchDisplay.
    staticClassName: str = None  # 2.4.0. The name of the class used when the form is statically displayed
    labelAlign: Literal["right", "left"] = None  # "right"  # 表单项标签对齐方式，默认右对齐，仅在 mode为horizontal 时生效
    labelWidth: Union[int, str] = None  # 表单项标签自定义宽度
    persistDataKeys: List[str] = None  # 指指定只有哪些 key 缓存
    closeDialogOnSubmit: bool = None  # 提交的时候是否关闭弹窗


class InputSubForm(FormItem):
    """Subform"""

    type: str = "input-sub-form"
    multiple: bool = None  # False # whether it is multiple selection mode
    labelField: str = None  # When this field exists in the value, the button name will be displayed using the value
    # of this field.
    btnLabel: str = None  # "Settings" # Default button name
    minLength: int = None  # 0 # Limit the minimum number.
    maxLength: int = None  # 0 # Limit the maximum number.
    draggable: bool = None  # whether it can be draggable and sorted
    addable: bool = None  # whether it can be added
    removable: bool = None  # whether it can be removed
    addButtonClassName: str = None  # "``" # Add button CSS class name
    itemClassName: str = None  # "``" # Value element CSS class name
    itemsClassName: str = None  # "``" # Value wrapping element CSS class name
    form: Form = None  # Subform configuration, same as Form
    addButtonText: str = None  # "``" # Customize the text of the new item
    showErrorMsg: bool = None  # True # whether to display the error message in the lower left corner


class Button(FormItem):
    """Button"""

    type: str = "button"
    className: str = None  # Specify the add button class name
    url: str = None  # Click the jump address, specify the behavior of this attribute button is consistent with the
    # a link
    size: str = None  # Set button size 'xs'|'sm'|'md'|'lg'
    actionType: str = None  # Set the button type 'button'|'reset'|'submit'| 'clear'| 'url'
    level: LevelEnum = None  # Set button style 'link'|'primary'|'enhance'|'secondary'|'info'|'success'|'warning
    # '|'danger'|'light'| 'dark'|'default'
    tooltip: Union[str, dict] = None  # Bubble tip content TooltipObject
    tooltipPlacement: str = None  # Balloon positioner 'top'|'right'|'bottom'|'left'
    tooltipTrigger: str = None  # trigger tootip 'hover'|'focus'
    disabled: bool = None  # button disabled state
    block: bool = None  # Option to adjust button width to its parent width
    loading: bool = None  # Show button loading effect
    loadingOn: str = None  # Display button loading expression


class InputFormula(FormItem):
    """Input Formula Editor"""

    type: str = "input-formula"
    title: str = None  # title
    header: str = None  # Editor header title, if not set, the form item labelfield is used by default
    evalMode: bool = None  # default True, Expression mode or template mode (False),
    # template mode requires the expression to be written between ${and }.
    variables: List[dict] = None  # Available variables, {label: string; value: string; children?: any[]; tag?: string}
    variableMode: Literal["tabs", "tree", "list"] = "list"  # Can be configured as tabs or tree ,
    # defaults to a list, which supports grouping.
    inputMode: Literal["button", "input-button", "input-group"] = None  # Display mode of the control
    icon: str = None  # fa icon
    btnLabel: str = None  # The button text, which inputModetakesbutton
    level: LevelEnum = LevelEnum.default  # button stlye
    allowInput: bool = None  # default -, Whether the input box can be entered
    btnSize: Literal["xs", "sm", "md", "lg"] = None  # button size
    borderMode: Literal["full", "half", "none"] = None  # Input box border mode
    placeholder: str = None  # input box placeholder
    className: str = None  # Control outer CSS style class name
    variableClassName: str = None  # Variable panel CSS style class name
    functionClassName: str = None  # Function panel CSS style class name
    mixedMode: bool = None  # default False, if True it supports values in both text and formula formats


class InputArray(FormItem):
    """Array input box"""

    type: str = "input-array"
    items: FormItem = None  # Configure single item form type
    addable: bool = None  # whether it can be added.
    removable: bool = None  # whether it can be removed
    draggable: bool = None  # False # whether drag sorting is possible, it should be noted that when drag sorting is
    # enabled, there will be an additional $id field
    draggableTip: str = None  # Draggable prompt text, the default is: "Order can be adjusted by dragging the [Swap]
    # button in each row"
    addButtonText: str = None  # "Add" # Add button text
    minLength: int = None  # Limit the minimum length
    maxLength: int = None  # limit max length
    scaffold: Any = None  # 新增成员时的默认值，一般根据items的数据类型指定需要的默认值


class Hidden(FormItem):
    """Hidden fields"""

    type: str = "hidden"


class Checkbox(FormItem):
    """Check box"""

    type: str = "checkbox"
    option: str = None  # option description
    trueValue: Any = None  # identifies the true value
    falseValue: Any = None  # identifies a false value
    optionType: Literal["default", "button"] = None  # 设置 option 类型


class Radios(FormItem):
    """Single box"""

    type: str = "radios"
    options: List[Union[dict, str]] = None  # Option group
    source: API = None  # Dynamic option group
    labelField: bool = None  # "label" # option label field
    valueField: bool = None  # "value" # option value field
    columnsCount: int = None  # 1 # options are displayed in several columns, default is one column
    inline: bool = None  # True # whether to display as one line
    selectFirst: bool = None  # False # whether to select the first one by default
    autoFill: dict = None  # autofill


class ChartRadios(Radios):
    """Single box"""

    type: str = "chart-radios"
    config: dict = None  # echart chart configuration
    showTooltipOnHighlight: bool = None  # False # whether to show tooltip when highlighted
    chartValueField: str = None  # "value" # Chart value field name


class Checkboxes(FormItem):
    """Checkbox"""

    type: str = "checkboxes"
    options: OptionsNode = None  # option group
    source: API = None  # Dynamic option group
    delimiter: str = None  # "," # splicer
    labelField: str = None  # "label" # option label field
    valueField: str = None  # "value" # option value field
    joinValues: bool = None  # True # join values
    extractValue: bool = None  # False # extract value
    columnsCount: int = None  # 1 # options are displayed in several columns, default is one column
    checkAll: bool = None  # False # whether to support select all
    inline: bool = None  # True # whether to display as one line
    defaultCheckAll: bool = None  # False # whether to check all by default
    creatable: bool = None  # False # New option
    createBtnLabel: str = None  # "Add option" # Add option
    addControls: List[FormItem] = None  # Customize new form items
    addApi: API = None  # Configure the new option interface
    editable: bool = None  # False # edit options
    editControls: List[FormItem] = None  # Customize edit form items
    editApi: API = None  # Configure editing options interface
    removable: bool = None  # False # remove option
    deleteApi: API = None  # Configure delete option interface
    optionType: Literal["default", "button"] = None  # "default"  # 按钮模式
    itemClassName: str = None  # 选项样式类名
    labelClassName: str = None  # 选项标签样式类名


class InputCity(FormItem):
    """City selector"""

    type: str = "input-city"
    allowCity: bool = None  # True # Allow city selection
    allowDistrict: bool = None  # True # Allow region selection
    searchable: bool = None  # False # whether to display the search box
    extractValue: bool = None  # True# whether to extract the value, if set to false, the value format will become an
    # object, including code, province, city and district text information.


class InputColor(FormItem):
    """Color picker"""

    type: str = "input-color"
    format: str = None  # "hex" # Please choose hex, hls, rgb or rgba.
    presetColors: List[str] = None  # "Selector preset color value" # The default color at the bottom of the selector,
    # if the array is empty, the default color will not be displayed
    allowCustomColor: bool = None  # True # When false, only colors can be selected, use presetColors to set the
    # color selection range
    clearable: bool = None  # "label" # whether to display the clear button
    resetValue: str = None  # "" # After clearing, the form item value is adjusted to this value


class Combo(FormItem):
    """combination"""

    type: str = "combo"
    formClassName: str = None  # The class name of a single group of form items
    addButtonClassName: str = None  # Add button CSS class name
    items: List[FormItem] = None  # Form items displayed in combination
    # items[x].columnClassName: str = None # The class name of the column, which can be used to configure the column
    # width. The default is evenly distributed. items[x].unique: bool = None # Set whether the current column value
    # is unique, that is, repeated selection is not allowed.
    noBorder: bool = False  # whether to display a border for a single group of form items
    scaffold: dict = {}  # initial value for a single set of form items
    multiple: bool = False  # whether to select multiple
    multiLine: bool = False  # The default is to display a row horizontally, after setting it will be displayed
    # vertically
    minLength: int = None  # Minimum number of added bars
    maxLength: int = None  # The maximum number of bars to add
    flat: bool = False  # whether to flatten the result (remove the name), only valid when the length of items is 1
    # and multiple is true.
    joinValues: bool = True  # The default is true When flattening is enabled, whether to send it to the backend in
    # the form of a delimiter, otherwise it is in the form of an array.
    delimiter: str = None  # "False" # What delimiter to use when flattening is on and joinValues is true.
    addable: bool = False  # whether it can be added
    addButtonText: str = None  # "Add" # Add button text
    removable: bool = False  # whether it can be removed
    deleteApi: API = None  # If configured, an api will be sent before deletion, and the deletion will be completed
    # after the request is successful
    deleteConfirmText: str = None  # "Confirm to delete?" # It only takes effect when deleteApi is configured! Used
    # for user confirmation when deleting
    draggable: bool = False  # whether drag sorting is possible, it should be noted that when drag sorting is
    # enabled, there will be an additional $id field
    draggableTip: str = None  # "Order can be adjusted by dragging the [Exchange] button in each row" # Draggable
    # prompt text
    subFormMode: str = None  # "normal" # optional normal, horizontal, inline
    placeholder: str = None  # "``" # Displayed when there is no member.
    canAccessSuperData: bool = False  # Specify whether the upper layer data can be automatically obtained and mapped
    # to the form item
    conditions: dict = None  # The form of an array contains the rendering types of all conditions. The test in a
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
    subFormHorizontal: dict = None  # The horizontal configuration of the sub-form item, which is the same as the
    # horizontal configuration of the form item.


class ConditionBuilder(FormItem):
    """Combined conditions"""

    class Field(AmisNode):
        type: str = "text"  # The field configuration is configured as "text"
        label: str = None  # Field name.
        placeholder: str = None  # placeholder
        operators: List[str] = None  # If not so many, you can configure overrides.
        # Default is ['equal','not_equal','is_empty','is_not_empty','like','not_like','starts_with','ends_with']
        defaultOp: str = None  # defaults to "equal"

    class Text(Field):
        """text"""

    class Number(Field):
        """number"""

        type: str = "number"
        minimum: float = None  # minimum value
        maximum: float = None  # maximum value
        step: float = None  # step size

    class Date(Field):
        """date"""

        type: str = "date"
        defaultValue: str = None  # default value
        format: str = None  # Default "YYYY-MM-DD" value format
        inputFormat: str = None  # Default "YYYY-MM-DD" display date format.

    class Datetime(Date):
        """Date Time"""

        type: str = "datetime"
        timeFormat: str = None  # The default "HH:mm" time format determines which input boxes are available.

    class Time(Date):
        """time"""

        type: str = "datetime"

    class Select(Field):
        """Drop down to select"""

        type: str = "select"
        options: OptionsNode = None  # options list, Array<{label: string, value: any}>
        source: API = None  # Dynamic options, please configure api.
        searchable: bool = None  # whether it can be searched
        autoComplete: API = None  # Automatically prompt for completion, each time new content is entered,
        # the interface will be called, and the update options will be returned according to the interface.

    type: str = "condition-builder"
    fields: List[Field] = None  # It is an array type, each member represents an optional field, supports multiple
    # layers, configuration example
    className: str = None  # Outer dom class name
    fieldClassName: str = None  # The class name of the input field
    source: str = None  # Pull configuration items remotely


class Editor(FormItem):
    """Code Editor"""

    type: str = "editor"
    language: str = None  # "javascript" # The language highlighted by the editor, which can be obtained through the
    # ${xxx} variable
    # bat, c, coffeescript, cpp, csharp, css, dockerfile, fsharp, go, handlebars, html, ini, java,
    # javascript, json, less, lua, markdown, msdax, objective-c, php, plaintext, postiats, powershell,
    # pug, python, r, razor, ruby, sb, scss, shell, sol, sql, swift, typescript, vb, xml, yaml
    size: str = None  # "md" # Editor height, the value can be md, lg, xl, xxl
    allowFullscreen: bool = None  # False # whether to display the full screen mode switch
    options: dict = None  # Other configurations of the monaco editor, such as whether to display line numbers, etc.,
    # please refer to here, but readOnly cannot be set, read-only mode needs to use disabled: true


class DiffEditor(FormItem):
    """Code Editor"""

    type: str = "diff-editor"
    language: str = None  # "javascript" # The language highlighted by the editor, which can be obtained through the
    # ${xxx} variable
    # bat, c, coffeescript, cpp, csharp, css, dockerfile, fsharp, go, handlebars, html, ini, java,
    # javascript, json, less, lua, markdown, msdax, objective-c, php, plaintext, postiats, powershell,
    # pug, python, r, razor, ruby, sb, scss, shell, sol, sql, swift, typescript, vb, xml, yaml
    diffValue: Template = None  # the diff value or reference to other data entry like '${value1}'


class Formula(AmisNode):
    """Formula for fields, linked by 'name'"""

    type: str = "formula"
    name: str = None  # The formula result will be applied to the variable (name) specified here.
    formula: Expression = None  # the formula itself
    condition: Expression = None  # condition for the formula
    initSet: bool = None  # Default True, whether to set at initialization
    autoSet: bool = None  # Default True, Observe the formula result, if the calculation result changes,
    # it will be automatically applied to the variable
    id: bool = None  # Default True, Define a name. When a button's target is specified, it will trigger a formula.


class DropDownButton(AmisNode):
    """Formula for fields, linked by 'name'"""

    type: str = "dropdown-button"
    label: str = None  # button text
    className: str = None  # Outer CSS class name
    btnClassName: str = None  # Button CSS class name
    menuClassName: str = None  # Dropdown menu CSS class name
    block: bool = None  # Default False, block style
    size: Literal["xs", "sm", "md", "lg"] = None  # size, support 'xs', 'sm', 'md','lg'
    align: Literal["left", "right"] = None  # location align
    buttons: List[Button] = []  # List of buttons
    iconOnly: bool = None  # default False, show only icon
    defaultIsOpened: bool = None  # default False, whether to open by default
    closeOnOutside: bool = None  # default True, Click whether to collapse the outer area
    closeOnClick: bool = None  # default False, automatically close dropdown menu after button click
    trigger: TriggerEnum = TriggerEnum.click  # trigger method
    hideCaret: bool = None  # default False, Hide drop down icon


class EachLoop(AmisNode):
    """Each loop renderer"""

    type: str = "each"
    value: list = []  # value for the loop
    name: str = None  # Data field name
    source: str = None  # Data mapping source
    items: dict = None  # {"type": "tpl", "tpl": "< span ..."}
    placeholder: str = None  # placeholder text when valuevalue does not exist or is an empty array


class GridNav(AmisNode):
    """Grid navigation
    menu navigation, does not support the configuration of the initialization interface to initialize the data field,
    so you need to work with similar to Service, Form or CRUD, with the configuration of the interface to initialize
    the data field components, or manually initialize the data field, and then through the source property,
    to obtain the data in the data chain to complete the menu display.
    """

    class OptionsItem(AmisNode):
        icon: str = None  # default '', list item icon
        text: str = None  # default '', list item text
        badge: Badge = None  # Bade Schema, list item badge
        link: str = None  # default '', Internal page path or external URL address, takes precedence over clickAction
        blank: bool = None  # default False, Whether a new page is opened, valid when link is url
        clickAction: Action = None  # ActionSchema

    type: str = "grid-nav"
    className: str = None  # outer dom classname
    itemClassName: str = None  # item custom css classname
    value: List = None  # array of images
    source: str = None  # data source
    square: bool = None  # default False, whether to fix list items to be square
    center: bool = None  # default False, whether to center the content of the list item
    border: bool = None  # default False, whether to show the list item border
    gutter: int = None  # default -, px, the spacing between list items
    reverse: bool = None  # default False, whether to swap the position of the icon and text
    iconRatio: int = None  # default 60, Icon width ratio, in %
    direction: Literal["horizontal", "vertical"] = "vertical"  # The direction in which the list items are arranged
    columnNum: int = None  # default 4,
    options: List[OptionsItem] = None  # the option items


class CollapseGroup(AmisNode):
    """Grid navigation
    menu navigation, does not support the configuration of the initialization interface to initialize the data field,
    so you need to work with similar to Service, Form or CRUD, with the configuration of the interface to initialize
    the data field components, or manually initialize the data field, and then through the source property,
    to obtain the data in the data chain to complete the menu display.
    """

    class CollapseItem(AmisNode):
        type: str = "collapse"
        disabled: bool = None  # default False
        collapsed: bool = None  # default True
        key: Union[int, str] = None  # default -, logo
        header: Union[str, SchemaNode] = None  # default -, title
        body: Union[str, SchemaNode] = None  # default -, content

    type: str = "collapse-group"
    activeKey: Union[str, int, List[Union[int, str]]] = None  # Initialize the key to activate the panel
    disabled: bool = None  # default False
    accordion: bool = None  # default False, accordion mode
    expandIcon: SchemaNode = None  # Custom toggle icon
    expandIconPosition: Literal["left", "right"] = "left"  # icon position
    body: List[Union[CollapseItem, SchemaNode]] = None  # group content


class Markdown(AmisNode):
    """Markdown rendering"""

    type: str = "markdown"
    name: str = None  # Field name, specifying the key when the form item is submitted
    value: Union[int, str] = None  # field value
    className: str = None  # The outermost class name of the form
    src: API = None  # external address
    options: dict = None  # html, whether to support html tags, default false;
    # linkify, whether to automatically identify the link, the default value is true; breaks, whether the carriage
    # return is a newline, the default value is false


class OfficeViewer(AmisNode):
    """Office Viewer：https://aisuda.bce.baidu.com/amis/zh-CN/components/office-viewer"""

    type: str = "office-viewer"
    src: API = None  # Document address
    loading: bool = None  # Whether to display the loading icon
    enableVar: bool = None  # Whether to enable variable replacement function
    wordOptions: dict = None  # Word rendering configuration


class InputFile(FormItem):
    """File Upload"""

    type: str = "input-file"
    receiver: API = None  # Upload file interface
    accept: str = None  # "text/plain" # Only plain text is supported by default. To support other types,
    # please configure this property as the file suffix .xxx
    asBase64: bool = None  # False # Assign the file to the current component in the form of base64
    asBlob: bool = None  # False # Assign the file to the current component in binary form
    maxSize: int = None  # There is no limit by default, when set, the file size larger than this value will not be
    # allowed to upload. unit is B
    maxLength: int = None  # There is no limit by default. When set, only the specified number of files can be
    # uploaded at a time.
    multiple: bool = None  # False # whether to select multiple.
    joinValues: bool = None  # True # join values
    extractValue: bool = None  # False # extract value
    delimiter: str = None  # "," # splicer
    autoUpload: bool = None  # True # No selection will automatically start uploading
    hideUploadButton: bool = None  # False # hide the upload button
    stateTextMap: dict = None  # Upload state text Default: {init: '', pending: 'Waiting to upload', uploading:
    # 'Uploading', error: 'Upload error', uploaded: 'Uploaded',ready: ''}
    fileField: str = None  # "file" # You can ignore this attribute if you don't want to store it yourself.
    nameField: str = None  # "name" # Which field is returned by the interface to identify the file name
    valueField: str = None  # "value" # The value of the file is identified by that field.
    urlField: str = None  # "url" # The field name of the file download address.
    btnLabel: str = None  # The text of the upload button
    downloadUrl: Union[bool, str] = None  # Version 1.1.6 supports post:http://xxx.com/${value}
    # When the file path is displayed by default, it will support direct download. It can support adding a prefix
    # such as: http://xx.dom/filename= . If you don't want this, you can set the current configuration item to false.
    useChunk: bool = None  # The server where amis is located limits the file upload size to no more than 10M,
    # so when amis selects a large file, it will automatically change to the chunked upload mode.
    chunkSize: int = None  # 5 * 1024 * 1024 # chunk size
    startChunkApi: API = None  # startChunkApi
    chunkApi: API = None  # chunkApi
    finishChunkApi: API = None  # finishChunkApi
    autoFill: Dict[str, str] = None  # After the upload is successful, the value returned by the upload interface can
    # be filled into a form item by configuring autoFill (not supported under non-form)


class InputExcel(FormItem):
    """Parse Excel"""

    type: str = "input-excel"
    allSheets: bool = None  # False # whether to parse all sheets
    parseMode: str = None  # 'array' or 'object' parsing mode
    includeEmpty: bool = None  # True # whether to include empty values
    plainText: bool = None  # True # whether to parse as plain text


class InputTable(FormItem):
    """sheet"""

    type: str = "input-table"  # Specify as Table renderer
    showIndex: bool = None  # False # Show index
    perPage: int = None  # Set how many pieces of data are displayed on one page. 10
    addable: bool = None  # False # whether to add a line
    editable: bool = None  # False # whether editable
    removable: bool = None  # False # whether it can be removed
    showAddBtn: bool = None  # True # whether to show the add button
    addApi: API = None  # API submitted when adding
    updateApi: API = None  # API submitted when modified
    deleteApi: API = None  # API submitted when deleting
    addBtnLabel: Union[bool, Template] = None  # Add button name
    addBtnIcon: Union[bool, str] = None  # "plus" # Add button icon
    copyBtnLabel: Union[bool, Template] = None  # Copy button text
    copyBtnIcon: Union[bool, str] = None  # "copy" # Copy button icon
    editBtnLabel: Union[bool, Template] = None  # "" # Edit button name
    editBtnIcon: Union[bool, str] = None  # "pencil" # edit button icon
    deleteBtnLabel: Union[bool, Template] = None  # "" # delete button name
    deleteBtnIcon: Union[bool, str] = None  # "minus" # delete button icon
    confirmBtnLabel: Union[bool, Template] = None  # "" # Confirm edit button name
    confirmBtnIcon: str = None  # "check" # Confirm edit button icon
    cancelBtnLabel: Union[bool, Template] = None  # "" # Cancel edit button name
    cancelBtnIcon: str = None  # "times" # Cancel edit button icon
    needConfirm: bool = None  # True # whether to confirm the operation, it can be used to control the operation
    # interaction of the control table
    canAccessSuperData: bool = None  # False # whether you can access the parent data, that is, the same level data
    # in the form, usually need to be used with strictMode
    strictMode: bool = None  # True # For performance, the default value of other form items will not update the
    # current table. Sometimes, in order to obtain other form item fields synchronously, you need to enable this.
    columns: list = None  # "[]" # Column information
    # columns[x].quickEdit: boolean|object = None # Use with editable as true columns[x].quickEditOnUpdate:
    # boolean|object = None # Edit configuration that can be used to distinguish between new mode and update mode


class InputGroup(FormItem):
    """Combination of input boxes"""

    type: str = "input-group"
    className: str = None  # CSS class name
    body: List[FormItem] = None  # Form item collection


class Group(InputGroup):
    """Form item group"""

    type: str = "group"
    mode: DisplayModeEnum = None  # Display the default, the same as the mode in Form
    gap: str = None  # Gap between form items, optional: xs, sm, normal
    direction: str = None  # "horizontal" # Can be configured to display horizontally or vertically. The
    # corresponding configuration items are: vertical, horizontal


class InputImage(FormItem):
    """upload picture"""

    class CropInfo(BaseAmisModel):
        aspectRatio: float = None  # Crop ratio. Floating point, the default is 1, which is 1:1. If you want to set
        # 16:9, please set 1.7777777777777777, which is 16/9. .
        rotatable: bool = None  # False # whether to rotate when cropping
        scalable: bool = None  # False # whether it can be scaled when cropping
        viewMode: int = None  # 1 # View mode when cropping, 0 is unlimited

    class Limit(BaseAmisModel):
        width: int = None  # Limit image width.
        height: int = None  # Limit image height.
        minWidth: int = None  # Limit image minimum width.
        minHeight: int = None  # Limit image minimum height.
        maxWidth: int = None  # Limit the maximum width of the image.
        maxHeight: int = None  # Limit the maximum height of the image.
        aspectRatio: float = None  # Limit the aspect ratio of the image, the format is a floating-point number,
        # the default is 1, which is 1:1, If you want to set 16:9, please set 1.7777777777777777 which is 16/9. If
        # you don't want to limit the ratio, set an empty string.

    type: str = "input-image"
    receiver: API = None  # Upload file interface
    accept: str = None  # ".jpeg,.jpg,.png,.gif" # Supported picture types and formats, please configure this
    # property as picture suffix, such as .jpg,.png
    maxSize: int = None  # There is no limit by default, when set, the file size larger than this value will not be
    # allowed to upload. unit is B
    maxLength: int = None  # There is no limit by default. When set, only the specified number of files can be
    # uploaded at a time.
    multiple: bool = None  # False # whether to select multiple.
    joinValues: bool = None  # True # join values
    extractValue: bool = None  # False # extract value
    delimiter: str = None  # "," # splicer
    autoUpload: bool = None  # True # No selection will automatically start uploading
    hideUploadButton: bool = None  # False # hide the upload button
    fileField: str = None  # "file" # You can ignore this attribute if you don't want to store it yourself.
    crop: Union[bool, CropInfo] = None  # Used to set whether to support cropping.
    cropFormat: str = None  # "image/png" # crop file format
    cropQuality: int = None  # 1 # The quality of the crop file format, for jpeg/webp, between 0 and 1
    limit: Limit = None  # Limit the size of the image, beyond which it will not be allowed to upload.
    frameImage: str = None  # Default placeholder image address
    fixedSize: bool = None  # whether to enable fixed size, if enabled, set fixedSizeClassName at the same time
    fixedSizeClassName: str = None  # When the fixed size is turned on, the display size is controlled according to this value.
    # For example, h-30, that is, the height of the picture frame is h-30, AMIS will automatically set the zoom ratio
    # to the width of the position occupied by the default image, and the final uploaded image will be scaled
    # accordingly according to this size.
    autoFill: Dict[str, str] = None  # After the upload is successful, the value returned by the upload interface can
    # be filled into a form item by configuring autoFill (not supported under non-form)
    initAutoFill: bool = None  # False  # 表单反显时是否执行 autoFill
    uploadBtnText: Union[str, SchemaNode] = None  # 上传按钮文案。支持tpl、schema形式配置。
    dropCrop: bool = None  # True  # 图片上传后是否进入裁剪模式
    initCrop: bool = None  # False  # 图片选择器初始化后是否立即进入裁剪模式


class LocationPicker(FormItem):
    """Location"""

    type: str = "location-picker"
    vendor: str = "baidu"  # Map vendor, currently only Baidu map is implemented
    ak: str = ...  # ak # registered address of Baidu map: http://lbsyun.baidu.com/
    clearable: bool = None  # False # whether the input box can be cleared
    placeholder: str = None  # "Please select a location" # Default prompt
    coordinatesType: str = None  # "bd09" # Default is Baidu coordinates, can be set to 'gcj02'


class InputNumber(FormItem):
    """Number input box"""

    type: str = "input-number"
    min: Union[int, Template] = None  # minimum value
    max: Union[int, Template] = None  # maximum value
    step: int = None  # step size
    precision: int = None  # Precision, i.e. a few decimal places
    showSteps: bool = None  # True # whether to show up and down click buttons
    prefix: str = None  # prefix
    suffix: str = None  # suffix
    kilobitSeparator: bool = None  # Kilobit Separator


class Picker(FormItem):
    """List selector"""

    type: str = "picker"  # List pick, similar in function to Select, but it can display more complex information.
    size: Union[str, SizeEnum] = None  # Supports: xs, sm, md, lg, xl, full
    options: OptionsNode = None  # option group
    source: API = None  # Dynamic option group
    multiple: bool = None  # whether it is multiple choice.
    delimiter: bool = None  # False # splicer
    labelField: str = None  # "label" # option label field
    valueField: str = None  # "value" # option value field
    joinValues: bool = None  # True # join values
    extractValue: bool = None  # False # extract value
    autoFill: dict = None  # autofill
    modalMode: Literal["dialog", "drawer"] = None  # "dialog" # Set dialog or drawer to configure the popup mode.
    pickerSchema: Union["CRUD", SchemaNode] = None  # "{mode: 'list', listItem: {title: '${label}'}}"
    # That is to use the rendering of the List type to display the list information. More configuration reference CRUD
    embed: bool = None  # False # whether to use embedded mode


class Switch(FormItem):
    """switch"""

    type: str = "switch"
    option: str = None  # option description
    onText: str = None  # Text when it is turned on
    offText: str = None  # text when off
    trueValue: Any = None  # "True" # identifies the true value
    falseValue: Any = None  # "false" # identifies a false value


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
    options: Union[List[str], List[dict]] = None  # Option group
    source: API = None  # Dynamic option group
    autoComplete: API = None  # autocomplete
    multiple: bool = None  # whether to select multiple
    delimiter: str = None  # Splice ","
    labelField: str = None  # option label field "label"
    valueField: str = None  # option value field "value"
    joinValues: bool = None  # True # join values
    extractValue: bool = None  # extract value
    addOn: SchemaNode = None  # Input box add-ons, such as with a prompt text, or with a submit button.
    trimContents: bool = None  # whether to remove leading and trailing blank text.
    creatable: bool = None  # whether it can be created, the default is yes, unless it is set to false, only the
    # value in the option can be selected
    clearable: bool = None  # whether it can be cleared
    resetValue: str = None  # Set the value given by this configuration item after clearing.
    prefix: str = None  # prefix
    suffix: str = None  # suffix
    showCounter: bool = None  # whether to show the counter
    minLength: int = None  # Limit the minimum number of words
    maxLength: int = None  # Limit the maximum number of characters


class InputPassword(InputText):
    """Password input box"""

    type: str = "input-password"


class InputRichText(FormItem):
    """Rich Text Editor"""

    type: str = "input-rich-text"
    saveAsUbb: bool = None  # whether to save in ubb format
    receiver: API = None  # '' # Default image save API
    videoReceiver: API = None  # '' # Default video save API
    size: str = None  # The size of the box, which can be set to md or lg
    options: dict = None  # Need to refer to tinymce or froala documentation
    buttons: List[str] = None  # froala dedicated, configure the displayed buttons, tinymce can set the toolbar
    # string through the previous options
    vendor: str = None  # "vendor": "froala" , configure to use froala editor


class InputRating(FormItem):
    """Input Rating"""

    type: str = "input-rating"
    half: bool = None  # default False, whether to use half star selection
    count: int = None  # default 5, amount of total stars
    readOnly: bool = None  # default False, is it read only
    allowClear: bool = None  # default True, allow clearing after another click
    colors: Union[str, dict] = None  # default {'2': '#abadb1', '3': '#787b81', '5': '#ffa900' }, The color in which
    # the stars are displayed. If a string is passed in, there is only one color.
    # If an dict is passed in, each level can be customized.
    # The key name is the limit value of the segment, and the key value is the corresponding class name.
    inactiveColor: str = None  # default #e7e7e8, color of unselected stars
    texts: dict = None  # default -, The tooltip text when the star is selected.
    # key name is the level of the segment, and the value is the corresponding text
    textPosition: Literal["right", "left"] = "right"  # position of Tooltip
    char: str = None  # default '*', custom character
    charClassNme: str = None  # default -, custom char class name
    textClassName: str = None  # default -, custom text class name


class InputRange(FormItem):
    """Input Range"""

    type: str = "input-range"
    min: int = None  # default 0, min value
    max: int = None  # default 100, max value
    step: int = None  # default 1, step size
    showSteps: bool = None  # default False, show step size
    parts: Union[int, List[int]] = None  # default 1, Number of blocks to split
    marks: Union[str, dict] = None  # Tick Marks, Support Custom Styles, Set Percentages
    # { [number | string]: ReactNode }or{ [number | string]: { style: CSSProperties, label: ReactNode } }
    tooltipVisible: bool = None  # default False, whether to show slider labels
    tooltipPlacement: PlacementEnum = None  # defualt 'top', tooltip placement 'top'|'right'|'bottom'|'left'
    multiple: bool = None  # default False, support selection range
    joinValues: bool = None  # default True, show step size
    delimiter: str = None  # dfeault ',', value delimiter
    unit: str = None  # unit
    clearable: bool = None  # default False, whether the precondition can be cleared : showInputValid when enabled
    showInput: bool = None  # default False, whether to display the input box


class Timeline(AmisNode):
    """Timeline"""

    class TimelineItem(AmisNode):
        time: str  # Node Time
        title: Union[str, SchemaNode] = None  # Node Title
        detail: str = None  # Node detailed description (collapsed)
        detailCollapsedText: str = None  # default 'Expand'
        detailExpandedText: str = None  # default 'Collapse'
        color: Union[str, LevelEnum] = None  # default #DADBDD, Timeline node color
        icon: str = None  # Icon name, support fontawesome v4 or use url (priority is higher than color)

    type: str = "timeline"
    items: List[TimelineItem] = None  # default [], Nodes
    source: API = None  # Data source, you can obtain current variables through data mapping, or configure API objects
    mode: Literal["left", "right", "alternate"] = "right"  # Position of the text relative to the timeline,
    # only supported when direction=vertical
    direction: Literal["vertical", "horizontal"] = "vertical"  # Direction of the Timeline
    reverse: bool = None  # default False, Reverse chronological order


class Steps(AmisNode):
    """Steps Bar"""

    class StepItem(AmisNode):
        title: Union[str, SchemaNode] = None  # Title
        subTitle: Union[str, SchemaNode] = None  # Sub Heading
        description: Union[str, SchemaNode] = None  # Detail Description
        value: str = None  # Step Value
        icon: str = None  # Icon name, support fontawesome v4 or use url (priority is higher than color)
        className: str = None  # Custom CSS class name

    type: str = "steps"
    steps: List[StepItem] = None  # default [], List of Steps
    source: API = None  # Data source, you can obtain current variables through data mapping, or configure API objects
    name: str = None  # Associated context variable
    value: Union[int, str, None] = None  # default -, Set the default value, expressions are not supported
    status: Union[StepStatusEnum, dict] = None  # default -, State of the steps
    className: str = None  # Custom CSS class name
    mode: Literal["vertical", "horizontal"] = "horizontal"  # Specifies the step bar direction.
    labelPlacement: Literal["vertical", "horizontal"] = "horizontal"  # Specify the label placement position.
    # The default is to place it horizontally to the right of the icon, and optional (vertical) below the icon.
    progressDot: bool = None  # Default False, show dotted step bar


class TooltipWrapper(AmisNode):
    type: str = "tooltip-wrapper"
    className: str = None  # Content area class name
    tooltipClassName: str = None  # Text prompt floating layer class name
    style: Union[str, dict] = None  # Custom style (inline style), highest priority
    tooltipStyle: Union[str, dict] = None  # floating layer custom style
    body: SchemaNode = None  # Content container
    wrapperComponent: str = None  # "div" | "span"
    inline: bool = None  # default False, whether the content area is displayed inline
    rootClose: bool = None  # default True, whether to click the non-content area to close the prompt
    mouseEnterDelay: int = None  # default 0, Floating layer delay display time, in ms
    mouseLeaveDelay: int = None  # default 300, Floating layer delay hiding time, in ms
    trigger: Union[TriggerEnum, List[TriggerEnum]] = None  # default 'hover', Floating layer trigger mode, support array writing
    # "hover" | "click" | "focus" | List["hover", "click", "focus"]
    disabled: bool = None  # default False, whether to disable overlay prompts
    enterable: bool = None  # default True, whether the mouse can move into the floating layer
    showArrow: bool = None  # default True, whether to display the overlay pointing arrow
    offset: Tuple[int, int] = None  # default [0, 0], relative offset of the position of the text prompt, in px
    tooltipTheme: Literal["light", "dark"] = "light"  # default light, Theme style
    placement: PlacementEnum = PlacementEnum.top  # text prompts position of the floating layer
    content: str = None  # default '',  Text prompt content
    title: str = None  # default '', tooltip title


class InputTag(FormItem):
    """Input Tag"""

    type: str = "input-tag"
    options: List[Union[str, dict]] = None  # default option group
    optionsTip: List[Union[str, dict]] = None  # default "Your most recent tags", option hint
    source: API = None  # default 	Dynamic option group
    delimiter: str = None  # default False, delimiter option
    labelField: str = None  # default "label", option label field
    valueField: str = None  # default "value", option value field
    joinValues: bool = None  # default True, Splice value
    extractValue: bool = None  # default False, extract value
    clearable: bool = None  # default False, whether to show a delete icon on the right when there is a value.
    resetValue: str = None  # default "", Set the value given by this configuration item after deletion.
    max: int = None  # Maximum number of tags allowed to be added
    maxTagLength: int = None  # Maximum text length for a single label
    maxTagCount: int = None  # The maximum number of labels to be displayed. If the number is exceeded,
    # it will be displayed in the form of a floating layer.
    # It will only take effect when the multi-selection mode is enabled.
    overflowTagPopover: TooltipWrapper = None  # default {"placement": "top", "trigger": "hover", "showArrow": false,
    # "offset": [0, -10]}	Store the configuration properties of the floating layer,
    # please refer to Tooltip for detailed configuration
    enableBatchAdd: bool = None  # default 	False, whether to enable batch add mode
    separator: str = None  # default "-", After batch adding is enabled, enter the delimiter of multiple labels,
    # support multiple symbols


class Select(FormItem):
    """Drop down box"""

    type: str = "select"
    options: OptionsNode = None  # option group
    source: API = None  # Dynamic option group
    autoComplete: API = None  # Automatic prompt completion
    delimiter: Union[bool, str] = None  # False # Splice
    labelField: str = None  # "label" # option label field
    valueField: str = None  # "value" # option value field
    joinValues: bool = None  # True # join values
    extractValue: bool = None  # False # extract value
    checkAll: bool = None  # False # whether to support select all
    checkAllLabel: str = None  # "Select All" # Text to be selected
    checkAllBySearch: bool = None  # False # When there is a search, only all items hit by the search are selected
    defaultCheckAll: bool = None  # False # whether to check all by default
    creatable: bool = None  # False # New option
    multiple: bool = None  # False # Multiple choice
    searchable: bool = None  # False # search
    createBtnLabel: str = None  # "Add option" # Add option
    addControls: List[FormItem] = None  # Customize new form items
    addApi: API = None  # Configure the new option interface
    editable: bool = None  # False # edit options
    editControls: List[FormItem] = None  # Customize edit form items
    editApi: API = None  # Configure editing options interface
    removable: bool = None  # False # remove option
    deleteApi: API = None  # Configure delete option interface
    autoFill: dict = None  # autofill
    menuTpl: str = None  # Supports configuring custom menus
    clearable: bool = None  # whether to support clearing in radio mode
    hideSelected: bool = None  # False # hide the selected option
    mobileClassName: str = None  # Mobile floating class name
    selectMode: str = None  # Optional: group, table, tree, chained, associated. They are: list form, table form,
    # tree selection form, Cascade selection form, association selection form (the difference from cascading
    # selection is that the cascade is infinite, while the association has only one level, and the left side of the
    # association can be a tree).
    searchResultMode: str = None  # If the value of selectMode is not set, it can be configured separately. Refer to
    # selectMode to determine the display form of search results.
    columns: List[dict] = None  # When the display form is table, it can be used to configure which columns are
    # displayed, which is similar to the columns configuration in table, but only has the display function.
    leftOptions: List[dict] = None  # Used to configure the left option set when the display form is associated.
    leftMode: str = None  # When the display form is associated, it is used to configure the left selection form,
    # support list or tree. Default is list.
    rightMode: str = None  # When the display form is associated, it is used to configure the right selection form,
    # optional: list, table, tree, chained.


class ChainedSelect(FormItem):
    """Chained Drop down boxs"""

    type: str = "chained-select"
    options: OptionsNode = None  # option group
    source: API = None  # Dynamic option group
    autoComplete: API = None  # Automatic prompt completion
    delimiter: str = None  # Default ',', Splice
    labelField: str = None  # Default "label", option label field
    valueField: str = None  # Default "value", option value field
    joinValues: bool = None  # Default True, join values
    extractValue: bool = None  # Default False, extract value


class NestedSelect(Select):
    """Cascade selector"""

    type: str = "nested-select"
    cascade: bool = None  # False # When set to true, child nodes are not automatically selected when the parent node
    # is selected.
    withChildren: bool = None  # False # When set to true, when the parent node is selected, the value of the child
    # node will be included in the value, otherwise only the value of the parent node will be retained.
    onlyChildren: bool = None  # False # For multiple selections, whether to add only its child nodes to the value
    # when the parent node is selected.
    searchPromptText: str = None  # "Enter content to search" # Search box placeholder text
    noResultsText: str = None  # "No results found" # Text if no results
    hideNodePathLabel: bool = None  # False # whether to hide the path label information of the selected node in the
    # selection box
    onlyLeaf: bool = None  # False # Only leaf nodes are allowed to be selected


class Breadcrumb(AmisNode):
    """Breadcrumb line"""

    class BreadcrumbItem(AmisNode):
        label: str = None  # label text
        href: str = None  # link
        icon: str = None  # fa icon
        dropdown: List = None  # list of breadcrumbitems as dropdown, needs label, href, icon

    type: str = "breadcrumb"
    className: str = None  # The outer class name
    itemClassName: str = None  # Navigation item class name
    separatorClassName: str = None  # separator class name
    dropdownClassName: str = None  # Dropdown menu class name
    dropdownItemClassName: str = None  # Dropdown menu item class name
    separator: str = ">"  # delimeter
    labelMaxLength: int = None  # Default 16, max display length
    tooltipPosition: PlacementEnum = PlacementEnum.top  # tooltip position
    source: API = None  # dynamic data
    items: List[BreadcrumbItem] = None  # list of breadcrumb icons


class Card(AmisNode):
    """Card"""

    class Media(AmisNode):
        type: Literal["image", "video"] = "image"  # multimedia type
        url: str = None  # image or video link
        position: PlacementEnum = PlacementEnum.left  # media location
        className: str = None  # default "w-44 h-28", multimedia CSS class
        isLive: bool = None  # default False, video is live or not
        autoPlay: bool = None  # default False, autoplay video
        poster: Union[bool, str] = None  # default false

    class Header(AmisNode):
        className: str = None  # The header class name
        title: str = None  # title
        titleClassName: str = None  # title class name
        subTitle: Template = None  # subtitle
        subTitleClassName: str = None  # subtitle class name
        subTitlePlaceholder: str = None  # Subtitle placeholder
        description: Template = None  # Description
        descriptionClassName: str = None  # Description class name
        descriptionPlaceholder: str = None  # Description placeholder
        avatar: Template = None  # picture
        avatarClassName: str = None  # default "pull-left thumb avatar b-3x m-r", Image includes layer class name
        imageClassName: str = None  # Image class name
        avatarText: Template = None  # If no picture is configured, the text will be displayed at the picture
        avatarTextBackground: str = None  # avatar text background color
        avatarTextClassName: str = None  # Image text class name
        highlight: bool = None  # default False, whether to show the active style
        highlightClassName: str = None  # Active style class name
        href: str = None  # external link link
        blank: bool = None  # default True, open link in new window

    type: str = "card"
    className: str = None  # The outer class name
    href: str = None  # external link link
    header: Header = None  # Header object
    body: List = []  # Content container, mainly used to place non-form item components
    bodyClassName: str = None  # Content area class name
    actions: List[Action] = None  # Configure button collection
    actionsCount: int = None  # default 4, number of buttons in each row
    itemAction: Action = None  # clicking on a card action
    media: Media = None  # Media object
    secondary: Template = None  # secondary note
    toolbar: List[Action] = None  # toolbar buttons
    dragging: bool = None  # default False, Whether to show the drag icon
    selectable: bool = None  # default False, can be selected
    checkable: bool = None  # default True, selection button is disabled or not
    selected: bool = None  # default False, selection button is selected or not
    hideCheckToggler: bool = None  # default False, hide the selection button
    multiple: bool = None  # default False, multi-select or not
    useCardLabel: bool = None  # default True, Whether the form item label in the card content area uses the
    # style inside the Card


class Cards(AmisNode):
    """Cards deck, allows to use data source to display data items as cards, or manual"""

    type: str = "cards"
    title: str = None  # title
    source: str = None  # default '${items}', Data source, get the variables in the current data field
    placeholder: str = None  # default 'No data', placeholder
    className: str = None  # The outer CSS class name
    headerClassName: str = None  # default 'amis-grid-header', Top outer CSS class name
    footerClassName: str = None  # default 'amis-grid-footer', Bottom outer CSS class name
    itemClassName: str = None  # default 'col-sm-4 col-md-3', Card CSS class name
    card: Card = None  # configured card object for repeat


class ListDisplay(AmisNode):
    """Cards deck, allows to use data source to display data items as cards, or manual"""

    class ListItem(AmisNode):
        title: str = None  # title
        titleClassName: str = None  # title class name
        subTitle: Template = None  # subtitle
        avatar: Template = None  # picture
        avatarClassName: str = None  # default "thumb-sm avatar m-r", Image CSS class name
        desc: Template = None  # Description
        body: List = None  # Content container, mainly used to place non-form item components
        actions: List[Action] = None  # action buttons area
        actionsPosition: Literal["left", "right"] = "right"  # button position

    type: str = "list"
    title: str = None  # title
    source: str = None  # default '${items}', Data source, get the variables in the current data field
    placeholder: str = None  # default 'No data', placeholder
    className: str = None  # The outer CSS class name
    headerClassName: str = None  # default 'amis-grid-header', Top outer CSS class name
    footerClassName: str = None  # default 'amis-grid-footer', Bottom outer CSS class name
    listItem: ListItem = None  # configured list object for repeat


class Textarea(FormItem):
    """Multi-line text input box"""

    type: str = "textarea"
    minRows: int = None  # Minimum number of rows
    maxRows: int = None  # maximum number of rows
    trimContents: bool = None  # whether to remove leading and trailing blank text
    readOnly: bool = None  # read-only
    showCounter: bool = True  # whether to show the counter
    minLength: int = None  # Limit the minimum number of words
    maxLength: int = None  # Limit the maximum number of characters


class InputMonth(FormItem):
    """month"""

    type: str = "input-month"
    value: str = None  # default value
    format: str = None  # "X" # Month selector value format, please refer to moment for more format types
    inputFormat: str = None  # "YYYY-MM" # The display format of the month selector, that is, the timestamp format.
    # For more format types, please refer to moment
    placeholder: str = None  # "Please select a month" # placeholder text
    clearable: bool = None  # True # whether it can be cleared


class InputTime(FormItem):
    """time"""

    type: str = "input-time"
    value: str = None  # default value
    timeFormat: str = None  # "HH:mm" # Time selector value format, please refer to moment for more format types
    format: str = None  # "X" # Time selector value format, please refer to moment for more format types
    inputFormat: str = None  # "HH:mm" # Time selector display format, that is, timestamp format, please refer to
    # moment for more format types
    placeholder: str = None  # "Please select a time" # placeholder text
    clearable: bool = None  # True # whether it can be cleared
    timeConstraints: dict = None  # True # Please refer to: react-datetime


class InputDatetime(FormItem):
    """date"""

    type: str = "input-datetime"
    value: str = None  # default value
    format: str = None  # "X" # Date time picker value format, please refer to the documentation for more format types
    inputFormat: str = None  # "YYYY-MM-DD HH:mm:ss" # Date time picker display format, namely timestamp format,
    # please refer to the documentation for more format types
    placeholder: str = None  # "Please select a date and time" # placeholder text
    shortcuts: str = None  # datetime shortcuts
    minDate: str = None  # Limit the minimum date and time
    maxDate: str = None  # Limit maximum date time
    utc: bool = None  # False # save utc value
    clearable: bool = None  # True # whether it can be cleared
    embed: bool = None  # False # whether to inline
    timeConstraints: dict = None  # True # Please refer to: react-datetime


class InputDate(FormItem):
    """date"""

    type: str = "input-date"
    value: str = None  # default value
    format: str = None  # "X" # Date picker value format, please refer to the documentation for more format types
    inputFormat: str = None  # "YYYY-DD-MM" # Date picker display format, that is, timestamp format, please refer to
    # the documentation for more format types
    placeholder: str = None  # "Please select a date" # placeholder text
    shortcuts: str = None  # date shortcuts
    minDate: str = None  # Limit the minimum date
    maxDate: str = None  # limit max date
    utc: bool = None  # False # save utc value
    clearable: bool = None  # True # whether it can be cleared
    embed: bool = None  # False # whether to inline mode
    timeConstraints: dict = None  # True # Please refer to: react-datetime
    closeOnSelect: bool = None  # False # whether to close the selection box immediately after clicking the date
    schedules: Union[list, str] = None  # The schedule is displayed in the calendar, static data can be set or data
    # can be taken from the context, className refers to the background color
    scheduleClassNames: List[str] = None  # "['bg-warning','bg-danger','bg-success','bg-info','bg-secondary']"
    # The color of the event displayed in the calendar, refer to the background color
    scheduleAction: SchemaNode = None  # Custom schedule display
    largeMode: bool = None  # False # zoom mode


class InputQuarter(InputDate):
    """InputQuarter"""

    type: str = "input-quarter"


class InputQuarterRange(FormItem):
    """Quarter range"""

    type: str = "input-quarter-range"
    format: str = None  # Default X, date picker value format
    inputFormat: str = None  # Default 'YYYY-DD', date picker display format
    placeholder: str = None  # Default 'Please select a quarterly range', placeholder text
    minDate: str = None  # Limit the minimum date and time, the usage is the same as the limit range
    maxDate: str = None  # Limit the maximum date and time, the usage is the same as the limit range
    minDuration: str = None  # Limit the minimum span, such as: 2quarter
    maxDuration: str = None  # Limit the maximum span, such as: 4quarter
    utc: bool = None  # Default False, save UTC value
    clearable: bool = None  # Default True, Is it clearable
    embed: bool = None  # Default False, inline mode
    animation: bool = None  # Default True, Whether to enable cursor animation, needs min amis 2.2.0


class Calendar(FormItem):
    """Calendar"""

    class CalendarItem(AmisNode):
        startTime: str  # ISO 8601 string
        endTime: str  # ISO 8601 string
        content: Union[str, int, dict] = None  # Any, static data or get data from the context
        className: str = None  # css background

    type: str = "calendar"
    schedules: Union[List[CalendarItem], str] = None  # List of schedule items
    scheduleClassNames: List[str] = None  # default ['bg-warning', 'bg-danger', 'bg-success', 'bg-info', 'bg-secondary']
    # color of the event displayed in the calendar, refer to the background color

    scheduleAction: SchemaNode = None  # custom schedule display
    largeMode: bool = None  # Default False, zoom mode full size
    todayActiveStyle: Union[str, dict] = None  # Custom styles when activated today


class InputKV(FormItem):
    """Input key-value pair"""

    type: str = "input-kv"
    valueType: str = None  # Default "input-text", value item type
    keyPlaceholder: str = None  # key placeholder information
    valuePlaceholder: str = None  # value placeholder information
    draggable: bool = None  # Default True, Whether to drag and drop to sort is allowed
    defaultValue: Union[str, int, dict] = None  # default ''
    keySchema: SchemaNode = None  # key field schema
    valueSchema: SchemaNode = None  # value field schema


class InputKVS(FormItem):
    """Input key-value pair, where value can be a deep structure"""

    type: str = "input-kvs"
    addButtonText: str = None  # default 'new field', butto text of the add button
    draggable: bool = None  # Default True, Whether to drag and drop to sort is allowed
    keyItem: Union[str, SchemaNode] = None  # key field
    valueItems: List[Union[str, SchemaNode]] = None  # items for the key


class InputTimeRange(FormItem):
    """time limit"""

    type: str = "input-time-range"
    timeFormat: str = None  # "HH:mm" # Time range selector value format
    format: str = None  # "HH:mm" # time range selector value format
    inputFormat: str = None  # "HH:mm" # Time range selector display format
    placeholder: str = None  # "Please select a time range" # placeholder text
    clearable: bool = None  # True # whether it can be cleared
    embed: bool = None  # False # whether to inline mode


class InputDatetimeRange(InputTimeRange):
    """Date time range"""

    type: str = "input-datetime-range"
    ranges: Union[str, List[str]] = None  # "yesterday,7daysago,prevweek,thismonth,prevmonth,prevquarter" date range
    # shortcut keys, Optional: today,yesterday,1dayago,7daysago,30daysago,90daysago,prevweek,thismonth,thisquarter,
    # prevmonth,prevquarter
    minDate: str = None  # Limit the minimum date and time, the usage is the same as the limit range
    maxDate: str = None  # Limit the maximum date and time, the usage is the same as the limit range
    utc: bool = None  # False # save UTC value


class InputDateRange(InputDatetimeRange):
    """Date Range"""

    type: str = "input-date-range"
    minDuration: str = None  # Limit the minimum span, such as: 2days
    maxDuration: str = None  # Limit the maximum span, such as: 1year


class InputMonthRange(InputDateRange):
    """month range"""

    type: str = "input-month-range"


class Transfer(FormItem):
    """Shuttle"""

    type: Literal["transfer", "transfer-picker", "tabs-transfer", "tabs-transfer-picker"] = "transfer"
    options: OptionsNode = None  # option group
    source: API = None  # Dynamic option group
    delimiter: str = None  # "False" # splicer
    joinValues: bool = None  # True # join values
    extractValue: bool = None  # False # extract value
    searchable: bool = None  # False When set to true, it means that options can be retrieved by entering partial content.
    searchApi: API = None  # If you want to retrieve through the interface, you can set an api.
    statistics: bool = None  # True # whether to display statistics
    selectTitle: str = None  # "Please select" # Title text on the left
    resultTitle: str = None  # "current selection" # title text of the result on the right
    sortable: bool = None  # False # The result can be sorted by drag and drop
    selectMode: str = None  # "list" # Optional: list, table, tree, chained, associated. They are: list form,
    # table form, tree selection form, Cascade selection form, association selection form (the difference from
    # cascading selection is that the cascade is infinite, while the association has only one level, and the left
    # side of the association can be a tree).
    searchResultMode: str = None  # If the value of selectMode is not set, it can be configured separately. Refer to
    # selectMode to determine the display form of search results.
    columns: List[dict] = None  # When the display form is table, it can be used to configure which columns are
    # displayed, which is similar to the columns configuration in table, but only has the display function.
    leftOptions: List[dict] = None  # Used to configure the left option set when the display form is associated.
    leftMode: str = None  # When the display form is associated, it is used to configure the left selection form,
    # support list or tree. Default is list.
    rightMode: str = None  # When the display form is associated, it is used to configure the right selection form,
    # optional: list, table, tree, chained.
    menuTpl: SchemaNode = None  # Used to customize option display
    valueTpl: SchemaNode = None  # Used to customize the display of the value


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
    options: OptionsNode = None  # option group
    source: API = None  # Dynamic option group
    autoComplete: API = None  # Automatic prompt completion
    multiple: bool = None  # False # whether to select multiple
    delimiter: str = None  # "False" # splicer
    labelField: str = None  # "label" # option label field
    valueField: str = None  # "value" # option value field
    iconField: str = None  # "icon" # icon value field
    joinValues: bool = None  # True # join values
    extractValue: bool = None  # False # extract value
    creatable: bool = None  # False # New option
    addControls: List[FormItem] = None  # Customize new form items
    addApi: API = None  # Configure the new option interface
    editable: bool = None  # False # edit options
    editControls: List[FormItem] = None  # Customize edit form items
    editApi: API = None  # Configure editing options interface
    removable: bool = None  # False # remove option
    deleteApi: API = None  # Configure delete option interface
    searchable: bool = None  # False # whether it is searchable, it only takes effect when type is tree-select
    hideRoot: bool = None  # True # Set to false if you want to show a top-level node
    rootLabel: bool = None  # "top level" # Useful when hideRoot is not false, used to set the text of the top level node.
    showIcon: bool = None  # True # whether to show the icon
    showRadio: bool = None  # False # whether to show radio buttons, multiple is false is valid.
    initiallyOpen: bool = None  # True # Set whether to expand all levels by default.
    unfoldedLevel: int = None  # 0 # Set the default unfolded level, which only takes effect when initiallyOpen is
    # not true.
    cascade: bool = None  # False # Do not automatically select child nodes when parent node is selected.
    withChildren: bool = None  # False # When the parent node is selected, the value will contain the value of the
    # child node, otherwise only the value of the parent node will be retained.
    onlyChildren: bool = None  # False # For multiple selections, whether to add only its child nodes to the value
    # when the parent node is selected.
    rootCreatable: bool = None  # False # whether top-level nodes can be created
    rootCreateTip: str = None  # "Add a first-level node" # Create a hovering tip for a top-level node
    minLength: int = None  # Minimum number of selected nodes
    maxLength: int = None  # Maximum number of nodes selected
    treeContainerClassName: str = None  # tree outermost container class name
    enableNodePath: bool = None  # False # whether to enable node path mode
    pathSeparator: str = None  # "/" # The separator of the node path, it takes effect when enableNodePath is true
    deferApi: API = None  # For lazy loading options, please configure defer to true, and then configure deferApi to
    # complete lazy loading
    selectFirst: bool = None
    showOutline: bool = None  # False  # 是否显示树层级展开线
    autoCheckChildren: bool = None  # True  # 当选中父节点时级联选择子节点。
    onlyLeaf: bool = None  # False  # 只允许选择叶子节点
    highlightTxt: str = None  # None  # 标签中需要高亮的字符，支持变量
    itemHeight: int = None  # 32  # 每个选项的高度，用于虚拟渲染
    virtualThreshold: int = None  # 100  # 在选项数量超过多少时开启虚拟渲染
    menuTpl: str = None  # 选项自定义渲染 HTML 片段
    enableDefaultIcon: bool = None  # True  # 是否为选项添加默认的前缀 Icon，父节点默认为folder，叶节点默认为file
    heightAuto: bool = None  # False  # 默认高度会有个 maxHeight，即超过一定高度就会内部滚动，如果希望自动增长请设置此属性


class TreeSelect(InputTree):
    """Tree selector"""

    type: str = "tree-select"
    hideNodePathLabel: bool = None  # whether to hide the path label information of the selected node in the selection box


class Image(AmisNode):
    """picture"""

    type: str = "image"  # "image" if used in Table, Card and List; "static-image" if used as static display in Form
    className: str = None  # Outer CSS class name
    imageClassName: str = None  # Image CSS class name
    thumbClassName: str = None  # Thumbnail CSS class name
    height: int = None  # Image reduction height
    width: int = None  # Image reduction width
    title: str = None  # title
    imageCaption: str = None  # description
    placeholder: str = None  # placeholder text
    defaultImage: str = None  # The image displayed when there is no data
    src: str = None  # Thumbnail address
    href: Template = None  # External link address
    originalSrc: str = None  # Original image address
    enlargeAble: bool = None  # Support zoom in preview
    enlargeTitle: str = None  # enlarge the title of the preview
    enlargeCaption: str = None  # Description of the enlarged preview
    thumbMode: str = None  # "contain" # preview mode, optional: 'w-full','h-full','contain','cover'
    thumbRatio: str = None  # "1:1" # Preview ratio, optional: '1:1','4:3','16:9'
    imageMode: str = None  # "thumb" Image display mode, optional: 'thumb', 'original' ie: thumbnail mode or original
    # image mode


class Images(AmisNode):
    """Photo album"""

    type: str = "images"  # "images" if used in Table, Card and List; "static-images" if used as static display in Form
    className: str = None  # Outer CSS class name
    defaultImage: str = None  # Default display image
    value: Union[str, List[str], List[dict]] = None  # Image array
    source: str = None  # data source
    delimiter: str = None  # "," # Delimiter, when value is a string, use this value to separate and split
    src: str = None  # Preview image address, support data mapping to obtain image variables in the object
    originalSrc: str = None  # Original image address, support data mapping to obtain image variables in the object
    enlargeAble: bool = None  # Support zoom in preview
    thumbMode: str = None  # "contain" # preview mode, optional: 'w-full','h-full','contain','cover'
    thumbRatio: str = None  # "1:1" # Preview ratio, optional: '1:1','4:3','16:9'


class Carousel(AmisNode):
    """Carousel"""

    class Item(AmisNode):
        image: str = None  # Image link
        href: str = None  # Image open URL link
        imageClassName: str = None  # Image class name
        title: str = None  # image title
        titleClassName: str = None  # Image title class name
        description: str = None  # Picture description
        descriptionClassName: str = None  # Picture description class name
        html: str = None  # HTML custom, same as Tpl

    type: str = "carousel"  # Specify as the Carousel renderer
    className: str = None  # "panel-default" # The class name of the outer Dom
    options: List[Item] = None  # "[]" # Carousel panel data
    itemSchema: dict = None  # custom schema to display data
    auto: bool = True  # whether to rotate automatically
    interval: str = None  # "5s" # Switch animation interval
    duration: str = None  # "0.5s" # Switch animation duration
    width: str = None  # "auto" # width
    height: str = None  # "200px" # height
    controls: List[str] = None  # "['dots','arrows']" # Display left and right arrows, bottom dot index
    controlsTheme: str = None  # "light" # Left and right arrows, bottom dot index color, default light, and dark mode
    animation: str = None  # "fade" # Switch animation effect, default fade, and slide mode
    thumbMode: str = None  # "cover"|"contain" # The default zoom mode of the picture


class Mapping(AmisNode):
    """Mapping"""

    type: str = "mapping"  # "mapping" if used in Table, Card and List; "static-mapping" if used as static display in Form
    className: str = None  # Outer CSS class name
    placeholder: str = None  # placeholder text
    map: dict = None  # map configuration
    source: API = None  # API or data map


class CRUD(AmisNode):
    """Add, delete, modify, check"""

    class Messages(AmisNode):
        fetchFailed: str = None  # Prompt when fetch fails
        saveOrderFailed: str = None  # Failed to save order
        saveOrderSuccess: str = None  # Save order success prompt
        quickSaveFailed: str = None  # Quick save failure prompt
        quickSaveSuccess: str = None  # Quick save success prompt

    type: str = "crud"  # type specifies the CRUD renderer
    mode: str = None  # "table" # "table" , "cards" or "list"
    title: str = None  # "" # Can be set to empty, when set to empty, there is no title bar
    className: str = None  # The class name of the outer Dom of the table
    api: API = None  # The api that CRUD uses to get list data.
    loadDataOnce: bool = None  # whether to load all data at once (front-end paging)
    loadDataOnceFetchOnFilter: bool = None  # True # When loadDataOnce is turned on, whether to re-request the api
    # when filtering
    source: str = None  # The data mapping interface returns the value of a field. If it is not set, the ${items} or
    # ${rows} returned by the interface will be used by default. It can also be set to the content of the upper data
    # source.
    filter: Union[SchemaNode, Form] = None  # Set the filter, when the form is submitted, it will bring the data to
    # the current mode refresh list.
    filterTogglable: bool = None  # False # whether the filter can be displayed or hidden
    filterDefaultVisible: bool = None  # True # Set whether the filter is visible by default.
    initFetch: bool = None  # True # whether to pull data during initialization, only for the case with filter,
    # without filter, data will be pulled initially
    interval: int = None  # refresh time (minimum 1000)
    silentPolling: bool = None  # Configure whether to hide the loading animation when refreshing
    stopAutoRefreshWhen: str = None  # Configure the condition for stopping refresh by expression
    stopAutoRefreshWhenModalIsOpen: bool = None  # Turn off auto refresh when there is a popup, close the popup and
    # restore
    syncLocation: bool = None  # False # whether to synchronize the parameters of the filter conditions to the
    # address bar, !!! After opening, the data type may be changed, and it cannot pass the fastpi data verification
    draggable: bool = None  # whether it can be sorted by dragging
    itemDraggableOn: bool = None  # Use expressions to configure whether drag and drop sorting is possible
    saveOrderApi: API = None  # Save order api.
    quickSaveApi: API = None  # API for batch saving after quick editing.
    quickSaveItemApi: API = None  # API to use when quick edit is configured to save in time.
    bulkActions: List[Action] = None  # Batch operation list, after configuration, the table can be selected.
    defaultChecked: bool = None  # When batch operations are available, whether to check all by default.
    messages: Messages = None  # Override the message prompt, if not specified, the message returned by the api will
    # be used
    primaryField: str = None  # Set the ID field name. 'id'
    perPage: int = None  # Set how many pieces of data are displayed on one page. 10
    defaultParams: dict = None  # Set the default filter default parameters, which will be sent to the backend
    # together when querying
    pageField: str = None  # Set the pagination page number field name. "page"
    perPageField: str = None  # "perPage" # Set the field name of how many pieces of data are displayed on one page.
    # Note: Best used with defaultParams, see example below.
    perPageAvailable: List[int] = None  # [5, 10, 20, 50, 100] # Set how many data drop-down boxes can be displayed
    # on one page.
    orderField: str = None  # Set the field name used to determine the position. After setting, the new order will be
    # assigned to this field.
    hideQuickSaveBtn: bool = None  # Hide the top quick save prompt
    autoJumpToTopOnPagerChange: bool = None  # whether to automatically jump to the top when splitting pages.
    syncResponse2Query: bool = None  # True # Synchronize the returned data to the filter.
    keepItemSelectionOnPageChange: bool = None  # True
    # Retain item selection. After the default paging and searching, the user-selected item will be cleared. After
    # this option is enabled, the user's selection will be retained, enabling cross-page batch operations.
    labelTpl: str = None  # Single description template, keepItemSelectionOnPageChange
    # When set to true, all selected items will be listed. This option can be used to customize the entry display copy.
    headerToolbar: list = None  # ['bulkActions','pagination'] # Top toolbar configuration
    footerToolbar: list = None  # ['statistics','pagination'] # Bottom toolbar configuration
    alwaysShowPagination: bool = None  # whether to always show pagination
    affixHeader: bool = None  # True # whether to fix the header (under table)
    autoGenerateFilter: bool = None  # whether to open the query area, after it is enabled, the query condition form
    # will be automatically generated according to the searchable attribute value of the column element
    itemAction: Action = None  # Implement custom actions after clicking a row, support all configurations in action,
    # such as pop-up boxes, refresh other components, etc.
    resizable: bool = None  # 是否可以调整列宽度
    orderBy: str = None  # 默认排序字段，这个是传给后端，需要后端接口实现
    orderDir: Literal["asc", "desc"] = None  # 排序方向
    resetPageAfterAjaxItemAction: bool = None  # False  # 单条数据 ajax 操作后是否重置页码为第一页
    autoFillHeight: Union[bool, Dict[str, int]] = None  # 内容区域自适应高度


class TableColumn(AmisNode):
    """Column configuration"""

    type: str = None  # Literal['text','audio','image','link','tpl','mapping','carousel','date',
    # 'progress','status','switch','list','json','operation','tag']
    label: Template = None  # header text content
    name: str = None  # Associate data by name
    tpl: Template = None  # Template
    fixed: str = None  # whether to fix the current column left|right|none
    popOver: Union[bool, dict] = None  # popover
    quickEdit: Union[bool, dict] = None  # quick edit
    copyable: Union[bool, dict] = None  # whether to copy boolean or {icon: string, content:string}
    sortable: bool = None  # False # whether it is sortable
    searchable: Union[bool, SchemaNode] = None  # False # whether to quickly search boolean|Schema
    width: Union[int, str] = None  # column width
    remark: RemarkT = None  # prompt message
    breakpoint: str = None  # *,ls. When there are too many columns, the content cannot be displayed completely,
    # some information can be displayed at the bottom, and users can expand to view the details
    filterable: Union[bool, Dict[str, Any]] = None  # filter configuration
    toggled: bool = None  # whether to expand by default, in the column configuration, you can configure toggled to
    # false to not display this column by default
    backgroundScale: int = None  # Can be used to automatically assign color scales based on data control


class ColumnOperation(TableColumn):
    """Action column"""

    type: str = "operation"
    buttons: List[Union[Action, AmisNode]] = None


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
    title: str = None  # title
    source: str = None  # "${items}" # Data source, bind the current environment variable
    affixHeader: bool = None  # True # whether to fix the header
    columnsTogglable: Union[bool, str] = None  # "auto" # Display column display switch, automatic: it is
    # automatically turned on when the number of columns is greater than or equal to 5
    placeholder: str = None  # "No data" # Text prompt when there is no data
    className: str = None  # "panel-default" # Outer CSS class name
    tableClassName: str = None  # "table-db table-striped" # table CSS class name
    headerClassName: str = None  # "Action.md-table-header" # Top outer CSS class name
    footerClassName: str = None  # "Action.md-table-footer" # Bottom outer CSS class name
    toolbarClassName: str = None  # "Action.md-table-toolbar" # Toolbar CSS class name
    columns: List[Union[TableColumn, SchemaNode]] = None  # Used to set column information
    combineNum: int = None  # Automatically combine cells
    itemActions: List[Action] = None  # Floating row action button group
    itemCheckableOn: Expression = None  # Configure the condition for whether the current row can be checked, use an
    # expression
    itemDraggableOn: Expression = None  # To configure whether the current row can be dragged or not, use an expression
    checkOnItemClick: bool = None  # False # whether clicking on the data row can check the current row
    rowClassName: str = None  # Add CSS class name to row
    rowClassNameExpr: Template = None  # Add CSS class name to row via template
    prefixRow: list = None  # top summary row
    affixRow: list = None  # Bottom summary row
    itemBadge: "Badge" = None  # Row badge configuration
    autoFillHeight: bool = None  # Content area adaptive height
    footable: Union[bool, dict] = None  # When there are too many columns, the content cannot be fully displayed.
    # Some information can be displayed at the bottom, allowing users to expand to view the details. The
    # configuration is very simple, just turn on the footable attribute, and add a breakpoint attribute to the column
    # you want to display at the bottom as *.
    resizable: bool = None  # 列宽度是否支持调整
    selectable: bool = None  # 支持勾选
    multiple: bool = None  # 勾选 icon 是否为多选样式checkbox， 默认为radio


class Chart(AmisNode):
    """Chart: https://echarts.apache.org/en/option.html#title"""

    type: str = "chart"  # specify the chart renderer
    className: str = None  # The class name of the outer Dom
    body: SchemaNode = None  # Content container
    api: API = None  # Configuration item interface address
    source: dict = None  # Get the variable value in the data chain as configuration through data mapping
    initFetch: bool = None  # whether to request the interface when the component is initialized
    interval: int = None  # refresh time (minimum 1000)
    config: Union[dict, str] = None  # Set the configuration item of eschars, when it is string, you can set
    # configuration items such as function
    style: dict = None  # Set the style of the root element
    width: str = None  # Set the width of the root element
    height: str = None  # Set the height of the root element
    replaceChartOption: bool = None  # False # Does each update completely overwrite the configuration item or append it?
    trackExpression: str = None  # Update the chart when the value of this expression changes


class Code(AmisNode):
    """Code highlighting"""

    type: str = "code"
    className: str = None  # Outer CSS class name
    value: str = None  # display color value
    name: str = None  # In other components, when used as variable mapping
    language: str = None  # The highlighted language used, the default is plaintext
    tabSize: int = None  # 4 # Default tab size
    editorTheme: str = None  # "'vs'" # theme, and 'vs-dark'
    wordWrap: str = None  # "True" # whether to wrap


class Json(AmisNode):
    """JSON display component"""

    type: str = "json"  # "json" if in Table, Card and List; "static-json" if used for static display in Form
    className: str = None  # Outer CSS class name
    value: Union[dict, str] = None  # json value, if it is string, it will be parsed automatically
    source: str = None  # Get the value in the data chain through the data map
    placeholder: str = None  # placeholder text
    levelExpand: int = None  # 1 # Default expanded level
    jsonTheme: str = None  # "twilight" # Theme, optional twilight and eighties
    mutable: bool = None  # False # whether it can be modified
    displayDataTypes: bool = None  # False # whether to display data types


class Link(AmisNode):
    """Link"""

    type: str = "link"  # "link" if used in Table, Card and List; "static-link" if used as static display in Form
    body: str = None  # Text inside the tag
    href: str = None  # link address
    blank: bool = None  # whether to open in a new tab
    htmlTarget: str = None  # The target of the a tag, which takes precedence over the blank attribute
    title: str = None  # the title of the a tag
    disabled: bool = None  # disable hyperlinks
    icon: str = None  # Hyperlink icon to enhance display
    rightIcon: str = None  # right icon


class Log(AmisNode):
    """Real-time log"""

    type: str = "log"
    source: API = None  # Support variables, which can be initially set to empty, so that it will not be loaded
    # initially, and will be loaded when the variable has a value
    height: int = None  # 500 # Display area height
    className: str = None  # Outer CSS class name
    autoScroll: bool = None  # True # whether to scroll automatically
    placeholder: str = None  # The text being loaded
    encoding: str = None  # "utf-8" # The character encoding of the returned content


class Property(AmisNode):
    """Property sheet"""

    class Item(AmisNode):
        label: Template = None  # attribute name
        content: Template = None  # attribute value
        span: int = None  # attribute values span several columns
        visibleOn: Expression = None  # Display expression
        hiddenOn: Expression = None  # hidden expression

    type: str = "property"
    className: str = None  # The class name of the outer dom
    style: dict = None  # The style of the outer dom
    labelStyle: dict = None  # style of attribute name
    contentStyle: dict = None  # style of attribute value
    column: int = None  # 3 # several columns per row
    mode: str = None  # 'table' # Display mode, currently only 'table' and 'simple'
    separator: str = None  # ',' # Separator between attribute name and value in 'simple' mode
    source: Template = None  # data source
    title: str = None  # title
    items: List[Item] = None  # data items


class QRCode(AmisNode):
    """QR code"""

    type: str = "qr-code"  # Specify as QRCode renderer
    value: Template  # The text displayed after scanning the QR code, if you want to display a page, please enter the
    # full url (starting with "http://..." or "https://..."), templates are supported
    className: str = None  # The class name of the outer Dom
    qrcodeClassName: str = None  # QR code SVG class name
    codeSize: int = None  # 128 # The width and height of the QR code
    backgroundColor: str = None  # "#fff" # QR code background color
    foregroundColor: str = None  # "#000" # QR code foreground color
    level: str = None  # "L" # QR code complexity level, there are four types ('L' 'M' 'Q' 'H')


class Barcode(AmisNode):
    """Barcode"""

    class Options(AmisNode):
        format: BarcodeEnum = BarcodeEnum.auto  # The format of the barcode
        width: int = None  # default 2 width of the barcode image
        height: int = None  # default 100 height of the barcode image
        displayValue: bool = None  # default True
        text: str = None
        fontOptions: str = ""
        font: str = None  # default "monospace"
        textAlign: str = None  # default "center"
        textPosition: str = None  # default "bottom"
        textMargin: int = None  # default 2
        fontSize: int = None  # default 20
        background: str = None  # #ffffff CSS Color
        lineColor: str = None  # #000000 CSS color
        margin: int = None  # default 10
        marginTop: int = None
        marginBottom: int = None
        marginLeft: int = None
        marginRight: int = None
        flat: bool = None  # default False, no guard bars if True

    type: str = "barcode"  # Specify as QRCode renderer
    value: str = None  # The value of the barcode
    className: str = None  # The class name of the outer Dom
    options: Options = None


class Color(AmisNode):
    type: Literal["color", "static-color"] = "color"
    value: str = None  # The value of the color CSS code
    className: str = None  # The class name of the outer Dom
    defaultColor: str = None  # "#ccc" default color value
    showValue: bool = None  # default True, whether to display the color value on the right


class Progress(AmisNode):
    type: Literal["progress", "static-progress"] = "progress"
    mode: ProgressEnum = None  # The type of progress "bar", optional
    value: Template = None  # The value of the progress
    className: str = None  # The class name of the outer Dom
    showLabel: bool = None  # default True, whether to show progress text
    stripe: bool = None  # default False
    animate: bool = None  # default False
    map: Union[str, List[str], List[Dict]] = None  # progress colormap, as dict = {value:number, color:string}
    # default ['bg-danger', 'bg-warning', 'bg-info', 'bg-success', 'bg-success']
    threshold: Union[Dict, List] = None  # default -,
    # {value: template , color?: template } | List[{value: template , color?: template }]
    showThresholdText: bool = None  # default False, whether to display the threshold (scale) value
    valueTpl: str = None  # default ${value}%, custom formatted content
    strokeWidth: int = None  # default 10 by circle, 6 with dashboard
    gapDegree: int = None  # default 75, angle of the missing corner of the instrument panel, the value can be 0 ~ 295
    gapPosition: str = None  # default "bottom", Dashboard progress bar notch position, optional top bottom left right


class PaginationWrapper(AmisNode):
    type: str = "pagination-wrapper"
    showPageInput: bool = None  # default False, whether to display the quick jump input box
    maxButtons: int = None  # default 5, Maximum number of pagination buttons to display
    inputName: str = None  # default 'items', input field name
    outputName: str = None  # default 'items', output field name
    perPage: int = None  # default 10, Display multiple pieces of data per page
    position: Literal["top", "none", "bottom"] = "top"  # Pagination display position, if it is configured as none,
    # you need to configure the pagination component in the content area, otherwise it will not be displayed
    body: SchemaNode = None  # Display content


class Pagination(AmisNode):
    type: str = "pagination"
    mode: Literal["simple", "normal"] = "normal"  # The mini version/simple version only displays left and right arrows,
    # used with hasNext
    layout: Union[str, List[str]] = None  # default 'pager', Adjust the paging structure layout by controlling
    # the order of the layout properties
    maxButtons: int = None  # default 10, Display multiple pieces of data per page
    lastPage: int = None  # lastPage will be recalculated when the total number of entries is set
    total: int = None  # total number of pages
    activePage: int = None  # default 1, current page number
    perPage: int = None  # default 10, Display multiple pieces of data per page
    showPerPage: bool = None  # default False, whether to display the perPage switcher layout
    perPageAvailable: List[int] = None  # default [10, 20, 50, 100], how many lines can be displayed per page
    showPageInput: bool = None  # default False, whether to display the quick jump input box layout
    disabled: bool = None  # default False, is pagination disabled


class MatrixCheckboxes(FormItem):
    """Matrix type input box."""

    class RowItem(AmisNode):
        label: str

    class ColumnItem(AmisNode):
        label: str

    type: str = "matrix-checkboxes"
    columns: List[ColumnItem] = None  # list of column items
    rows: List[RowItem] = None  # list of row items
    rowLabel: str = None  # row header description
    source: API = None  # Api address, if the option group is not fixed.
    multiple: bool = None  # default False, multiple choice
    singleSelectMode: Literal["false", "cell", "row", "column"] = "column"


class Wrapper(AmisNode):
    type: str = "wrapper"
    className: str = None  # The class name of the outer Dom
    style: Union[str, dict] = None  # Custom style (inline style), highest priority
    body: SchemaNode = None  # Display content
    size: Union[str, SizeEnum] = None  # Specify the wrapper size, support: xs, sm, md, lg


class WebComponent(AmisNode):
    type: str = "web-component"
    tag: str = None  # The specific web-component tag used
    style: Union[str, dict] = None  # Custom style (inline style), highest priority
    body: SchemaNode = None  # child node
    props: dict = None  # attributes by their labels


class UUIDField(AmisNode):
    """Randomly generates an id that can be used to prevent repeated form submissions."""

    type: str = "uuid"
    name: str = None  # The field name
    length: int = None  # if set, generates short random numbers, if not set it generates a UUID


class SearchBox(AmisNode):
    type: str = "search-box"
    className: str = None  # The class name of the outer Dom
    mini: bool = None  # default False, whether it is in mini mode
    searchImediately: bool = None  # default False, whether to search now


class Sparkline(AmisNode):
    type: str = "sparkline"
    width: int = None  # width of the sparkline image
    height: int = None  # height of the sparkline image
    value: List[Union[int, float]] = None  #
    clickAction: Action = None  # Action when clicked


class Tag(AmisNode):
    type: str = "tag"
    className: str = None  # Custom CSS style class name
    displayMode: Literal["normal", "rounded", "status"] = "normal"  # Display mode
    closable: bool = None  # default False, show close icon
    color: str = None  # color theme or custom color value,
    # 'active' | 'inactive' | 'error' | 'success' | 'processing' | 'warning'
    label: str = None  # default '-'
    icon: str = None  # custom font icon
    style: Union[str, dict] = None  # Custom style (inline style), highest priority


class Video(AmisNode):
    """video"""

    type: str = "video"  # specify the video renderer
    className: str = None  # The class name of the outer Dom
    src: str = None  # video address
    isLive: bool = None  # False # whether it is a live broadcast, it needs to be added when the video is live,
    # supports flv and hls formats
    videoType: str = None  # Specify the live video format
    poster: str = None  # Video cover address
    muted: bool = None  # whether to mute
    autoPlay: bool = None  # whether to play automatically
    rates: List[float] = None  # Multiples in the format [1.0, 1.5, 2.0]


class Alert(AmisNode):
    """hint"""

    type: str = "alert"  # Specify as the alert renderer
    className: str = None  # The class name of the outer Dom
    level: str = None  # "info" # Level, can be: info, success, warning or danger
    body: SchemaNode = None  # Display content
    showCloseButton: bool = None  # False # whether to show the close button
    closeButtonClassName: str = None  # CSS class name of the close button
    showIcon: bool = None  # False # whether to show icon
    icon: str = None  # custom icon
    iconClassName: str = None  # CSS class name of icon


class Dialog(AmisNode):
    """Dialog"""

    type: str = "dialog"  # Specify as Dialog renderer
    title: SchemaNode = None  # Popup layer title
    body: SchemaNode = None  # Add content to the Dialog content area
    size: Union[str, SizeEnum] = None  # Specify the dialog size, support: xs, sm, md, lg, xl, full
    bodyClassName: str = None  # "modal-body" # The style class name of the Dialog body area
    closeOnEsc: bool = None  # False # whether to support pressing Esc to close Dialog
    showCloseButton: bool = None  # True # whether to show the close button in the upper right corner
    showErrorMsg: bool = None  # True # whether to display the error message in the lower left corner of the popup
    disabled: bool = None  # False # If this property is set, the Dialog is read-only and has no submit operation.
    actions: List[Action] = None  # If you want to not display the bottom button, you can configure: [] "[Confirm]
    # and [Cancel]"
    data: dict = None  # Support data mapping, if not set, it will inherit the data in the context of the trigger
    # button by default.
    showLoading: bool = None  # True # 是否在弹框左下角显示 loading 动画


class Drawer(AmisNode):
    """drawer"""

    type: str = "drawer"  # "drawer" specifies the Drawer renderer
    title: SchemaNode = None  # Popup layer title
    body: SchemaNode = None  # Add content to the Drawer content area
    size: Union[str, SizeEnum] = None  # Specify Drawer size, support: xs, sm, md, lg
    position: str = None  # 'left' # position
    bodyClassName: str = None  # "modal-body" # The style class name of the Drawer body area
    closeOnEsc: bool = None  # False # whether to support pressing Esc to close Drawer
    closeOnOutside: bool = None  # False # whether to close the Drawer when clicking outside the content area
    overlay: bool = None  # True # whether to display the overlay
    resizable: bool = None  # False # whether the size of the Drawer can be changed by dragging and dropping
    actions: List[Action] = None  # Can not be set, there are only two buttons by default. "[Confirm] and [Cancel]"
    data: dict = None  # Support data mapping, if not set, it will inherit the data in the context of the trigger
    # button by default.
    className: str = None  # Drawer 最外层容器的样式类名
    headerClassName: str = None  # Drawer 头部 区域的样式类名
    footerClassName: str = None  # Drawer 页脚 区域的样式类名
    showCloseButton: bool = True  # 是否展示关闭按钮，当值为 false 时，默认开启 closeOnOutside
    width: Union[int, str] = "500px"  # 容器的宽度，在 position 为 left 或 right 时生效
    height: Union[int, str] = "500px"  # 容器的高度，在 position 为 top 或 bottom 时生效


class Iframe(AmisNode):
    """Iframe"""

    type: str = "iframe"  # Specify as iFrame renderer
    className: str = None  # iFrame class name
    frameBorder: list = None  # frameBorder
    style: dict = None  # style object
    src: str = None  # iframe address
    allow: str = None  # allow configuration
    sandbox: str = None  # sandbox configuration
    referrerpolicy: str = None  # referrerpolicy configuration
    height: Union[int, str] = None  # "100%" # iframe height
    width: Union[int, str] = None  # "100%" # iframe width


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
    className: str = None  # The class name of the outer dom
    fit: str = None  # "cover" # Image zoom type
    src: str = None  # Image address
    text: str = None  # text
    icon: str = None  # icon
    shape: str = None  # "circle" # shape, can also be square
    size: int = None  # 40 # size
    style: dict = None  # The style of the outer dom


class Audio(AmisNode):
    """Audio"""

    type: str = "audio"  # specify the audio renderer
    className: str = None  # The class name of the outer Dom
    inline: bool = None  # True # whether it is inline mode
    src: str = None  # audio address
    loop: bool = None  # False # whether to loop playback
    autoPlay: bool = None  # False # whether to play automatically
    rates: List[float] = None  # "[]" # Configurable audio playback speed such as: [1.0, 1.5, 2.0]
    controls: List[str] = None  # "['rates','play','time','process','volume']" # Internal module customization


class Status(AmisNode):
    """state"""

    type: str = "status"  # Specify as Status renderer
    className: str = None  # The class name of the outer Dom
    placeholder: str = None  # placeholder text
    map: dict = None  # map icon
    labelMap: dict = None  # map text


class Tasks(AmisNode):
    """Task operation collection"""

    class Item(AmisNode):
        label: str = None  # task name
        key: str = None  # Task key value, please distinguish it uniquely
        remark: str = None  # Current task status, support html
        status: str = None  # Task status: 0: Initial status, inoperable. 1: Ready, operational state. 2: In
        # progress, not over yet.
        # 3: There is an error, no retry. 4: Completed normally. 5: There is an error, and you can try again.

    type: str = "tasks"  # Specify as Tasks renderer
    className: str = None  # The class name of the outer Dom
    tableClassName: str = None  # class name of table Dom
    items: List[Item] = None  # task list
    checkApi: API = None  # Return the task list, please refer to items for the returned data.
    submitApi: API = None  # API used for submitting tasks
    reSubmitApi: API = None  # If the task fails and can be retried, this API will be used when submitting
    interval: int = None  # 3000 # When there is a task in progress, it will be checked again at regular intervals,
    # and the time interval is configured through this, the default is 3s.
    taskNameLabel: str = None  # "task name" # task name column description
    operationLabel: str = None  # "Operation" # Operation column description
    statusLabel: str = None  # "status" # description of status column
    remarkLabel: RemarkT = None  # "Remark" # Remark column description
    btnText: str = None  # "Online" # Action button text
    retryBtnText: str = None  # "Retry" # Retry action button text
    btnClassName: str = None  # "btn-sm btn-default" # Configure the container button className
    retryBtnClassName: str = None  # "btn-sm btn-danger" # Configure container retry button className
    statusLabelMap: List[str] = None  # Status display corresponding class name configuration
    # "["label-warning", "label-info", "label-success", "label-danger", "label-default", "label-danger"]"
    statusTextMap: List[str] = None  # "["Not started", "Ready", "In progress", "Error", "Completed", "Error"]" #
    # Status display corresponding text display configuration


class Wizard(AmisNode):
    """Wizard"""

    class Step(AmisNode):
        title: str = None  # Step title
        mode: str = None  # Display the default, the same as the mode in Form, choose: normal, horizontal or inline.
        horizontal: Horizontal = None  # When in horizontal mode, it is used to control the ratio of left and right
        api: API = None  # The current step saves the interface, which can be left unconfigured.
        initApi: API = None  # The current step data initialization interface.
        initFetch: bool = None  # whether the current step data initialization interface is initially fetched.
        initFetchOn: Expression = None  # whether the current step data initialization interface is initially fetched
        # is determined by an expression.
        body: List[FormItem] = None  # The form item collection of the current step, please refer to FormItem.

    type: str = "wizard"  # Specify as Wizard component
    mode: str = None  # "horizontal" # Display mode, choose: horizontal or vertical
    api: API = None  # The interface saved in the last step.
    initApi: API = None  # Initialize data interface
    initFetch: API = None  # whether to fetch data initially.
    initFetchOn: Expression = None  # whether to pull data initially, configure by expression
    actionPrevLabel: str = None  # "Previous" # Previous button text
    actionNextLabel: str = None  # "Next" # Next button text
    actionNextSaveLabel: str = None  # "Save and Next" # Save and Next button text
    actionFinishLabel: str = None  # "Finish" # Finish button text
    className: str = None  # Outer CSS class name
    actionClassName: str = None  # "btn-sm btn-default" # Button CSS class name
    reload: str = None  # Refresh the target object after the operation. Please fill in the name value set by the
    # target component. If it is filled in window, the current page will be refreshed as a whole.
    redirect: Template = None  # "3000" # Jump after the operation.
    target: str = None  # "False" # You can submit data to other components instead of saving it yourself. Please
    # fill in the name value set by the target component,
    # If it is filled in as window, the data will be synchronized to the address bar, and the components that depend
    # on these data will be automatically refreshed.
    steps: List[Step] = None  # Array, configure step information
    startStep: int = None  # "1" # Start default value, starting from the first step. Templates can be supported,
    # but only when the component is created, the template is rendered and the current number of steps is set. When
    # the component is refreshed later,
    # The current step will not change according to startStep


class AmisRender(AmisNode):
    """Amis render"""

    type: str = "amis"  # Specify as amis renderer
    schema_: SchemaNode = Field(None, alias="schema")  # amis schema
    props: dict = None  # amis props


PageSchema.update_forward_refs()
ActionType.Dialog.update_forward_refs()
ActionType.Drawer.update_forward_refs()
TableCRUD.update_forward_refs()
Form.update_forward_refs()
Tpl.update_forward_refs()
InputText.update_forward_refs()
InputNumber.update_forward_refs()
Picker.update_forward_refs()
