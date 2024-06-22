from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass(unsafe_hash=True)
class AnswerOption:
    text: str = field(compare=False)
    comment: str = field(compare=False)
    criteria: str = field(compare=False)
    _tm: datetime = field(compare=False)
    _id: str = field(default_factory=uuid4)


@dataclass(unsafe_hash=True)
class FormItem:
    text: str = field(compare=False)
    description: str = field(compare=False)
    options: list[AnswerOption] = field(compare=False)
    _tm: datetime = field(compare=False)
    _id: str = field(default_factory=uuid4)
