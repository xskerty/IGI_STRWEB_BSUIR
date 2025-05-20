from .drawer import Drawer
from .math_models import TaylorSeries, TaylorSeriesExp, TaylorSeriesExpTable
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program
from ..itask import ITask


class Task3(ITask):

    X_START, X_END, X_STEP = -99, 99, 1

    def __init__(self, directory: str):
        self._exp_handler = TaylorSeriesExp
        self._table = None
        self._table_manager = TaylorSeriesExpTable
        self._directory = directory
        self._drawer = Drawer()

    @repeating_program
    def run(self):

        try:
            x, eps = self._input_values()

            series = self._exp_handler(eps, x)
            print(series)

            self._table = self._table_manager.create_table(self._exp_handler, eps)
            self._plot_ln()
            self._plot_n()
        except Exception as e:
            print(e)

    def _plot_ln(self):
        """Plots the graphs of the natural logarithm using the Taylor series and the math.log function."""

        x, y_taylor, y_math = self._table_manager.extract_columns(self._table, 'x', 'fx', 'math_f')

        self._drawer.plot_table(((x, y_taylor), (x, y_math)), ('x', 'y'),
                                ('y = taylor_ln(x)', 'y = math_ln(x)'),
                                'Comparison of exponent graphs using Taylor series and math',
                                f'{self._directory}exp_graphics.png')

    def _plot_n(self):
        """Plots the dependence of the number of terms on x."""

        x, n = self._table_manager.extract_columns(self._table, 'x', 'n')

        self._drawer.plot_table(((x, n),), ('x', 'n'), ('n(x)',),
                                'Dependence of the number of Taylor series terms on x',
                                f'{self._directory}n_graphics.png')

    @staticmethod
    def _input_values():
        """Prompts the user to input x and eps with validation."""

        x = float(input_with_validating(lambda i: abs(float(i)) < 40 ,'Enter the value of x: (-40, 40): '))
        eps = float(input_with_validating(lambda i: 1 > float(i) > 0.00001, 'Enter the value of eps: (0.00001, 1): '))
        return x, eps
            