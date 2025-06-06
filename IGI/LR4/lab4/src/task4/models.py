from abc import ABC, abstractmethod



class Figure(ABC):
    @abstractmethod
    def square(self) -> float: ...


class Color:
    def __init__(self, color: str):
        self._color: str = color

    def get_color(self) -> str:
        return self._color

    def set_color(self, value: str):
        self._color = value

    color = property(fget=get_color, fset=set_color)
    

    
class Square(Figure):
    name = 'Square'

    def __init__(self, side: float, color: str):
        self._side: float = side
        self._color: Color = Color(color)

    def __str__(self):
        return f'side: {self._side}, color: {self._color.color}, square: {self.square()}'

    def square(self) -> float:
        return self._side ** 2

    @property
    def side(self) -> float:
        return self._side

    @property
    def color(self) -> str:
        return self._color.color

    @classmethod
    def name_of_class(cls) -> str:
        return cls.name