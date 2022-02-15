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
