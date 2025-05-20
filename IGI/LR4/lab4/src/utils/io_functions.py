def input_with_validating(validator: callable, msg: str = '', repeat: bool = True):
    while repeat:
        value = input(msg)
        if validate_any_input(value, validator):
            return value
        print('Invalid input.')


def validate_any_input(value, validator: callable) -> bool:
    try:
        result = validator(value)
        if isinstance(result, bool):
            return result
        return True
    except Exception:
        return False


def ask_for_repeat() -> bool:
    choice = input("Reload this task? (y/n): ").lower()
    return True if choice == 'y' else False
