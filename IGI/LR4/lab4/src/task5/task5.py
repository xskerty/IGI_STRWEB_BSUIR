from .math_models import MatrixProcessor
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program
from ..itask import ITask


class Task5(ITask):

    @repeating_program
    def run(self):

        try:
            n = int(input_with_validating(lambda x: int(x) > 0, 'Enter n: '))
            m = int(input_with_validating(lambda x: int(x) > 0, 'Enter m: '))

            processor = MatrixProcessor(n, m)
            print("Original matrix:\n", processor.matrix)

            processed_matrix = processor.process_matrix()
            print("Processed matrix:\n", processed_matrix)

            median_func, median_formula = processor.compute_median()
            print("Median with numpy method:", round(median_func, 2))
            print("Median with formula:", round(median_formula, 2))

        except Exception as e:
            print(e)
