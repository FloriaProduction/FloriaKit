"""Демонстрация валидаторов из FloriaKit.validator."""

from FloriaKit import validator

# -------------------- not_none --------------------
value = "hello"
validated = validator.not_none(value)  # возвращает "hello"
print(validated)

try:
    validator.not_none(None)  # ValueError: Value is None
except ValueError as e:
    print("Caught:", e)

# С кастомным исключением
try:
    validator.not_none(None, exception=TypeError("Custom error"))
except TypeError as e:
    print("Custom exception:", e)

# Со значением по умолчанию
defaulted = validator.not_none(None, default="default_value")
print("Defaulted:", defaulted)  # default_value


# -------------------- is_instance --------------------
number = 42
as_int = validator.is_instance(number, int)  # 42
print("is_instance int:", as_int)

try:
    validator.is_instance("string", int)  # ValueError
except ValueError as e:
    print("Expected error:", e)

# С исключением
try:
    validator.is_instance("string", int, exception=RuntimeError("Not an int"))
except RuntimeError as e:
    print("Custom type error:", e)

# С дефолтом
fallback = validator.is_instance("string", int, default=0)
print("Fallback:", fallback)  # 0


# -------------------- raiser --------------------


try:
    validator.raiser("Just an error message") if True else None
except Exception as e:
    print("raiser str ->", e)

try:
    validator.raiser(ValueError("Detailed error")) if True else None
except ValueError as e:
    print("raiser Exception ->", e)
