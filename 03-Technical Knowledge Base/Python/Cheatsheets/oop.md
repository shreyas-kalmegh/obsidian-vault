# Python OOP: Practical Notes

## Quick Reference Table

| Concept | Best For | Core Tooling | Caveat |
|---|---|---|---|
| Classes/Objects | Bundle state + behavior | `class`, `__init__`, methods | Class attrs are shared |
| Inheritance | "is-a" extension | `super()`, method override | Deep hierarchies become brittle |
| Composition | "has-a" assembly | object fields | Preferred over inheritance in many designs |
| Encapsulation | Controlled access | `_name`, `__name`, `@property` | Name mangling is not true private |
| Dataclasses | Boilerplate-free models | `@dataclass`, `field(...)` | Mutable defaults must use `default_factory` |
| Polymorphism | Common interface usage | duck typing, ABCs, `Protocol` | Over-abstraction hurts readability |

---

## 1) Classes and Objects

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
- Keep classes cohesive (single responsibility).
- Prefer explicit invariants in `__init__`.

Gotcha:
- Class attributes are shared by all instances.

```python
class Bad:
    items = []
```

---

## 2) Instance, Class, and Static Methods

```python
class User:
    user_count = 0

    def __init__(self, name: str):
        self.name = name
        User.user_count += 1

    def greet(self) -> str:  # instance method
        return f"hi {self.name}"

    @classmethod
    def total_users(cls) -> int:
        return cls.user_count

    @staticmethod
    def is_valid_name(name: str) -> bool:
        return bool(name and name.strip())
```

When to use:
- Instance method: needs object state (`self`).
- Class method: needs class-level state (`cls`).
- Static method: utility logically grouped with class but no `self/cls`.

---

## 3) Encapsulation: Getters/Setters with `@property`

```python
class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius

    @property
    def celsius(self) -> float:
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self) -> float:
        return (self._celsius * 9 / 5) + 32
```

Notes:
- `@property` lets you keep attribute-style API with validation.
- Leading `_name` means "internal use" by convention.

Gotcha:
- `__name` triggers name mangling (`_ClassName__name`), not strict privacy.

---

## 4) Inheritance and `super()`

```python
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "..."


class Dog(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name)
        self.breed = breed

    def speak(self) -> str:
        return "woof"
```

Notes:
- Override behavior where subclasses differ.
- Call `super()` when parent initialization/logic matters.

Gotcha:
- Prefer composition if inheritance is only for code reuse, not true subtype behavior.

---

## 5) Composition Over Inheritance

```python
class Engine:
    def start(self) -> str:
        return "engine started"


class Car:
    def __init__(self, engine: Engine):
        self.engine = engine

    def drive(self) -> str:
        return self.engine.start() + " -> driving"
```

Why:
- Easier testing (inject dependencies).
- Lower coupling than deep inheritance trees.

---

## 6) `isinstance`, `issubclass`, and Type Checks

```python
class Animal:
    pass

class Dog(Animal):
    pass

x = Dog()
print(isinstance(x, Dog))      # True
print(isinstance(x, Animal))   # True
print(issubclass(Dog, Animal)) # True
```

Guideline:
- Prefer polymorphic behavior over many explicit type checks.
- Use `isinstance` when behavior or validation truly depends on runtime type.

---

## 7) Dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class User:
    id: int
    name: str
    tags: list[str] = field(default_factory=list)
```

Useful options:
- `frozen=True` for immutability.
- `slots=True` (3.10+) for lower memory and faster attribute access.
- `order=True` for generated ordering methods.

Gotcha:
- Never write `tags=[]`; always use `default_factory` for mutables.

---

## 8) Abstract Base Classes (Interfaces via `abc`)

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def put(self, key: str, value: str) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> str:
        pass


class InMemoryStorage(Storage):
    def __init__(self):
        self._d = {}

    def put(self, key: str, value: str) -> None:
        self._d[key] = value

    def get(self, key: str) -> str:
        return self._d[key]
```

Why:
- Enforces required methods in subclasses.
- Makes plugin-like architectures safer.

Gotcha:
- ABCs add ceremony; for lightweight cases duck typing or `Protocol` may be simpler.

---

## 9) Protocols (Structural Interfaces)

```python
from typing import Protocol

class Notifier(Protocol):
    def send(self, msg: str) -> None:
        ...


def alert(n: Notifier, msg: str) -> None:
    n.send(msg)
```

Notes:
- Any class with `send` method matches at type-check time.
- Great for decoupling and testing with fakes.

---

## 10) Dunder Methods (Operator/Representation Hooks)

```python
class Vector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector(x={self.x}, y={self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
```

High-value dunders:
- `__repr__` for debugging
- `__str__` user-friendly print
- `__eq__`, `__lt__` comparisons
- `__len__`, `__iter__` container behavior

---

## 11) Common OOP Design Guidelines

- Keep inheritance shallow.
- Depend on interfaces/Protocols, not concrete classes.
- Favor composition for flexibility.
- Keep mutable state minimal and validated.
- Avoid "god classes" with too many responsibilities.

---

## 12) High-Value Gotchas

- Mutable class attributes shared across instances.
- Forgetting `super().__init__()` in subclasses.
- Property setters causing unexpected side effects.
- Overusing inheritance for code reuse.
- Relying on private name mangling as security.
- Circular imports from tightly coupled class modules.

---

## 13) Selection Cheatsheet

- Data model object with minimal logic: `@dataclass`
- Domain behavior + invariants: class with methods/properties
- Family of interchangeable implementations: ABC/Protocol
- Reuse behavior without subtype relationship: composition
- Shared utility unrelated to instance/class state: `@staticmethod`
