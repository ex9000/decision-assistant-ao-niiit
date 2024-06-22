from dataclasses import dataclass, field
from uuid import UUID, uuid4

from src.undoredo import undoredo


@dataclass
class EditableDataModel(undoredo(key=lambda x: x.uid)):
    uid: UUID = field(default_factory=uuid4, kw_only=True)
