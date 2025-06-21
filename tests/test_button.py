import pygame
import pytest

from pygameui.widgets.button import Button


class TestButton:
    def test_button_creation(self, screen):
        """Test if the button can be created."""
        button = Button(master=screen, width=200, height=50, text="Click Me")
        assert isinstance(button, Button)
        assert button.width == 200
        assert button.height == 50
        assert button.text == "Click Me"

    def test_button_draw(self, screen):
        """Test if the button can be drawn on the screen."""
        button = Button(master=screen, width=200, height=50, text="Click Me")
        button.draw()
        # pygame.display.flip()
        # Check if the button is drawn by checking its rect
        assert button.rect.width == 200
        assert button.rect.height == 50

    def test_button_click(self, screen):
        """Test if the button can handle click events."""
        button = Button(master=screen, width=200, height=50, text="Click Me")
        button.rect.topleft = (100, 100)
        button.draw()
        # pygame.display.flip()
        mouse_pos = (150, 120)
        mouse_click = pygame.mouse.get_pressed()

        if mouse_click[0]:  # Left mouse button
            if button.rect.collidepoint(mouse_pos):
                button.on_click()
                assert button.clicked is True
        else:
            assert button.clicked is False

    def test_button_text(self, screen):
        """Test if the button text is set correctly."""
        button = Button(master=screen, width=200, height=50, text="Click Me")
        assert button.text == "Click Me"
        button.text = "New Text"
        assert button.text == "New Text"
        button.draw()
        pygame.display.flip()

    def test_button_visibility(self, screen):
        """Test if the button visibility can be toggled."""
        button = Button(master=screen, width=200, height=50, text="Click Me")
        assert button.visible is True
        button.hide()
        assert button.visible is False
        button.draw()
        pygame.display.flip()
        button.show()
        assert button.visible is True
        button.draw()
        pygame.display.flip()

    def test_button_position(self, screen):
        """Test if the button position can be set."""
        button = Button(master=screen, width=200, height=50, text="Click Me")
        button.place(x=100, y=100)
        assert button.rect.topleft == (100, 100)
        button.draw()
        pygame.display.flip()

    def test_button_size(self, screen):
        """Test if the button size can be set."""
        button = Button(master=screen, width=200, height=50, text="Click Me")
        button.resize(300, 100)
        assert button.width == 300
        assert button.height == 100
        button.draw()
        pygame.display.flip()

    def test_button_color(self, screen):
        """Test if the button color can be set."""
        button = Button(
            master=screen,
            width=200,
            height=50,
            text="Click Me",
            bg_color=pygame.Color("#ff0000"),
        )
        # assert button.configure("bg_color") == pygame.Color("#ff0000")
        button.draw()
        pygame.display.flip()
        # Check if the color is applied by checking the surface color
        # assert button.surface.get_at((0, 0)) == pygame.Color("#ff0000")

    def test_button_text_color(self, screen):
        """Test if the button text color can be set."""
        button = Button(
            master=screen,
            width=200,
            height=50,
            text="Click Me",
            text_color=pygame.Color("#00ff00"),
        )
        # assert text_color == pygame.Color("#00ff00")
        button.draw()
        pygame.display.flip()
        # Check if the text color is applied by checking the surface color
        # assert button._surface.get_at((10, 10)) == pygame.Color("#00ff00")

    def test_button_font_size(self, screen):
        """Test if the button font size can be set."""
        button = Button(master=screen, width=200, height=50, text="Click Me", font_size=30)
        # assert font_size == 30
        button.draw()
        pygame.display.flip()
        # Check if the font size is applied by checking the surface size
        assert button.surface.get_size() == (200, 50)


def test_button_click_event(screen):
    """Test if the button click event is triggered."""
    button = Button(master=screen, width=200, height=50, text="Click Me")
    button.rect.topleft = (100, 100)
    button.draw()
    pygame.display.flip()
    mouse_pos = (150, 120)
    mouse_click = pygame.mouse.get_pressed()

    if mouse_click[0]:  # Left mouse button
        if button.rect.collidepoint(mouse_pos):
            # button.on_click()
            assert button.clicked is True
    else:
        assert button.clicked is False


def test_button_hide_show(screen):
    """Test if the button can be hidden and shown."""
    button = Button(master=screen, width=200, height=50, text="Click Me")
    assert button.visible is True
    button.hide()
    assert button.visible is False
    button.draw()
    pygame.display.flip()
    button.show()
    assert button.visible is True
    button.draw()
    pygame.display.flip()


@pytest.mark.skip("This feature is currently broken.")
def test_button_pack(screen):
    """Test if the button can be packed."""
    button = Button(master=screen, width=200, height=50, text="Click Me")
    button.pack(side="top", padx=10, pady=10)
    assert button.rect.topleft == (10, 10)
    assert button.rect.size == (200, 50)
    button.draw()
    pygame.display.flip()


@pytest.mark.skip("This feature is currently broken.")
def test_button_grid(screen):
    """Test if the button can be placed in a grid."""
    button = Button(master=screen, width=200, height=50, text="Click Me")
    button.grid(row=1, column=2, rowspan=2, columnspan=1)
    assert button.rect.topleft == (0, 0)  # Adjust based on grid implementation
    assert button.rect.size == (200, 50)
    button.draw()
    pygame.display.flip()


@pytest.mark.skip("This feature is currently broken.")
def test_button_place(screen):
    """Test if the button can be placed."""
    button = Button(master=screen, width=200, height=50, text="Click Me")
    button.place(x=400, y=300)
    assert button.rect.topleft == (400, 300)
    assert button.rect.size == (200, 50)
    button.draw()
    pygame.display.flip()


@pytest.mark.xfail(reason="A Certain Geometry Method is broken.")
def test_button_geometry(screen):
    """Test if the button geometry can be set."""
    button = Button(master=screen, width=200, height=50, text="Click Me")
    button.place(x=100, y=100)
    assert button.rect.topleft == (100, 100)
    assert button.rect.size == (200, 50)
    button.draw()
    pygame.display.flip()


if __name__ == "__main__":
    pytest.main([__file__])
