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

    def __mul__(self, other: Union[number, T]) -> "TriangleSymmetric":
        if isinstance(other, Probability):
            assert self.scale is None and self.shift is None
            return TriangleSymmetric(self.mode, self.fuzziness, self.shift, other)

        if isinstance(other, number):
            shift = (self.shift * other) if self.shift is not None else None
            return TriangleSymmetric(
                self.mode * other, self.fuzziness * abs(other), shift, self.scale
            )

        return NotImplemented

    def __rmul__(self, other: Union[number, T]) -> "TriangleSymmetric":
        return self.__mul__(other)

    def __add__(self, other: Union[number, T]) -> "TriangleSymmetric":
        if isinstance(other, Probability):
            assert self.shift is None
            return TriangleSymmetric(self.mode, self.fuzziness, other, self.scale)

        if isinstance(other, number):
            if np.isclose(other, 0, atol=1e-8):
                return self

            assert self.scale is None
            return TriangleSymmetric(
                self.mode + other, self.fuzziness, self.shift, self.scale
            )

        return NotImplemented

    def __radd__(self, other: Union[number, T]) -> "TriangleSymmetric":
        return self.__add__(other)

    def __sub__(self, other: Union[number, T]) -> "TriangleSymmetric":
        return self + (-other)

    def __rsub__(self, other: Union[number, T]) -> "TriangleSymmetric":
        return -self + other

    def __neg__(self) -> "TriangleSymmetric":
        return self * -1

    def __truediv__(self, other: number) -> "TriangleSymmetric":
        return self * (1 / other)

    def _produce_random(self, factor: float) -> T:
        assert self.shift is not None or self.scale is not None

        if self.scale is None:
            return self.shift

        if self.shift is None:
            return self.scale * factor

        return self.shift + self.scale * factor

    @overload
    def to_random(self, alpha: float, measure: Measure) -> T: ...
    @overload
    def to_random(self, beta: float) -> T: ...

    def to_random(self, alpha: float, measure: Measure = None) -> T:
        """
        It is not correct to say `convert` fuzzy-value using measure.
        ! It is STRONGLY ASSUMED that given random-value will be used to compare it GREATER OR EQUAL with some level.

        pi {FUZZY >= level} >= alpha
        nu {FUZZY >= level} >= alpha

        beta -- is seamless transition from nu to pi. (their common point nu(0) == pi(1)).
        beta [-1 .. 0] ~ nu [1 .. 0]
        beta [0 .. 1] ~ pi [1 .. 0]
        """
        match measure:
            case None:
                beta = alpha
            case Measure.POSSIBILITY:
                beta = 1 - alpha
            case Measure.NECESSITY:
                beta = -alpha
            case _:
                raise ValueError(f"Unknown measure {measure}")

        val: float = np.interp(beta, (-1, 1), (self.left, self.right))
        return self._produce_random(val)
