from typing import Callable

# callable that take 1 int and return int
def apply(t: Callable[[int], int], v: int) -> int:
    if not callable(t):
        raise TypeError("t must be callable")
    return t(v)

def inc(x: int) -> int:
    return x + 1

double = lambda x: x * 2  # inferred as Callable[[int], int]

class Adder:
    def __init__(self, n: int): self.n = n
    def __call__(self, x: int) -> int:
        return x + self.n

print(apply(inc, 3))       # 4
print(apply(double, 4))    # 8
print(apply(Adder(5), 2))  # 7


print(callable(inc))         # True
print(callable(double))      # True
print(callable(Adder))       # True (class)
print(callable(Adder(5)))    # True (instance with __call__)

# callaable that take 2 int and return int
def apply1(t: Callable[[int, int], int], v1: int, v2: int) -> int:
    if not callable(t):
        raise TypeError("t must be callable")
    return t(v1, v2)

def inc(x: int, y: int) -> int:
    return x + y

add = lambda x, y: x + y  # inferred as Callable[[int, int], int]

print(apply1(add, 3, 4))       # 7
