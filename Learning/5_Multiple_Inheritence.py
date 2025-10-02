# MRO = Method Resolution Order.
# It’s the order Python uses to look up attributes/methods on a class in presence of inheritance.
# For multiple inheritance Python uses the C3 linearization algorithm to produce a consistent, monotonic order.
# super() follows the MRO to find the “next” method.

# C3 linearization is the algorithm Python uses to compute a class’s MRO (Method Resolution Order) in presence of multiple inheritance. It produces a single, deterministic order that respects:

# local precedence order (the order you list base classes),
# monotonicity (subclasses keep the ordering of their parents), and
# that each class appears before its bases.
# How it works (high level — the merge step)

# Start with sequences: MROs of each direct base, plus the direct-bases list.
# Repeatedly pick the first class (head) of the leftmost sequence that does not appear in the tail (anywhere except the head) of any sequence.
# Append that class to the output and remove it from all sequences.
# If no valid head exists, the hierarchy is inconsistent (no valid MRO).

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
    

    print("MRO:", [cls.__name__ for cls in D.__mro__])