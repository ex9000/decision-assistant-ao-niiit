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
K_FRONTIER_SHARES = Translation("frontier with shares", "граница и доли")
K_INCOME = Translation("income", "доходность")
K_RISK = Translation("risk", "риск")
K_TACTICAL_PLANNING = Translation("tactical planning", "тактическое планирование")
K_MENU = Translation("menu", "меню")
K_VIEW = Translation("view", "вид")
K_DARK_MODE = Translation("dark mode", "ночной режим")
K_LOAD_FROM_FILE = Translation("load from file", "загрузить из файла")
K_SAVE_TO_FILE = Translation("save to file", "сохранить в файл")
K_WEAPON = Translation("weapon", "вооружение")
K_TARGET = Translation("target", "цель")
K_DATA_LOADED = Translation("data loaded", "данные загружены")
K_DATA_SAVED = Translation("data saved", "данные сохранены")
K_FIND_SOLUTION = Translation("find solution", "найти решение")
K_ITEM_NUMBER = Translation("item #", "опция №")
K_OLDER = Translation("older", "старее")
K_NEWER = Translation("newer", "новее")
K_SAVE = Translation("save", "сохранить")
K_VERSION = Translation("version", "версия")

K_SHORT_NAME = Translation("short name", "краткое наименование")
K_OPTION_SHORT_NAME_HINT = Translation(
    "the name that will be displayed in the questionnaire",
    "название, которое будет отображено в анкете",
)

K_DESCRIPTION = Translation("description", "описание")
K_OPTION_DESCRIPTION_HINT = Translation(
    "hint that will be displayed in the questionnaire",
    "подсказка, которая будет отображаться в анкете",
)

K_CRITERIA = Translation("criteria", "критерии")
K_OPTION_CRITERIA_HINT = Translation(
    "how do you know if this option is appropriate?",
    "как понять, что данная опция является подходящей?",
)

E_FILE_IS_NOT_EXISTS = Translation(
    "file `{}` does not exists!",
    "файл `{}` не существует!",
)
E_PATH_IS_NOT_A_FILE = Translation("`{}` is not a file!", "`{}` это не файл!")
E_CANNOT_PARSE_FILE = Translation(
    "cannot parse `{}`!",
    "не удалось прочитать файл `{}`!",
)
E_CANNOT_SAVE_FILE = Translation("cannot save `{}`!", "не удалось сохранить файл `{}`!")


class MILITARY:
    class ANSWER_OPTION:
        K_DEFAULT_SHORT_NAME = Translation(
            "excellent",
            "превосходно",
        )
        K_DEFAULT_DESCRIPTION = Translation(
            "extreme positive assessment",
            "крайне положительная оценка",
        )
        K_DEFAULT_CRITERIA = Translation(
            """# Basic criteria
- indicators are at least 90% of the maximum
- it is impossible to achieve greater readiness

### Additional
- the consent of 2 or more persons with this assessment is desirable""",
            """# Основные критерии
- показатели составляют не менее 90% от максимальных
- невозможно достичь большей готовности

### Дополнительно
- желательно согласие 2-х и более лиц с данной оценкой""",
        )


class DISTRIBUTE:
    class SUPPLY:
        K_FILE_NAME = Translation("supplies", "арсенал")

        K_NAME = Translation("name", "наименование")
        K_POTENTIAL = Translation(
            "combat potential [art. shell]",
            "боевой потенциал [арт. снаряд]",
        )
        K_AMOUNT = Translation("available [units]", "доступно [единиц]")
        K_PRICE = Translation("price [mill. per 1 unit]", "стоимость [млн. за 1 ед.]")
        K_ACTIVE = Translation("active [true/false]", "активен [истина/ложь]")

    class TARGET:
        K_FILE_NAME = Translation("targets", "цели")

        K_NAME = Translation("name", "наименование")
        K_HEALTH = Translation("survivability [art. shell]", "живучесть [арт. снаряд]")
        K_PRIORITY = Translation("priority", "приоритет")
        K_ACTIVE = Translation("active [true/false]", "активен [истина/ложь]")

    class SOLUTION:
        K_FILE_NAME = Translation("solution", "решение")

        K_NAME = Translation("name", "наименование")
        K_PRICE = Translation("price", "стоимость")
        K_TOTAL = Translation("total", "итого")
