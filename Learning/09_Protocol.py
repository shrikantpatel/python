# Protocol (PEP 544) — short definition

# A Protocol describes an interface by structure (methods/attributes) rather than by inheritance.
# Static type checkers (mypy/pyright) treat an object as matching a Protocol if it has the required members (duck typing).
# Useful when you want to accept “any object that implements X” without forcing subclasses.
# Why use Protocols

# Document expected behavior (interfaces) without coupling to a base class.
# Enable static checking for duck-typed code.
# Create generic, composable APIs that accept any compatible object.

# Protocols are for static (and optionally limited runtime) structural typing — prefer them when you want flexible interfaces.
# Use abc.ABC / abstract methods when you need runtime enforcement, registration, or concrete base behavior.
# For older Python versions install typing_extensions for newer Protocol features.

####################
# Simple example
####################

from typing import Protocol

class Speaker(Protocol):
    def speak(self) -> str: ...

def announce(s: Speaker) -> None:
    print(s.speak())

class Person:
    def speak(self) -> str:
        return "hello"

announce(Person())  # works — Person matches Speaker structurally even though it doesn't inherit

####################
# Protocol with an attribute
####################

class HasName(Protocol):
    name: str

def greet(obj: HasName) -> str:
    return f"hi {obj.name}"

class User:
    def __init__(self, name: str): 
        self.name = name

greet(User("Alice"))  # ok


####################
# Callable Protocol (useful for higher-order APIs)
###################

class Transformer(Protocol):
    def __call__(self, x: int) -> int: ...

def apply(t: Transformer, v: int) -> int:
    return t(v)

apply(lambda x: x + 1, 2)  # OK

####################
# from typing import Protocol, runtime_checkable
###################

from typing import Protocol, runtime_checkable
@runtime_checkable
class Speaker(Protocol):
    def speak(self) -> str: ...

class Person:
    def speak(self) -> str: return "hi"

isinstance(Person(), Speaker)  # may be True (runtime structural check), but use sparingly

####################
# Generic Protocol
###################
from typing import Protocol, TypeVar, Iterator

T = TypeVar("T")

class Container(Protocol[T]):
    def __iter__(self) -> Iterator[T]: ...
    def __len__(self) -> int: ...

def first_item(c: Container[T]) -> T:
    for x in c:
        return x
    raise IndexError("first_item() called on empty container")

# Usage examples (mypy will infer types):
re = first_item([1, 2, 3])    # re: int
rs = first_item(["a", "b"])   # rs: str
print (re)
print (rs)
