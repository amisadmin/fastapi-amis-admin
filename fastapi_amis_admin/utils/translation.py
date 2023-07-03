import gc
import locale
import os
from functools import lru_cache
from gettext import GNUTranslations
from typing import Dict, Set


class I18N:
    def __init__(self):
        self._locales: Dict[str, Set[GNUTranslations]] = {}
        self._language: str = self.set_language()

    def load_translations(self, translations: Dict[str, GNUTranslations]):
        for language, trans in translations.items():
            if language in self._locales:
                self._locales[language].add(trans)
            else:
                self._locales[language] = {trans}

    def set_language(self, language: str = None) -> str:
        """
        Set the i18n localization language. If it is empty, try to read the environment variable `LANGUAGE`/`LANG`,
        the system default language, in turn.
        :param language: the language to try to set
        :return: the language after the successful setting
        """
        language = language or os.getenv("LANGUAGE") or os.getenv("LANG") or locale.getlocale()[0] or "en_US"
        self._language = "zh_CN" if language.lower().startswith(("zh", "chinese")) else language
        I18N.gettext.cache_clear()  # clear cache after language has changed
        gc.collect()
        return self._language

    def get_language(self):
        return self._language

    @lru_cache()  # noqa: B019
    def gettext(self, value: str, language: str = None) -> str:
        language = language or self._language
        if language in self._locales:
            for trans in self._locales[language]:
                # noinspection PyProtectedMember
                if value in trans._catalog:  # type: ignore
                    value = trans.gettext(value)
        return value

    def __call__(self, value, language: str = None) -> str:
        return self.gettext(str(value), language)


i18n = I18N()
