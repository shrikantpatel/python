class A:
    def hello(self):
        print("A.hello")

class B(A):
    def hello(self):
        print("B.before")
        super().hello()
        print("B.after")

class C(A):
    def hello(self):
        print("C.before")
        super().hello()
        print("C.after")

class D(B, C):  # multiple inheritance: D inherits from B and C, order matters
#class D(C, B):  # multiple inheritance: D inherits from C and B, order matters
    def hello(self):
        print("D.before")
        super().hello()  # follows MRO (C3 linearization)
        print("D.after")

if __name__ == "__main__":
    d = D()
    d.hello()
    

# MRO = Method Resolution Order.
# It’s the order Python uses to look up attributes/methods on a class in presence of inheritance.
# For multiple inheritance Python uses the C3 linearization algorithm to produce a consistent, monotonic order.
# super() follows the MRO to find the “next” method.
    print("MRO:", [cls.__name__ for cls in D.__mro__])