# square.py
def area(a):
    return a * a

def perimeter(a):
    return 4 * a

if __name__ == "__main__":
    side = float(input("Введите длину стороны квадрата: "))
    print(f"Площадь квадрата: {area(side)}")
    print(f"Периметр квадрата: {perimeter(side)}")