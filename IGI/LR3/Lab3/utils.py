import random
from msvcrt import getch
from os import system

def clear_screen(func):
    def wrapper(*args, **kwargs):
        system('cls')
        result = func(*args, **kwargs)
        print("Enter any key...")
        getch()  
        system('cls')
        return result
    return wrapper

def generate_int(low_value: int, high_value: int):
    while True:
        yield random.randint(low_value, high_value)

def validate_any_input(value, validator: callable) -> bool:
    try:
        result = validator(value)
        if isinstance(result, bool):
            return result
        return True
    except Exception:
        return False
    
def input_with_validating(validator: callable, msg: str = ''):
    while True:
        value = input(msg)
        if validate_any_input(value, validator):
            return value
        print('Invalid input. Try again.')