"""Uinex Label Widget Element

This module defines the Label widget for Uinex, supporting rounded corners,
borders, hover effects, and flexible configuration. The Label can display text
and an optional image, and supports theming via the ThemeManager.

Usage Example:
    label = Label(master=screen, text="My Label")
    label.place(x=100, y=100)
    ...
    label.handle(event)
    label.update()
    label.draw()
    ...

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & Uinex Contributors
License: MIT
"""

from typing import Any

import pygame

from uinex.theme.manager import ThemeManager
from uinex.utils.mixins import HoverableMixin
from uinex.widget.base import Widget

__all__ = ["Label"]


class Label(Widget, HoverableMixin):
    """
    Label widget with rounded corners, border, and hover effect.

    Args:
        master (Widget or pygame.Surface, optional): Parent widget or surface.
        width (int): Width of the label.
        height (int): Height of the label.
        text (str): Text to display.
        font (tuple or pygame.Font, optional): Font or font tuple.
        image (pygame.Surface, optional): Optional image/icon.
        background (pygame.Color, optional): Background color.
        foreground (pygame.Color, optional): Foreground/text color.
        **kwargs: Additional configuration options.

    Keyword Args:
        wraplength (bool): Whether to wrap text (default True).
        underline (bool): Whether to underline text (default False).
        border_radius (int): Border radius for rounded corners.
        borderwidth (int): Border width.
        hovercolor (pygame.Color): Foreground color on hover.
        hoverbackground (pygame.Color): Background color on hover.
        bordercolor (pygame.Color): Border color.
        state (str): Widget state ("normal", "hovered", etc.).

    Attributes:
        _text (str): The label's text.
        _font (pygame.Font): The font used for rendering text.
        _image (pygame.Surface): Optional image/icon.
        _border_radius (int): Border radius for rounded corners.
        _borderwidth (int): Border width.
        _foreground (pygame.Color): Foreground/text color.
        _background (pygame.Color): Background color.
        _hovercolor (pygame.Color): Foreground color on hover.
        _hoverbackground (pygame.Color): Background color on hover.
        _bordercolor (pygame.Color): Border color.
        _state (str): Current state ("normal", "hovered", etc.).
    """

    def __init__(
        self,
        master: Widget | pygame.Surface | None = None,
        width: int = 200,
        height: int = 40,
        text: str = "Label",
        font: tuple | pygame.font.Font | None = None,
        image: pygame.Surface | None = None,
        background: pygame.Color | None = None,
        foreground: pygame.Color | None = None,
        **kwargs,
    ) -> "Label":
        """
        Initialize a Label widget.

        Args:
            See class docstring for details.
        """
        Widget.__init__(self, master, width, height, **kwargs)

        # Apply per-instance colour overrides
        if background is not None:
            self._theme["background"] = background
        if foreground is not None:
            self._theme["text_color"] = foreground

        # Ensure mandatory keys exist
        self._theme.setdefault("background", (30, 30, 46))
        self._theme.setdefault("text_color", (220, 220, 220))
        self._theme.setdefault("hover_text_color", (255, 255, 255))
        self._theme.setdefault("disable_text_color", (140, 140, 150))
        self._theme.setdefault("hover_color", (50, 50, 70))
        self._theme.setdefault("border_color", (100, 100, 120))

        # Text
        self._text: str = text
        self._wraplength: bool = True
        self._underline: bool = False

        # Font
        _font_cfg = ThemeManager.theme.get("font", ThemeManager.theme.get("Font", {}))
        font_: pygame.Font = pygame.font.SysFont(
            _font_cfg.get("family", "Arial"), _font_cfg.get("size", 14)
        )
        self._font: pygame.Font = font_ if font is None else font

        # Image/Icon
        self._image: pygame.Surface = image

        HoverableMixin.__init__(self)

    # region Public

    @property
    def text(self) -> str:
        """Get or set the label text."""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    def get_text(self) -> str:
        """Get the current label text.

        Returns:
            str: The label's text.
        """
        return self._text

    def set_text(self, new_text: str) -> None:
        """Set the label text.

        Args:
            new_text (str): The new text to display.
        """
        self._text = new_text

    # endregion

    # region Private

    def _set_state_(self, state: str = None) -> None:
        """Set the state of the label.

        If state is None, it will determine the state based on the current conditions.
        """
        if state is None:
            self._state = "hovered" if self.hovered else "normal"
        else:
            self._state = state

    def _get_state_foreground_(self) -> pygame.Color:
        """Get the foreground color based on the current state.

        Returns:
            pygame.Color: The foreground color.
        """
        return self._theme["text_color"] if self._state == "hovered" else self._theme["text_color"]

    def _get_state_background_(self) -> pygame.Color:
        """Get the background color based on the current state.

        Returns:
            pygame.Color: The background color.
        """
        return self._theme["hover_color"] if self._state == "hovered" else self._theme["background"]

    def _configure_set_(self, **kwargs) -> None:
        """Configure method to set custom attributes.

        Args:
            **kwargs: Attributes to set.
        """
        self._text = self._kwarg_get(kwargs, "text", self._text)
        self._font = self._kwarg_get(kwargs, "font", self._font)
        self._image = self._kwarg_get(kwargs, "image", self._image)
        self._underline = self._kwarg_get(kwargs, "underline", self._underline)
        self._wraplength = self._kwarg_get(kwargs, "wraplength", self._wraplength)

        # hover_color
        # text_color, disable_text_color

        super()._configure_set_(**kwargs)

    def _configure_get_(self, attribute: str) -> Any:
        """Configure method to get the current value of an attribute.

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
        if attribute == "wraplength":
            return self._wraplength
        if attribute == "underline":
            return self._underline

        if attribute == "text_color":
            return
        if attribute == "hover_text_color":
            return
        if attribute == "disable_text_color":
            return

        if attribute == "hover_color":
            return

        return super()._configure_get_(attribute)

    def _perform_draw_(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """Draw the widget on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        foreground = self._get_state_foreground_()
        background = self._get_state_background_()

        # Draw Label Background
        pygame.draw.rect(
            surface,
            background,
            self._rect,
            border_radius=self._border_radius,
        )

        # Draw Label Border
        if self._borderwidth > 0:
            pygame.draw.rect(
                surface,
                self._theme.get("border_color", (100, 100, 120)),
                self._rect,
                self._borderwidth,
                self._border_radius,
            )

        # Draw image if provided (left of text)
        text_offset_x = 0
        if self._image:
            img_rect = self._image.get_rect()
            img_rect.centery = self._rect.centery
            img_rect.left = self._rect.left + 8
            surface.blit(self._image, img_rect)
            text_offset_x = img_rect.width + 8

        # Draw Label Text
        btn_text = self._font.render(self._text, True, foreground)
        if self._image:
            btn_text_rect = btn_text.get_rect()
            btn_text_rect.centery = self._rect.centery
            btn_text_rect.left = self._rect.left + text_offset_x
        else:
            btn_text_rect = btn_text.get_rect(center=self._rect.center)
        surface.blit(btn_text, btn_text_rect)

    def _handle_event_(self, event: pygame.event.Event, *args, **kwargs) -> None:
        """Handle an event for the widget.

        Args:
            event (pygame.Event): The event to handle.
        """
        self._check_hover(event)

    def _perform_update_(self, delta: float, *args, **kwargs) -> None:
        """Update the widget's logic.

        Args:
            delta (float): Time since last update.
        """
        self._set_state_()

    # endregion Private


# region Testing
# --------------------------------------------------------------------
# Testing and demonstration

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((480, 280))
    pygame.display.set_caption("Uinex Label")

    label = Label(master=screen, text="My Label", tooltip="Say hello")

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            label.handle(event)
        label.update()
        label.draw()
        pygame.display.flip()
