from functools import wraps
from .io_functions import ask_for_repeat

def repeating_program(foo: callable) -> callable:

    @wraps(foo)
    def wrapper(*args, **kwargs):
        while True:
            foo(*args, **kwargs)
            if not ask_for_repeat():
                break

    return wrapper