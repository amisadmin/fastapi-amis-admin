from enum import Enum


class LevelEnum(str, Enum):
    """按钮等级"""
    primary = 'primary'
    secondary = 'secondary'
    info = 'info'
    success = 'success'
    warning = 'warning'
    danger = 'danger'
    light = 'light'
    dark = 'dark'
    link = 'link'
    default = 'default'


class SizeEnum(str, Enum):
    """窗口尺寸"""
    xs = 'xs'
    sm = 'sm'
    md = 'md'
    lg = 'lg'
    xl = 'xl'
    full = 'full'


class DisplayModeEnum(str, Enum):
    """表单展示模式"""
    normal = 'normal'  # 常规模式
    horizontal = 'horizontal'  # 水平模式
    inline = 'inline'  # 内联模式


class LabelEnum(str, Enum):
    """标签样式"""
    primary = 'primary'
    success = 'success'
    warning = 'warning'
    danger = 'danger'
    default = 'default'
    info = 'info'


class StatusEnum(str, Enum):
    """默认状态"""
    success = 'success'  # 成功
    fail = 'fail'  # 失败
    pending = 'pending'  # 运行中
    queue = 'queue'  # 排队中
    schedule = 'schedule'  # 调度中


class TabsModeEnum(str, Enum):
    """选项卡模式"""
    line = "line"
    card = "card"
    radio = "radio"
    vertical = "vertical"
    chrome = "chrome"
    simple = "simple"
    strong = "strong"
    tiled = "tiled"
    sidebar = "sidebar"
