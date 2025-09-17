import pygame
import pytest

from uinex.core.widget import Widget


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


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])
