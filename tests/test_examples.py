"""Smoke tests for example modules."""

import importlib


def test_example_modules_importable():
    modules = [
        "examples.simple",
        "examples.showcase",
        "examples.customization",
        "examples.theming",
        "examples.ui_samples",
    ]

    for module_name in modules:
        module = importlib.import_module(module_name)
        assert module is not None
