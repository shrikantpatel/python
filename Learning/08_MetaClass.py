# Metaclass = “class of a class” — it controls how classes are created. The default metaclass is type; you can provide a custom metaclass to customize class creation (inject attributes/methods, enforce constraints, auto-register classes, etc.). Common uses: ORMs, registries, ABCMeta (abstract base classes).

# Key points

# A metaclass is called when a class statement is executed.
# Implement hooks in the metaclass via new and/or init to change the class object being created.
# Set with: class C(metaclass=MyMeta): ...
# type is the usual metaclass; abc.ABCMeta is used for abstract base classes.

# When to use
# - Use metaclasses sparingly — prefer class decorators or simple base classes unless you need class-creation-time control.
# - Metaclasses are powerful for framework-level APIs (ORMs, registries, enforcing invariants).

class RequiresNameMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        # only enforce NAME on subclasses (skip root/base declarations with no explicit bases)
        if bases and not getattr(cls, "NAME", None):
            raise TypeError(f"{name} must define a NAME class attribute")

class PluginBase(metaclass=RequiresNameMeta):
    pass

# valid
class GoodPlugin(PluginBase):
    NAME = "good"

# invalid -> raises TypeError
class BadPlugin(PluginBase):
    pass