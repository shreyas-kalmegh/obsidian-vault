# Python Patterns: Practical Notes

## Quick Reference Table

| Pattern | Best For | Core Tooling |
|---|---|---|
| Classes/OOP | Stateful domain models | `class`, methods, `super()` |
| Dataclasses | Lightweight typed records | `@dataclass`, `field(default_factory=...)` |
| Decorators | Cross-cutting behavior | `functools.wraps` |
| Closures | Function factories + private state | `nonlocal` |
| Iterators/Generators | Lazy streaming and pipelines | `__iter__`, `__next__`, `yield` |
| File I/O | Reliable read/write | `with open(...)` |
| JSON/CSV | Data interchange | `json`, `csv` |
| CLI scripts | Command-line tools | `argparse` |

---

## 1) Classes and Objects

Use classes to bundle state + behavior.

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount
```

Notes:
- Prefer small, focused classes.
- Validate in `__init__` when invariants matter.

Gotchas:
- Class attributes are shared across instances.

```python
class Bad:
    items = []  # shared by all instances
```

---

## 2) Inheritance and Composition

Use inheritance for clear "is-a" relationships; composition for "has-a".

```python
class Animal:
    def speak(self) -> str:
        return "..."

class Dog(Animal):
    def speak(self) -> str:
        return "woof"
```

```python
class Engine:
    def start(self):
        return "started"

class Car:
    def __init__(self):
        self.engine = Engine()  # composition
```

Notes:
- Favor composition unless inheritance clearly simplifies design.
- Use `super()` in overridden methods when parent init/behavior is required.

---

## 3) Dataclasses

Great for data containers.

```python
from dataclasses import dataclass, field

@dataclass
class User:
    id: int
    name: str
    tags: list[str] = field(default_factory=list)
```

Why useful:
- Auto-generates `__init__`, `__repr__`, comparisons.

Gotchas:
- Never use mutable defaults directly (`tags=[]` is bad).
- Use `frozen=True` for immutable records.

---

## 4) File I/O (`with open`)

Always use context managers.

```python
# write
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("hello\n")

# read entire
with open("notes.txt", "r", encoding="utf-8") as f:
    text = f.read()

# line by line
with open("notes.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.rstrip())
```

Modes:
- `r` read, `w` truncate+write, `a` append, `x` create new
- `b` for binary (e.g., images)

Gotchas:
- `w` overwrites existing file.
- Always specify `encoding` for text files.

---

## 5) Decorators

Wrap function behavior without modifying function body.

```python
from functools import wraps

def log_call(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

@log_call
def add(a, b):
    return a + b
```

Notes:
- Use `@wraps` to preserve function metadata.

Gotchas:
- Decorator order matters when stacking multiple decorators.

---

## 6) Closures

Inner function remembers outer variables.

```python
def make_multiplier(factor: int):
    def mul(x: int) -> int:
        return x * factor
    return mul

triple = make_multiplier(3)
print(triple(4))  # 12
```

Stateful closure:

```python
def counter():
    c = 0
    def inc():
        nonlocal c
        c += 1
        return c
    return inc
```

Gotcha:
- Need `nonlocal` to mutate captured outer variables.

---

## 7) Iterators and Iterables

- Iterable: can be looped (`__iter__`)
- Iterator: yields next items (`__next__`)

```python
nums = [1, 2, 3]
it = iter(nums)
print(next(it))  # 1
```

Custom iterator:

```python
class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val
```

Gotcha:
- Iterators are usually one-pass.

---

## 8) Generators

Lazy sequence generation with `yield`.

```python
def squares(n):
    for i in range(n):
        yield i * i

for x in squares(5):
    print(x)
```

Generator expression:

```python
total = sum(x * x for x in range(1_000_000))
```

Why useful:
- Memory efficient for large streams.

Gotcha:
- Once consumed, generator is exhausted.

---

## 9) JSON Handling

```python
import json

payload = {"id": 1, "name": "ana"}
text = json.dumps(payload)                  # dict -> JSON string
obj = json.loads(text)                      # JSON string -> dict

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=2)

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

Custom encoder/decoder for `datetime` and `Decimal`:

```python
import json
from datetime import datetime
from decimal import Decimal


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return {"__type__": "datetime", "value": obj.isoformat()}
        if isinstance(obj, Decimal):
            # Keep decimal precision by storing as string
            return {"__type__": "decimal", "value": str(obj)}
        return super().default(obj)


def custom_object_hook(d):
    t = d.get("__type__")
    if t == "datetime":
        return datetime.fromisoformat(d["value"])
    if t == "decimal":
        return Decimal(d["value"])
    return d


payload = {
    "amount": Decimal("12.34"),
    "created_at": datetime(2026, 2, 24, 10, 30, 0),
}

text = json.dumps(payload, cls=CustomEncoder)
restored = json.loads(text, object_hook=custom_object_hook)
```

Gotchas:
- JSON keys are strings.
- `datetime`, `Decimal`, and custom objects need custom serialization.
- Avoid converting `Decimal` to `float` if precision matters.
- Use `object_hook` to restore typed objects on load.

---

## 10) CSV Handling

```python
import csv

rows = [
    {"name": "ana", "age": 30},
    {"name": "bob", "age": 28},
]

with open("users.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["name", "age"])
    w.writeheader()
    w.writerows(rows)

with open("users.csv", "r", newline="", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for row in r:
        print(row["name"], row["age"])
```

Gotchas:
- Use `newline=""` when opening CSV files.
- Values are read as strings unless you cast.

---

## 11) CLI Parsing with `argparse`

```python
import argparse

parser = argparse.ArgumentParser(description="Process data")
parser.add_argument("--input", required=True)
parser.add_argument("--limit", type=int, default=100)
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

print(args.input, args.limit, args.verbose)
```

Notes:
- Prefer `type=` for automatic parsing/validation.
- Provide clear help text.

---

## 12) Context Managers (`with`)

Use for deterministic setup/teardown (files, locks, DB sessions).

```python
from contextlib import contextmanager

@contextmanager
def managed_resource():
    print("acquire")
    try:
        yield "resource"
    finally:
        print("release")

with managed_resource() as r:
    print(r)
```

---

## 13) Common Utility Patterns

### EAFP style (Pythonic error handling)

```python
def to_int(s: str, default=0):
    try:
        return int(s)
    except ValueError:
        return default
```

### Enumerate + zip

```python
names = ["a", "b", "c"]
scores = [10, 20, 30]
for i, (n, s) in enumerate(zip(names, scores)):
    print(i, n, s)
```

### Dictionary merge

```python
a = {"x": 1}
b = {"y": 2}
c = a | b
```

---

## 14) High-Value Gotchas

- Mutable default args (`def f(x, acc=[])`) keep state between calls.
- Shadowing built-ins (`list`, `dict`, `sum`) causes bugs.
- `==` vs `is`: value vs identity.
- Float precision issues (`0.1 + 0.2 != 0.3` exactly).
- Catching broad `Exception` can hide real defects.

---

## 15) Selection Cheatsheet

- Structured record-like object: `@dataclass`
- Stream processing large data: generator
- Reusable behavior around functions: decorator
- Stateful function factory: closure
- Sequential data transform pipeline: iterator/generator + comprehensions
- CLI script: `argparse`
- Data interchange: `json`
- Tabular lightweight I/O: `csv`
