""" Mixins are small, focused classes that provide reusable behavior to other classes via multiple inheritance. They are not meant to stand alone (usually not instantiated); instead you "mix" them into concrete classes to add methods or behavior.

Key points

* Single responsibility: one behavior per mixin (e.g., logging, serialization, timestamps).
* Put mixins before the concrete base class in the bases list (so MRO picks them up).
* Use cooperative super() if the mixin overrides a method that other classes in the chain may also override.
* Don’t store lots of state in mixins; prefer methods that operate on the host instance.
* Name convention: end mixin class names with "Mixin".
* If multiple mixins override the same method, ensure they call super() to cooperate; otherwise some behavior may be skipped.
* Don’t treat mixins as independent components to instantiate; use them only as part of a concrete subclass.
"""

def current_time():
    from datetime import datetime
    return datetime.utcnow().isoformat()

class LoggingMixin:
    def log(self, msg: str) -> None:
        print(f"[LOG] {msg}")

class TimestampMixin:
    def add_timestamp(self, data: dict) -> dict:
        data["timestamp"] = current_time()
        return data

class BaseModel:
    def save(self, data: dict) -> None:
        print("saving:", data)

# Compose behavior: mixins first, concrete base last
class AuditedModel(TimestampMixin, LoggingMixin, BaseModel):
    def save(self, data: dict) -> None:
        data = self.add_timestamp(data)   # from TimestampMixin
        self.log("about to save")         # from LoggingMixin
        super().save(data)                # call BaseModel.save via MRO

if __name__ == "__main__":
    m = AuditedModel()
    data : dict = {"value": 42}
    m.save(data)