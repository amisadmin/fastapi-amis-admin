from functools import lru_cache
from gettext import GNUTranslations
from typing import Dict, Set


class I18N:
    def __init__(self):
        self._locales: Dict[str, Set[GNUTranslations]] = {}
        self._language: str = 'en_US'

    def load_translations(self, translations: Dict[str, GNUTranslations]):
        for language, locale in translations.items():
            if language in self._locales:
                self._locales[language].add(locale)
            else:
                self._locales[language] = {locale}

    def set_language(self, language='zh_CN'):
        assert (not language or language in self._locales), f'{language} language is not exist!'
        self._language = language

    def get_language(self):
        return self._language

    @lru_cache()
    def gettext(self, value: str, language: str = None) -> str:
        language = language or self._language
        if language in self._locales:
            for locale in self._locales[language]:
                if value in locale._catalog:
                    value = locale.gettext(value)
        return value

    def __call__(self, value, language: str = None) -> str:
        return self.gettext(str(value), language)


i18n = I18N()
