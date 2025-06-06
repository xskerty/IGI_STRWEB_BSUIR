from math import exp, factorial


def calc_exp_using_taylor_series(x: float, n: int) -> float:
    return 1 + sum(pow(x, i) / factorial(i) for i in range(1, n + 1))


def find_n_for_series(epsilon: float, value: float) -> tuple[float, int]:
    result = 0
    math_result = exp(value)
    num_of_members = 1

    for num_of_members in range(1, 501):
        result = calc_exp_using_taylor_series(value, num_of_members)
        if abs(result - math_result) <= epsilon:
            return result, num_of_members

    return result, num_of_members


def calculate_sum_of_odd_indexed_elements(numbers: tuple | list) -> float | None:
    return sum(numbers[1::2]) if len(numbers) >= 2 else None


def find_sum_after_min_abs_elem(numbers: tuple | list) -> float | None:
    min_abs = float('inf')  
    min_abs_index = -1

    for i, num in enumerate(numbers):
        abs_num = abs(num)
        if abs_num < min_abs:
            min_abs = abs_num
            min_abs_index = i

    if min_abs_index == len(numbers) - 1 or min_abs_index == -1:
        return None

    sum_after_min_abs = sum(numbers[min_abs_index + 1:])

    return sum_after_min_abs

  