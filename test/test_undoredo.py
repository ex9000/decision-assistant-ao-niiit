import unittest
from dataclasses import dataclass
from time import sleep

import src.undoredo.limit as limit
from src.undoredo import undoredo


@dataclass
class Data(undoredo(key=id)):
    number: int
    text: str


@dataclass
class ExtraData(Data):
    other_number: int


@dataclass
class DataList(undoredo(key=id)):
    ds: list[Data]


class TestUndoRedo(unittest.TestCase):
    def test_undo(self):
        d = Data(1, "abc")
        d.commit()

        d.number = 100
        d.commit()

        assert d == Data(100, "abc")

        d.undo()
        assert d == Data(1, "abc")

    def test_redo(self):
        d = Data(1, "abc")
        d.commit()

        d.number = 100
        d.commit()

        d.text = "xyz"
        d.commit()

        d.undo()
        d.undo()

        assert d == Data(1, "abc")

        d.redo()
        d.redo()
        assert d == Data(100, "xyz")

    def test_rollback(self):
        e = ExtraData(1, "abc", 2)

        for i in range(1, 10):
            e.number = 100 * i
            e.other_number = 200 * i
            e.commit()
            sleep(0.01)

        sp = e.snapshots()

        e.rollback(sp[-7])
        assert e == ExtraData(700, "abc", 1400)

        e.rollback(sp[-1])
        assert e == ExtraData(100, "abc", 200)

        e.rollback(sp[-6])
        assert e == ExtraData(600, "abc", 1200)

    def test_chain(self):
        """
        a -> b -> c -> a -> x -> y -> b -> p -> q -> y -> z
        """
        d = Data(1, "a")
        d.commit()

        d.text = "b"
        d.commit()

        d.text = "c"
        d.commit()

        d.undo()
        d.undo()

        d.text = "x"
        d.commit()

        d.text = "y"
        d.commit()

        for _ in range(4):
            d.undo()

        d.text = "p"
        d.commit()

        d.text = "q"
        d.commit()

        for _ in range(3):
            d.undo()

        d.text = "z"
        d.commit()

        for x in reversed("abcaxybpqyz"):
            assert x == d.text
            d.undo()

        for x in "abcaxybpqyz":
            assert x == d.text
            d.redo()

    def test_limit(self):
        limit.LIMIT = 10

        d = Data(1, "abc")

        for i in range(95):
            d.number = i
            d.commit()

        vals = [d.number]
        for _ in range(15):
            d.undo()
            vals.append(d.number)

        assert vals == list(reversed(range(80, 95))) + [80]

    def test_nested(self):
        d1 = Data(1, "abc")
        d1.commit()

        d2 = Data(2, "xyz")
        d2.commit()

        dl = DataList([d1, d2])
        dl.commit()

        for i, x in enumerate("one"):
            d1.number = i
            d1.text = x
            d1.commit()

        d1.number = 42
        d1.text = "answer"
        d1.commit()

        dl.commit()

        assert dl.ds[0] == Data(42, "answer")

        dl.undo()
        assert dl.ds[0] == Data(1, "abc")
