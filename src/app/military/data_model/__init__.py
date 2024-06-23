from dataclasses import dataclass

from src.app.common.editable_data_model import EditableDataModel


@dataclass
class AnswerOption(EditableDataModel):
    short: str
    info: str
    criteria: str
    disabled: bool


@dataclass
class FormGroup(EditableDataModel):
    short: str
    info: str


@dataclass
class FormItem(EditableDataModel):
    text: str
    description: str
    group: FormGroup | None
    options: list[AnswerOption]
    is_negative: bool


@dataclass
class FormContent(EditableDataModel):
    title: str
    description: str
    groups: list[FormGroup]
    items: list[FormItem]
