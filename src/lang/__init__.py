from enum import Enum, auto


class Lang(Enum):
    US = auto()
    RU = auto()


_current_lang = Lang.US
_order_lang = (Lang.US, Lang.RU)


def switch_lang(lang: Lang):
    global _current_lang
    _current_lang = lang


class Translation(str):
    def __new__(cls, *translations: str):
        x = super().__new__(cls)
        x.__init__(*translations)
        return x

    def __init__(self, *translations: str):
        assert len(translations) == len(_order_lang)
        self._translations = dict(zip(_order_lang, translations))

    def __str__(self):
        return self._translations[_current_lang]

    def __repr__(self):
        return str(self)

    def __getattribute__(self, __name):
        if __name.startswith("_"):
            return super().__getattribute__(__name)

        return getattr(str(self), __name)


K_PESSIMISTIC = Translation("pessimistic", "пессимистичный")
K_OPTIMISTIC = Translation("optimistic", "оптимистичный")
K_EXPECTED = Translation("expected", "ожидаемый")
K_EFFECTIVENESS = Translation("effectiveness", "эффективность")
K_POSSIBILITY = Translation("possibility", "возможность")
