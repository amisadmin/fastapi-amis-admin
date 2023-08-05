__version__ = "0.6.4a1"
__url__ = "https://github.com/amisadmin/fastapi_amis_admin"

import gettext
from pathlib import Path

from .utils.translation import i18n

BASE_DIR = Path(__file__).resolve().parent

i18n.load_translations(
    {
        "zh_CN": gettext.translation(
            domain="messages",
            localedir=BASE_DIR / "locale",
            languages=["zh_CN"],
        ),
        "de_DE": gettext.translation(
            domain="messages",
            localedir=BASE_DIR / "locale",
            languages=["de_DE"],
        ),
    }
)

from . import globals as g  # noqa: E402

__all__ = ["__version__", "__url__", "g", "i18n"]
