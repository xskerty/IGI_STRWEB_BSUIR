from src import ITask, Task1, Task2, Task3, Task4, Task5


class Menu(object):
    def __init__(self):
        self.tasks: dict[str, ITask] = {
            '1': Task1(filepath='data/numbers'),
            '2': Task2(original_text_path='data/text.txt',
                       filepath='data/final_text.txt',
                       archive_path='data/final_text.zip'),
            '3': Task3(directory='data/'),
            '4': Task4(directory='data/'),
            '5': Task5()
        }

    def show(self):
        while True:
            choice = input('Complete task - 1..5\nExit - 0\n').strip()
            match choice:
                case cmd if cmd in self.tasks:
                    self.tasks[cmd].run()
                case '0':
                    break
                case _:
                    print('Invalid choice.')


if __name__ == '__main__':
    menu = Menu()
    menu.show()
