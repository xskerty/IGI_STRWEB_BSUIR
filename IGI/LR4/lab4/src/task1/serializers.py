import csv
import pickle
from abc import ABC, abstractmethod
from typing import Dict

from .models import RationalNumberRepository, RationalNumber


class RationalNumberFileHandler(ABC):
    
    @abstractmethod
    def save(self, repo: RationalNumberRepository, filename: str): ...
    
    @abstractmethod
    def load(self, repo: RationalNumberRepository, filename: str): ...


class PickleRationalNumberFileHandler(RationalNumberFileHandler):
    
    def save(self, repo: RationalNumberRepository, filename: str):
        with open(filename, 'wb') as file:
            pickle.dump(repo.numbers, file)
    
    def load(self, repo: RationalNumberRepository, filename: str):
        with open(filename, 'rb') as file:
            numbers_dict = pickle.load(file)
        repo._numbers = numbers_dict


class CSVRationalNumberFileHandler(RationalNumberFileHandler):
    
    def save(self, repo: RationalNumberRepository, filename: str):

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Key', 'Numerator', 'Denominator'])
            for key, num in repo.numbers.items():
                writer.writerow([key, num.numerator, num.denominator])
    
    def load(self, repo: RationalNumberRepository, filename: str):

        repo.clear()
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader, start=1):
                try:
                    key = row.get('Key', f'number{i}')
                    numerator = int(row['Numerator'])
                    denominator = int(row['Denominator'])
                    repo.add_number(key, RationalNumber(numerator, denominator))
                except (ValueError, KeyError) as e:
                    print(f"Error processing row {row}: {e}")