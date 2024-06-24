from dataclasses import dataclass

from src.app.common.editable_data_model import EditableDataModel


@dataclass
class AnswerOption(EditableDataModel):
    short: str
    info: str
    criteria: str


@dataclass
class FormGroup(EditableDataModel):
    short: str
    info: str


@dataclass
class FormItem(EditableDataModel):
    text: str
    description: str
    active: list[AnswerOption]
    disabled: list[AnswerOption]
    is_reversed: bool  # last is the best

    def is_first_option(self, opt: AnswerOption):
        return opt in self.active and len(self.active) > 1 and opt == self.active[0]

    def is_last_option(self, opt: AnswerOption):
        return opt in self.active and len(self.active) > 1 and opt == self.active[-1]

    def is_best_option(self, opt: AnswerOption):
        return (
            self.is_last_option(opt) if self.is_reversed else self.is_first_option(opt)
        )

    def is_worst_option(self, opt: AnswerOption):
        return (
            self.is_first_option(opt) if self.is_reversed else self.is_last_option(opt)
        )


@dataclass
class FormContent(EditableDataModel):
    title: str
    description: str
    groups: dict[FormGroup | None, list[FormItem]]
