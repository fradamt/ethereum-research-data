"""Sample Python module for testing tree-sitter parser."""

import os  # noqa: F401 — intentional test data for parser import extraction
from pathlib import Path  # noqa: F401


def simple_function(x: int) -> int:
    """A simple function."""
    return x + 1


def _private_helper():
    pass


class MyClass:
    """A sample class."""

    def __init__(self, value: int):
        self.value = value

    def get_value(self) -> int:
        """Return the value."""
        return self.value

    @staticmethod
    def create(value: int) -> "MyClass":
        return MyClass(value)
