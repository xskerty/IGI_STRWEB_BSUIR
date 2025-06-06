from .models import Square
from .services import SquareManager
from ..task3.task3 import Drawer
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program
from ..itask import ITask
from math import sqrt


class Task4(ITask):

    def __init__(self, directory: str):
        self._directory = directory

    @staticmethod
    def input_figure():

        a = float(input_with_validating(lambda i: float(i) > 0, 'Enter radius: '))*(sqrt(2))
        color = input('Enter figure color : ').strip().lower()

        return a, color

    @repeating_program
    def run(self):

        try:
            square_manager = SquareManager(self._directory, Drawer())
            square = Square(*self.input_figure())

            print(square.name_of_class() + ': ' + str(square))
            square_manager.draw_square(square)
        except Exception as e:
            print(e)