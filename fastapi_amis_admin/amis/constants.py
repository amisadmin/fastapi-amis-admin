from enum import Enum


class LevelEnum(str, Enum):
    """Button level"""

    primary = "primary"
    secondary = "secondary"
    info = "info"
    success = "success"
    warning = "warning"
    danger = "danger"
    light = "light"
    dark = "dark"
    link = "link"
    default = "default"


class SizeEnum(str, Enum):
    """Window size"""

    xs = "xs"
    sm = "sm"
    md = "md"
    lg = "lg"
    xl = "xl"
    full = "full"


class DisplayModeEnum(str, Enum):
    """Form display mode"""

    normal = "normal"  # normal mode
    horizontal = "horizontal"  # horizontal mode
    inline = "inline"  # inline mode


class LabelEnum(str, Enum):
    """Label style"""

    primary = "primary"
    success = "success"
    warning = "warning"
    danger = "danger"
    default = "default"
    info = "info"


class StatusEnum(str, Enum):
    """Default state"""

    success = "success"  # success
    fail = "fail"  # fail
    pending = "pending"  # running
    queue = "queue"  # in queue
    schedule = "schedule"  # scheduling


class TabsModeEnum(str, Enum):
    """Tab mode"""

    line = "line"
    card = "card"
    radio = "radio"
    vertical = "vertical"
    chrome = "chrome"
    simple = "simple"
    strong = "strong"
    tiled = "tiled"
    sidebar = "sidebar"
