from typing import List, Optional, Dict
from .models import RationalNumberRepository, RationalNumber


class RationalNumberService:

    def __init__(self, repository: RationalNumberRepository):
        self._repo = repository

    def contains_number(self, numerator: int, denominator: int = 1) -> bool:
        target = RationalNumber(numerator, denominator)
        return target in self._repo.numbers

    def find_number_info(self) -> List[str]:
        try:
            key = input('Enter number key: ').strip()
        
            if key not in self._repo.numbers:
                return [f"Number with key '{key}' don't exist"]
        
            num = self._repo.numbers[key]
            return [
                f"Key: {key}",
                f"Number: {num.to_json()}",
                f"Decimal Value: {float(num):.4f}",
        ]
        
        except Exception as e:
            raise ValueError(f"Error: {e}")

    def get_all_numbers(self) -> List[RationalNumber]:
        return self._repo.numbers.copy()