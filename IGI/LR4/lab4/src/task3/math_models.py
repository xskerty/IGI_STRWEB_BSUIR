import math
from statistics import median, mode, pvariance, pstdev
from typing import Any


class TaylorSeries:

    def __init__(self, series: tuple[float, ...]):
        self._series = series
        self._n = len(series)

    @property
    def n(self):
        return self._n

    def sum(self):
        return 1 + sum(self._series)

    def average_value(self):
        return sum(self._series) / self._n

    def median(self):
        return median(self._series)

    def mode(self):
        return mode(self._series)

    def variance(self):
        return pvariance(self._series)

    def stdev(self):
        return pstdev(self._series)

    def __str__(self):
        return (f'n: {self.n}\n'
                f'F(x): {self.sum()}\n'
                f'Average value: {self.average_value()}\n'
                f'Median: {self.median()}\n'
                f'Mode: {self.mode()}\n'
                f'Variance: {self.variance()}\n'
                f'Stdev: {self.stdev()}')


class TaylorSeriesExp(TaylorSeries):

    def __init__(self, epsilon: float, x: float):
        n = self._find_min_n_for_epsilon(epsilon, x)
        super().__init__(tuple(pow(x, i)/math.factorial(i) for i in range(1, n + 1)))

    @staticmethod
    def _find_min_n_for_epsilon(epsilon: float, x: float) -> int:
        math_result = math.exp(x)
        for num_of_members in range(0, 501):
            result = TaylorSeries(tuple(pow(x, i)/math.factorial(i) for i in range(1, num_of_members + 1)))
            if abs(result.sum() - math_result) <= epsilon:
                return num_of_members
        return 501


class TaylorSeriesExpTable:

    @staticmethod
    def create_table(exp_handler: type[TaylorSeriesExp], eps: float):
        table = []
        for x in range(-300, 300, 3):
            f_x = exp_handler(eps, x * 0.1)
            table.append({
                'x': x * 0.1,
                'n': f_x.n,
                'fx': f_x.sum(),
                'math_f': math.exp(x * 0.1),
                'eps': eps
            })
        return table

    @staticmethod
    def extract_columns(table: list[dict[str, Any]], *column_values: str):
        return tuple(tuple(row[i] for row in table) for i in column_values)