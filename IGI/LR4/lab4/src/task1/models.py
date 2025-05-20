from math import gcd
from typing import List, Optional
import json

class JsonSerializationMixin:
    def to_json(self):
        return json.dumps(self.__dict__) 

class RationalNumber(JsonSerializationMixin):

    def __init__(self, numerator: int, denominator: int = 1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        
        self._numerator = numerator 
        self._denominator = denominator 
    
    @property
    def numerator(self) -> int:
        return self._numerator
    
    @property
    def denominator(self) -> int:

        return self._denominator
    
    def __float__(self) -> float:

        return self._numerator / self._denominator
    
    def __str__(self) -> str:
        return f"{self._numerator}/{self._denominator}"


class RationalNumberRepository:

    def __init__(self):
        self._numbers: dict[str, list[RationalNumber]] = {}
    
    @property
    def numbers(self) -> dict[str, RationalNumber]:
        return self._numbers.copy()
    
    @numbers.setter
    def numbers(self, numbers: dict[str, list[RationalNumber]]) -> None:
        self._products = numbers.copy()
    
    def add_number(self, key: str, number: RationalNumber):
        self._numbers[key] = number
    
    def clear(self):
        self._numbers.clear()

    def find_duplicates(self) -> dict[str, List[str]]:
        value_map = {}
    
        for key, num in self._numbers.items():
            value = round(float(num), 10)
        
            if value not in value_map:
                value_map[value] = []
            value_map[value].append(key)
    
        return {
            f"{value:.10f}": keys 
            for value, keys in value_map.items() 
            if len(keys) > 1
        }


    def find_max_number(self) -> Optional[RationalNumber]:
        if not self._numbers:
            return None
         
        max_num = next(iter(self._numbers.values()))
    
        for num in self._numbers.values():
            if (num.numerator * max_num.denominator > 
                max_num.numerator * num.denominator):
                max_num = num
            
        return max_num
        