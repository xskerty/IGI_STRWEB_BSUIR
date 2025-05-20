from .models import RationalNumber, RationalNumberRepository
from .serializers import RationalNumberFileHandler, PickleRationalNumberFileHandler, CSVRationalNumberFileHandler
from .services import RationalNumberService
from ..utils.io_functions import input_with_validating
from ..utils.utils import repeating_program
from ..itask import ITask
from typing import List, Dict


class Task1(ITask):


    def __init__(self, filepath: str):
        self._repo = RationalNumberRepository()
        self._service = RationalNumberService(self._repo)
        self._export_methods: dict[str, RationalNumberFileHandler] = {
            'pickle': PickleRationalNumberFileHandler(),
            'csv': CSVRationalNumberFileHandler()
        }
        self._filepath = filepath

    @repeating_program
    def run(self):
        try:
            self._repo.add_number("number1", RationalNumber(1, 2))
            self._repo.add_number("number2", RationalNumber(3, 4))
            self._repo.add_number("number3", RationalNumber(2, 4))
            self._repo.add_number("number4", RationalNumber(1, 10))
            self._repo.add_number("number5", RationalNumber(10, 1))
            self._repo.add_number("number6", RationalNumber(1, 3))
            self._repo.add_number("number7", RationalNumber(10, 5))
            self._repo.add_number("number8", RationalNumber(3, 2))
            self._repo.add_number("number9", RationalNumber(5, 2))
            self._repo.add_number("number10", RationalNumber(1, 4))
            
            self._export_methods['csv'].save(self._repo, f'{self._filepath}.csv')
            self._export_methods['pickle'].save(self._repo, f'{self._filepath}.pickle')
            
            self._repo.clear()
            
            export_method = input_with_validating(
                lambda msg: msg.lower().strip() in self._export_methods,
                'Choose format (pickle, csv): '
            ).lower().strip()
            
            self._export_methods[export_method].load(
                self._repo, 
                f'{self._filepath}.{export_method}'
            )

            print(f"\nNumbers:")
            for key, num in self._repo.numbers.items():
                print(f"{key}: {str(num)}")
            
            duplicates = self._repo.find_duplicates()
            if duplicates:
                print(f"\nEqual numbers: ")
                for key, num in duplicates.items():
                    print(f"{key}: {num}")
            else:
                print("No equals numbers")
                
            max_element = self._repo.find_max_number()
            print(f"\nMax number: {str(max_element)}")
            
            print(self._service.find_number_info(), sep='\n')
               
        except Exception as e:
            print(f"Error: {e}")
            
