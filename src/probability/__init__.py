from abc import ABC, abstractmethod
from typing import Union

from scipy.stats import rv_continuous, norm

from src.common import number


class Probability(ABC):
    @abstractmethod
    def to_scipy_stat(self) -> rv_continuous: ...
    @abstractmethod
    def __add__(self, other: Union[number, "Probability"]) -> "Probability": ...
    @abstractmethod
    def __sub__(self, other: Union[number, "Probability"]) -> "Probability": ...
    @abstractmethod
    def __mul__(self, other: Union[number, "Probability"]) -> "Probability": ...
    @abstractmethod
    def __radd__(self, other: Union[number, "Probability"]) -> "Probability": ...
    @abstractmethod
    def __rsub__(self, other: Union[number, "Probability"]) -> "Probability": ...
    @abstractmethod
    def __rmul__(self, other: Union[number, "Probability"]) -> "Probability": ...
    @abstractmethod
    def __neg__(self) -> "Probability": ...
    @abstractmethod
    def __truediv__(self, other: Union[number, "Probability"]) -> "Probability": ...


class Normal(Probability):
    __slots__ = "mu", "sigma2"

    def __new__(cls, mean: number = 0, variance: number = 1) -> "Probability":
        if variance == 0:
            return mean

        x = super().__new__(cls)
        x.__init__(mean, variance)
        return x

    def __init__(self, mean: number = 0, variance: number = 1):
        assert variance > 0
        self.mu = mean
        self.sigma2 = variance

    def __mul__(self, other: number) -> "Normal":
        if isinstance(other, number):
            return Normal(self.mu * other, self.sigma2 * abs(other) ** 2)
        else:
            return NotImplemented

    def __rmul__(self, other: number) -> "Normal":
        return self.__mul__(other)

    def __add__(self, other: Union[number, "Normal"]) -> "Normal":
        if isinstance(other, Normal):
            return Normal(self.mu + other.mu, self.sigma2 + other.sigma2)
        elif isinstance(other, number):
            return Normal(self.mu + other, self.sigma2)
        else:
            return NotImplemented

    def __radd__(self, other: Union[number, "Normal"]) -> "Normal":
        return self + other

    def __sub__(self, other: Union[number, "Normal"]) -> "Normal":
        return self + (-other)

    def __rsub__(self, other: Union[number, "Normal"]) -> "Normal":
        return -self + other

    def __neg__(self) -> "Normal":
        return self * -1

    def __truediv__(self, other: number) -> "Normal":
        return self * (1 / other)

    def __eq__(self, other: "Normal") -> bool:
        assert isinstance(other, Normal)
        return self.mu == other.mu and self.sigma2 == other.sigma2

    def __ne__(self, other: "Normal") -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.mu, self.sigma2))

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"𝓝(μ={self.mu}, σ²={self.sigma2})"

    def to_scipy_stat(self) -> rv_continuous:
        return norm(self.mu, self.sigma2 ** 0.5)
