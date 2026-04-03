"""Tests for ThemeManager runtime theming APIs."""

import json

import pytest

from uinex.core.exceptions import ThemeError
from uinex.theme.manager import ThemeManager


class TestThemeManager:
    def test_reset_theme_restores_defaults(self):
        ThemeManager.reset_theme()
        defaults = ThemeManager.get_default_theme()

        ThemeManager.update_theme({"Button": {"background": [1, 2, 3]}})
        assert ThemeManager.theme["Button"]["background"] == [1, 2, 3]

        ThemeManager.reset_theme()
        assert ThemeManager.theme["Button"]["background"] == defaults["Button"]["background"]

    def test_update_theme_deep_merges_nested_data(self):
        ThemeManager.reset_theme()
        original = ThemeManager.get_default_theme()

        ThemeManager.update_theme(
            {
                "Entry": {
                    "focused": {"bordercolor": "#FF0000"},
                }
            }
        )

        assert ThemeManager.theme["Entry"]["focused"]["bordercolor"] == "#FF0000"
        assert ThemeManager.theme["Entry"]["focused"]["foreground"] == original["Entry"]["focused"]["foreground"]

    def test_update_theme_requires_dictionary(self):
        ThemeManager.reset_theme()
        with pytest.raises(ThemeError):
            ThemeManager.update_theme("invalid")

    def test_save_theme_to_custom_path(self, tmp_path):
        ThemeManager.reset_theme()
        ThemeManager.update_theme({"Label": {"background": [12, 22, 32]}})

        output = tmp_path / "saved_theme.json"
        ThemeManager.save_theme(str(output))

        assert output.exists()
        content = json.loads(output.read_text())
        assert content["Label"]["background"] == [12, 22, 32]

    def test_load_theme_from_custom_path_deep_merge(self, tmp_path):
        custom_theme = {
            "Entry": {
                "focused": {
                    "background": "#123456",
                }
            }
        }
        theme_path = tmp_path / "custom_theme.json"
        theme_path.write_text(json.dumps(custom_theme), encoding="utf-8")

        ThemeManager.load_theme(str(theme_path))

        assert ThemeManager.theme["Entry"]["focused"]["background"] == "#123456"
        assert "foreground" in ThemeManager.theme["Entry"]["focused"]


@pytest.fixture(autouse=True)
def _reset_theme_between_tests():
    ThemeManager.reset_theme()
    yield
    ThemeManager.reset_theme()
