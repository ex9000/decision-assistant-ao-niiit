from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import overload, Union

import numpy as np

from src.common import number
from src.probability import Probability


class Measure(Enum):
    POSSIBILITY = auto()
    NECESSITY = auto()


class Fuzzy(ABC):
    @overload
    def to_random(self, alpha: float, measure: Measure) -> Probability: ...
    @overload
    def to_random(self, beta: float) -> Probability: ...
    @abstractmethod
    def to_random(self, *args, **kwargs): ...
    @abstractmethod
    def __add__(self, other: Union[number, Probability]) -> "Fuzzy": ...
    @abstractmethod
    def __sub__(self, other: Union[number, Probability]) -> "Fuzzy": ...
    @abstractmethod
    def __mul__(self, other: Union[number, Probability]) -> "Fuzzy": ...
    @abstractmethod
    def __radd__(self, other: Union[number, Probability]) -> "Fuzzy": ...
    @abstractmethod
    def __rsub__(self, other: Union[number, Probability]) -> "Fuzzy": ...
    @abstractmethod
    def __rmul__(self, other: Union[number, Probability]) -> "Fuzzy": ...
    @abstractmethod
    def __neg__(self) -> "Fuzzy": ...
    @abstractmethod
    def __truediv__(self, other: number) -> "Fuzzy": ...


class TriangleSymmetric[T: Probability](Fuzzy):
    __slots__ = "left", "right", "mode", "shift", "scale"

    def __init__(self, mode, fuzziness, shift: T = None, scale: T = None):
        self.left = mode - fuzziness / 2
        self.right = mode + fuzziness / 2
        self.mode = mode

        self.shift: T | None = shift
        self.scale: T | None = scale

    @property
    def fuzziness(self):
        return self.right - self.left

    def __mul__(self, other: Union[number, Probability]) -> "Fuzzy":
        assert isinstance(other, Probability) or isinstance(other, number)

        if isinstance(other, Probability):
            assert self.scale is None and self.shift is None
            return TriangleSymmetric(self.mode, self.fuzziness, self.shift, other)

        if isinstance(other, number):
            shift = (self.shift * other) if self.shift is not None else None
            return TriangleSymmetric(
                self.mode * other, self.fuzziness * abs(other), shift, self.scale
            )

    def __rmul__(self, other: Union[number, Probability]) -> "Fuzzy":
        return self.__mul__(other)

    def __add__(self, other: Union[number, Probability]) -> "Fuzzy":
        assert isinstance(other, Probability) or isinstance(other, number)

        if isinstance(other, Probability):
            assert self.shift is None
            return TriangleSymmetric(self.mode, self.fuzziness, other, self.scale)

        if isinstance(other, number):
            assert self.scale is None
            return TriangleSymmetric(
                self.mode + other, self.fuzziness, self.shift, self.scale
            )

    def __radd__(self, other: Union[number, Probability]) -> "Fuzzy":
        return self.__add__(other)

    def __sub__(self, other: Union[number, Probability]) -> "Fuzzy":
        return self + (-other)

    def __rsub__(self, other: Union[number, Probability]) -> "Fuzzy":
        return -self + other

    def __neg__(self) -> "Fuzzy":
        return self * -1

    def __truediv__(self, other: number) -> "Fuzzy":
        return self * (1 / other)

    def _produce_random(self, factor: float) -> Probability:
        assert self.shift is not None or self.scale is not None

        if self.scale is None:
            return self.shift

        if self.shift is None:
            return self.scale * factor

        return self.shift + self.scale * factor

    @overload
    def to_random(self, alpha: float, measure: Measure) -> Probability: ...
    @overload
    def to_random(self, beta: float) -> Probability: ...

    def to_random(self, alpha: float, measure: Measure = None) -> Probability:
        match measure:
            case None | Measure.POSSIBILITY:
                beta = alpha
            case Measure.NECESSITY:
                beta = alpha - 1
            case _:
                raise ValueError(f"Unknown measure {measure}")

        val: float = np.interp(beta, (-1, 1), (self.left, self.right))
        return self._produce_random(val)
