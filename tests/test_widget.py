import pygame
import pytest

from uinex.widget.base import Widget


class TestWidget:
    def test_widget_creation(self, screen):
        """Test if the widget can be created."""
        widget = Widget(master=screen, width=200, height=50)
        assert isinstance(widget, Widget)
        assert widget.width == 200
        assert widget.height == 50

    def test_widget_draw(self, screen):
        """Test if the widget can be drawn on the screen."""
        widget = Widget(master=screen, width=200, height=50)
        widget.draw()
        pygame.display.flip()
        # Check if the widget is drawn by checking its rect
        assert widget.rect.width == 200
        assert widget.rect.height == 50

    def test_widget_visibility(self, screen):
        """Test if the widget visibility can be toggled."""
        widget = Widget(master=screen, width=200, height=50)
        assert widget.visible is True
        widget.hide()
        assert widget.visible is False
        widget.draw()
        pygame.display.flip()
        widget.show()
        assert widget.visible is True
        widget.draw()
        pygame.display.flip()

    def test_widget_position(self, screen):
        """Test if the widget position can be set."""
        widget = Widget(master=screen, width=200, height=50)
        widget.place(x=100, y=100)
        assert widget.rect.topleft == (100, 100)
        widget.draw()
        pygame.display.flip()

    def test_widget_size(self, screen):
        """Test if the widget size can be set."""
        widget = Widget(master=screen, width=200, height=50)
        widget.resize(300, 100)
        assert widget.width == 300
        assert widget.height == 100
        widget.draw()
        pygame.display.flip()


def test_widget_hide_show(screen):
    """Test if the widget can be hidden and shown."""
    widget = Widget(master=screen, width=200, height=50)
    assert widget.visible is True
    widget.hide()
    assert widget.visible is False
    widget.draw()
    pygame.display.flip()
    widget.show()
    assert widget.visible is True
    widget.draw()
    pygame.display.flip()


def test_widget_diable_enable(screen):
    """Test if the widget can be disabled and enabled."""
    widget = Widget(master=screen, width=200, height=50)
    assert widget.disabled is False
    assert widget.state == "normal"
    widget.disable()
    assert widget.disabled is True
    assert widget.state == "disabled"
    widget.enable()
    assert widget.disabled is False
    assert widget.state == "normal"
    widget.draw()
    pygame.display.flip()


def test_widget_focus_unfocus(screen):
    """Test if the widget can be hidden and shown."""
    widget = Widget(master=screen, width=200, height=50)
    assert widget.focused is False
    widget.focus()
    assert widget.focused is True
    widget.unfocus()
    assert widget.focused is False
    widget.draw()
    pygame.display.flip()


@pytest.mark.skip("Dirty feature is currently not implemented.")
def test_widget_dirty_clean(screen):
    """Test if the widget can be hidden and shown."""
    widget = Widget(master=screen, width=200, height=50)
    assert widget.dirty is True
    widget.draw()
    assert widget.dirty is False
    # widget
    assert widget.dirty is True
    widget.draw()
    assert widget.dirty is False
    pygame.display.flip()


@pytest.mark.skip("This feature is currently broken.")
def test_widget_pack(screen):
    """Test if the widget can be packed."""
    widget = Widget(master=screen, width=200, height=50)
    widget.pack(padx=10, pady=10)
    assert widget.rect.topleft == (10, 10)
    assert widget.rect.size == (200, 50)
    widget.draw()
    pygame.display.flip()


@pytest.mark.skip("This feature is currently broken.")
def test_widget_grid(screen):
    """Test if the widget can be placed in a grid."""
    widget = Widget(master=screen, width=200, height=50)
    widget.grid(row=1, column=2, rowspan=2, columnspan=1)
    assert widget.rect.topleft == (0, 0)  # Adjust based on grid implementation
    assert widget.rect.size == (200, 50)
    widget.draw()
    pygame.display.flip()


def test_widget_place(screen):
    """Test if the widget can be placed."""
    widget = Widget(master=screen, width=200, height=50)
    widget.place(x=400, y=300)
    assert widget.rect.topleft == (400, 300)
    assert widget.rect.size == (200, 50)
    widget.draw()
    pygame.display.flip()


def test_widget_geometry(screen):
    """Test if the widget geometry can be set."""
    widget = Widget(master=screen, width=200, height=50)
    widget.place(x=100, y=100)
    assert widget.rect.topleft == (100, 100)
    assert widget.rect.size == (200, 50)
    widget.draw()
    pygame.display.flip()


def test_widget_runtime_style_update(screen):
    """Test runtime style updates with set_style/reset_style."""
    widget = Widget(master=screen, width=120, height=40)
    original_bg = widget.style.get("background")

    widget.set_style(background=(10, 20, 30), border_color=(120, 130, 140))
    assert widget.style["background"] == (10, 20, 30)
    assert widget.style["border_color"] == (120, 130, 140)

    widget.reset_style()
    assert widget.style.get("background") == original_bg


def test_widget_set_background_helper(screen):
    """Test helper for setting background color."""
    widget = Widget(master=screen, width=120, height=40)
    widget.set_background("#112233")
    assert widget.configure("background") == pygame.Color("#112233")


def test_widget_configure_theme_and_background(screen):
    """Test configuring style values via configure API."""
    widget = Widget(master=screen, width=120, height=40)
    widget.configure(theme={"background": (1, 2, 3), "border_color": (4, 5, 6)})
    assert widget.configure("background") == (1, 2, 3)
    assert widget.configure("bordercolor") == (4, 5, 6)

    widget.configure(background=(11, 12, 13), bordercolor=(21, 22, 23))
    assert widget.configure("background") == (11, 12, 13)
    assert widget.configure("bordercolor") == (21, 22, 23)


def test_widget_opacity_customization(screen):
    """Test setting and reading widget opacity."""
    widget = Widget(master=screen, width=120, height=40)
    widget.set_opacity(120)
    assert widget.configure("opacity") == 120

    widget.configure(opacity=200)
    assert widget.configure("opacity") == 200


def test_widget_opacity_out_of_range_raises(screen):
    """Opacity outside 0-255 should raise ValueError."""
    widget = Widget(master=screen, width=120, height=40)
    with pytest.raises(ValueError):
        widget.set_opacity(500)


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])
