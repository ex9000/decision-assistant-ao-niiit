from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import overload, Union

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
    __slots__ = "mode", "diameter"

    def __init__(self, mode: T, diameter: T):
        self.mode = mode
        self.diameter = diameter

    @property
    def fuzziness(self):
        return 2 * self.diameter.to_scipy_stat().mean()

    def __mul__(self, other: Union[number, T]) -> "TriangleSymmetric":
        if isinstance(other, Probability) or isinstance(other, number):
            return TriangleSymmetric(self.mode * other, self.diameter * other)

        return NotImplemented

    def __rmul__(self, other: Union[number, T]) -> "TriangleSymmetric":
        return self.__mul__(other)

    def __add__(self, other: Union[number, T]) -> "TriangleSymmetric":
        if isinstance(other, Probability) or isinstance(other, number):
            return TriangleSymmetric(self.mode + other, self.diameter)

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
        return self.mode + self.diameter * factor / 2

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

        return self._produce_random(beta)
