# Diamond problem: when a class D inherits from B and C, and both B and C inherit from the same base A, the inheritance graph forms a diamond. The questions: which implementation of a method from A should be used, and how often should A.init (or similar) run?

# Python solution

# Python uses C3 linearization (MRO) to compute a single, deterministic order (e.g., D, B, C, A).
# Use cooperative super() in each class so each class’s method runs exactly once, following the MRO.


print("# non-cooperative: A.__init__ may run twice")
class A:
    def __init__(self):
        print("A.__init__")

class B(A):
    def __init__(self):
        print("B.__init__")
        A.__init__(self)    

class C(A):
    def __init__(self):
        print("C.__init__")
        A.__init__(self)

class D(B, C):
    def __init__(self):
        print("D.__init__")
        B.__init__(self)
        C.__init__(self)

D()
# Output:
# D.__init__
# B.__init__
# A.__init__
# C.__init__
# A.__init__   <- A run twice (undesirable)

print("# cooperative: each __init__ calls super() once, A.__init__ runs once")
class A:
    def __init__(self):
        print("A.__init__")

class B(A):
    def __init__(self):
        print("B.__init__")
        super().__init__()        # cooperative

class C(A):
    def __init__(self):
        print("C.__init__")
        super().__init__()        # cooperative

class D(B, C):
    def __init__(self):
        print("D.__init__")
        super().__init__()        # follows MRO (D, B, C, A)

D()
# Output:
# D.__init__
# B.__init__
# C.__init__
# A.__init__    <- A run once (correct)