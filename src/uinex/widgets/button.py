"""PygameUI Button Widget Element

This module defines the Button widget for PygameUI, supporting rounded corners,
borders, hover/click/disabled effects, image support, and command binding.

Features:
    - Modern theming via ThemeManager
    - Rounded corners and border styling
    - Hover, click, and disabled states
    - Optional image/icon support
    - Command/callback binding for click events

Usage Example:
    button = Button(master=screen, text="Click Me", command=my_callback)
    button.place(x=100, y=100)
    ...
    button.handle(event)
    button.update()
    button.draw()
    ...

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & PygameUI Contributors
License: MIT
"""

from typing import Union, Tuple, Callable, Optional, Any

import pygame

from uinex.core.themes import ThemeManager
from uinex.core.widget import Widget

from uinex.core.mixins import (
    HoverableMixin,
    DoubleClickMixin,
    ClickableMixin,
)


class Button(Widget, HoverableMixin, DoubleClickMixin, ClickableMixin):
    """
    Button widget with rounded corners, border, hover/click/disabled effects, image support, and command binding.

    Args:
        master (Widget or pygame.Surface, optional): Parent widget or surface.
        width (int): Width of the button.
        height (int): Height of the button.
        text (str): Button label text.
        state (str): Initial state ("normal", "hovered", "clicked", "disabled").
        disabled (bool): If True, button is disabled.
        font (tuple or pygame.Font, optional): Font or font tuple.
        image (pygame.Surface, optional): Optional image/icon.
        border_radius (int, optional): Border radius for rounded corners.
        self._borderwidth (int, optional): Border width.
        background (pygame.Color, optional): Background color.
        foreground (pygame.Color, optional): Foreground/text color.
        hovercolor (pygame.Color, optional): Foreground color on hover.
        border_color (pygame.Color, optional): Border color.
        command (callable, optional): Function to call on click.
        **kwargs: Additional configuration options.

    Attributes:
        _text (str): Button label text.
        _font (pygame.Font): Font for rendering text.
        _image (pygame.Surface): Optional image/icon.
        _state (str): Current state ("normal", "hovered", "clicked", "disabled").
        _disabled (bool): Whether the button is disabled.
        _handler (dict): Event handlers for custom events.
        _foreground, _background, _hovercolor, etc.: Colors for various states.
        _border_radius, _borderwidth, etc.: Border styling for various states.
    """

    def __init__(
        self,
        master: Optional[Any] = None,
        width: int = 100,
        height: int = 40,
        text: str = "Button",
        state: str = "normal",
        disabled: bool = False,
        font: Optional[Union[Tuple, pygame.font.Font]] = None,
        image: Union[pygame.Surface, None] = None,
        background: Optional[pygame.Color] = None,
        text_color: Optional[pygame.Color] = None,
        hovercolor: Optional[pygame.Color] = None,
        border_color: Optional[pygame.Color] = None,
        command: Optional[Union[Callable[[], Any], None]] = None,
        **kwargs,
    ):
        """
        Initialize a Button widget.

        Args:
            See class docstring for details.
        """
        Widget.__init__(self, master, width, height, **kwargs)

        # Bind command if provided
        if command is not None:
            self.bind(pygame.MOUSEBUTTONDOWN, command)

        self._state: str = state
        self._disabled: bool = disabled

        self._text: str = text
        self._wraplenght: bool = kwargs.pop("wraplenght", True)
        self._underline: bool = kwargs.pop("underline", False)
        self._image: pygame.Surface = image

        # Font
        font_: pygame.Font = pygame.font.SysFont(
            ThemeManager.theme["font"]["family"], ThemeManager.theme["font"]["size"]
        )
        self._font: pygame.font.Font = font_ if font is None else font

        custom_theme = {
            "background": (0, 120, 215),
            "text_color": (255, 255, 255),
            "hover_color": (0, 90, 180),
            "select_color": (0, 90, 180),
            "disable_color": (0, 90, 180),
            "border_color": (0, 90, 180),
        }
        self._theme.update(custom_theme)

        DoubleClickMixin.__init__(self)
        ClickableMixin.__init__(self)
        HoverableMixin.__init__(self)

    # region Property

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, _text):
        self._text = _text

    # endregion

    # region Public

    def disable(self):
        """Disables the button so that it is no longer interactive."""
        if not self._disabled:
            self._disabled = True
            self._set_state_("disabled")
            self._hover = False
            self._clicked = False
            self._double_clicked = False

    def enable(self):
        """Re-enables the button, so it can once again be interacted with."""
        if self._disabled:
            self._disabled = False
            self._set_state_("normal")

    # endregion

    # region Private

    def _set_state_(self, state: str = None):
        """
        Set the state of the button.

        If state is None, it will determine the state based on the current conditions.
        """
        if state is None:
            if not self._disabled:
                if self.hovered:
                    self._state = "hovered"
                elif self.clicked:
                    self._state = "clicked"
                else:
                    self._state = "normal"
            else:
                self._state = "disabled"
        else:
            self._state = state

    def _get_state_foreground_(self) -> pygame.Color:
        """Get the foreground color based on the current state."""
        if self._state == "hovered":
            return self._theme["text_color"]
        if self._state == "clicked":
            return self._theme["text_color"]
        if self._state == "disabled":
            return self._theme["text_color"]
        return self._theme["text_color"]

    def _get_state_background_(self) -> pygame.Color:
        """Get the background color based on the current state."""
        if self._state == "hovered":
            return self._theme["hover_color"]
        if self._state == "clicked":
            return self._theme["hover_color"]
        if self._state == "disabled":
            return self._theme["hover_color"]
        return self._theme["background"]

    def _configure_set_(self, **kwargs) -> None:
        """
        Configure method to set custom attributes.

        Args:
            **kwargs: Attributes to set.
        """
        self._text = self._kwarg_get(kwargs, "text", self._text)
        self._font = self._kwarg_get(kwargs, "font", self._font)
        self._image = self._kwarg_get(kwargs, "image", self._image)
        self._underline = self._kwarg_get(kwargs, "underline", self._underline)
        # self._wraplength = self._kwarg_get(kwargs, "wraplength", self._wraplength)

        # hover_color, select_color
        # text_color, disable_text_color, select_text_color

    def _configure_get_(self, attribute: str) -> Any:
        """
        Configure method to get the current value of an attribute.

        Args:
            attribute (str): The attribute name.

        Returns:
            Any: The value of the attribute.
        """
        if attribute == "text":
            return self._text
        if attribute == "font":
            return self._font
        if attribute == "image":
            return self._image
        # if attribute == "wraplength":
        #     return self._wraplength
        if attribute == "underline":
            return self._underline

        if attribute == "text_color":
            return
        if attribute == "disable_text_color":
            return
        if attribute == "select_text_color":
            return
        if attribute == "hover_text_color":
            return

        if attribute == "select_color":
            return
        if attribute == "hover_color":
            return

        return super()._configure_get_(attribute)

    def _perform_draw_(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """
        Draw the button widget on the given surface with a modern look.

        - Uses theme colors for background, border, and text.
        - Draws a filled rounded rectangle for the button background.
        - Draws a border with rounded corners.
        - Supports optional shadow for depth (modern effect).
        - Renders text centered, and optional image left of text.
        - Handles all states: normal, hovered, clicked, disabled.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        foreground = self._get_state_foreground_()
        background = self._get_state_background_()
        bordercolor = self._theme["border_color"]

        # # Optional: Draw shadow for modern depth effect
        # shadow_offset = 3
        # shadow_color = (0, 0, 0, 60)  # semi-transparent black
        # shadow_rect = self._rect.move(shadow_offset, shadow_offset)
        # shadow_surf = pygame.Surface(self._rect.size, pygame.SRCALPHA)
        # pygame.draw.rect(
        #     shadow_surf,
        #     shadow_color,
        #     shadow_surf.get_rect(),
        #     border_radius=border_radius,
        # )
        # surface.blit(shadow_surf, shadow_rect.topleft)

        # Draw filled rounded rectangle for button background
        pygame.draw.rect(surface, background, self._rect, border_radius=self._border_radius)

        # Draw border (rounded)
        if self._borderwidth > 0:
            pygame.draw.rect(surface, bordercolor, self._rect, self._borderwidth, self._border_radius)

        # Draw optional image (left of text)
        text_offset_x = 0
        if self._image:
            img_rect = self._image.get_rect()
            img_rect.centery = self._rect.centery
            img_rect.left = self._rect.left + 12  # More padding for modern look
            surface.blit(self._image, img_rect)
            text_offset_x = img_rect.width + 16  # Space for image + padding

        # Render and draw text centered (with offset if image present)
        btn_text = self._font.render(self._text, True, foreground)
        btn_text_rect = btn_text.get_rect()
        btn_text_rect.centery = self._rect.centery
        if self._image:
            btn_text_rect.left = self._rect.left + text_offset_x
        else:
            btn_text_rect.centerx = self._rect.centerx
        surface.blit(btn_text, btn_text_rect)

    def _handle_event_(self, event: pygame.event.Event, *args, **kwargs) -> None:
        """
        Handle an event for the widget.

        Args:
            event (pygame.Event): The event to handle.
        """
        self._check_hover(event)
        self._check_double(event)
        self._check_click(event)

        # If clicked/hovered/doubleclicked, call bound command if present
        # if self.clicked or self.hovered or self.doubleclicked:
        #     try:
        #         command = self._handler[event.type]
        #         command()
        #     except KeyError:
        #         pass

    def _perform_update_(self, delta: float, *args, **kwargs) -> None:
        """
        Update the widget's logic.

        Args:
            delta (float): Time since last update.
        """
        self._set_state_()
        if self._state == "hovered":
            self._show_tooltip = True
        else:
            self._show_tooltip = False

    # endregion


# --------------------------------------------------------------------
# testing and demonstration stuff

if __name__ == "__main__":

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((480, 280))
    pygame.display.set_caption("PygameUI Label")
    clock = pygame.time.Clock()

    def command(hello):
        print(f"Clicked {hello.text}")

    button = Button(master=screen, text="Click Me", tooltip="Say hello", command=command)
    button.pack()

    running: bool = True
    while running:
        delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            button.handle(event)
        button.update(delta)

        screen.fill("white")
        button.draw()

        pygame.display.flip()
