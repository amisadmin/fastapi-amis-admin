__version__ = "0.4.1"
__url__ = "https://github.com/amisadmin/fastapi_amis_admin"

import gettext
import os

from .utils.translation import i18n

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

i18n.load_translations(
    {
        "zh_CN": gettext.translation(
            domain="messages",
            localedir=os.path.join(BASE_DIR, "locale"),
            languages=["zh_CN"],
        ),
        "de_DE": gettext.translation(
            domain="messages",
            localedir=os.path.join(BASE_DIR, "locale"),
            languages=["de_DE"],
        ),
    }
)
