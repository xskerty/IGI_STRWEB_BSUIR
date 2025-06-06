import math
from mathematics import find_n_for_series, find_sum_after_min_abs_elem
from utils import input_with_validating, generate_int, clear_screen
from string_handler import split_text, count_lowercase_consonant_words, count_words_with_max_length, words_before_punctuation, find_longest_word_ending_with_e

@clear_screen
def task1():

    x = float(input_with_validating(lambda i: -40 < float(i) < 40, 'Enter the value of x(-40, 40) :'))
    eps = float(input_with_validating(lambda i: 0.00001 <= float(i) < 1, 'Enter the value of eps [0.00001, 1) :'))

    f_x, n = find_n_for_series(eps, x)
    result_lst = (x, n, f_x, math.exp(x), eps)

    print(result_lst)

@clear_screen
def task2():
    numbers = []
    generated_numbers = []
    generating_way = int(input_with_validating(lambda i: 0 <= int(i) <= 1, '0 - Generate array, 1 - Input: '))
    n = 0 
    while n <= 100:
        if generating_way == 0:
            x = next(generate_int(0, 100))
        else:
            x = int(input_with_validating(lambda i: 0 <= int(i) <= 100, 'enter number from 0 to 100 : ' ))
        numbers.append(x)
        print(f'{n} + {x} = {n+x}')
        n += x

    print(f'Array: {numbers}')
    
    print(f'Result: {n}')

@clear_screen
def task3():
    string = input('Enter text: ')
    print(f'The number of words starting with a lowercase consonant: {count_lowercase_consonant_words(string)}')
    
@clear_screen
def task4():

    text = ('So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy '
              'and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and '
              'picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.')
    words = split_text(text)

    print(f'Count of words with max length : {count_words_with_max_length(words)}')
    print(f"Words before , or . : {words_before_punctuation(text) or 'no such words'}")
    print(f'Longest word ending with e : {find_longest_word_ending_with_e(words) or 'no such words'}')
    
@clear_screen
def task5():
 
    numbers = input_with_validating(lambda s: tuple(map(float, s.strip().split())),
                                    'Enter the list (separated by space): ')
    numbers = tuple(map(float, numbers.strip().split()))

    sum_after_min_abs_elem = find_sum_after_min_abs_elem(numbers)

    print(f'Count of zeros: {numbers.count(0)}' )
    print(f'Sum of elements located after the minimum modulo element: {sum_after_min_abs_elem}' 
          if sum_after_min_abs_elem is not None
          else 'Minimum modulo element is the last one in list')


def menu():
    
   
    while True:
        print('1 - Calculate the value of the function e^x \n2 - Summing numbers up to 100 \n3 - Count the number of words starting with a lowercase consonant letter \n4 - process the given text: \n a) determine how many words have the maximum length\n b) print all the words followed by a comma or period\n c) find the longest word that ends with "e"" \n5 - Find the number of list elements equal to 0 and the sum of the list elements located after the minimum modulo element \n0 - exit')
        choice = int(input_with_validating(lambda i: 0 <= int(i) <= 5))
        match choice:
            case 1:
                task1()
            case 2:
                task2()
            case 3:
                task3()
            case 4:
                task4()
            case 5:
                task5()
            case 0:
                return
                



if __name__ == '__main__':
    menu()