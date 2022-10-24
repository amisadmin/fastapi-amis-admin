from enum import Enum


class ProgressEnum(str, Enum):
    """Progressbar Mode"""

    line = "click"
    circle = "circle"
    dashboard = "dashboard"


class BarcodeEnum(str, Enum):
    """Barcode Format"""

    auto = "auto"  # CODE128
    pharmacode = "pharmacode"
    codabar = "codabar"
    CODE128 = "CODE128"
    CODE128A = "CODE128A"
    CODE128B = "CODE128B"
    CODE128C = "CODE128C"
    EAN2 = "EAN2"
    EAN5 = "EAN5"
    EAN8 = "EAN8"
    EAN13 = "EAN13"
    UPC = "UPC"
    CODE39 = "CODE39"
    ITF14 = "ITF14"
    MSI = "MSI"
    MSI10 = "MSI10"
    MSI11 = "MSI11"
    MSI1010 = "MSI1010"
    MSI1110 = "MSI1110"


class StepStatusEnum(str, Enum):
    wait = "wait"
    process = "process"
    finish = "finish"
    error = "error"


class TriggerEnum(str, Enum):
    """Trigger Type"""

    click = "click"
    hover = "hover"
    focus = "focus"


class PlacementEnum(str, Enum):
    """Placement Position"""

    top = "top"
    left = "left"
    right = "right"
    bottom = "bottom"


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
