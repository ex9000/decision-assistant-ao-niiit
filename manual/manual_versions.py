from dataclasses import dataclass, field
from uuid import uuid4, UUID

import src.undoredo.limit as limit
from src.undoredo import undoredo

limit.LIMIT = 1


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line(undoredo(key=lambda x: x._id)):
    a: Point
    b: Point
    _id: UUID = field(default_factory=lambda: uuid4())


p1 = Point(1, 2)
p2 = Point(3, 4)

line = Line(p1, p2)
line.commit()
print(line)

line.a = Point(10, 20)
line.commit()
print(line)

line.undo()
print(line)

line.b = Point(-3, -4)
line.commit()
print(line)

for _ in range(4):
    line.undo()
    print("undo", line)

for _ in range(4):
    line.redo()
    print("redo", line)
