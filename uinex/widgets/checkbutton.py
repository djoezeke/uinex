"""PygameUI CheckButton Widget

This module defines the CheckButton widget for PygameUI, supporting modern theming,
rounded corners, hover/active/disabled states, and callback binding.

Features:
    - Modern look with rounded corners and accent colors
    - Theming via ThemeManager
    - Hover, active (checked), and disabled states
    - Optional label text
    - Callback/callback binding for state change

Usage Example:
    check = CheckButton(master=screen, text="Accept Terms", command=on_toggle)
    check.place(x=100, y=150)
    ...
    check.handel(event)
    check.update()
    check.draw()
    ...

Author: Sackey Ezekiel Etrue & PygameUI Contributors
License: MIT
"""

from typing import Optional, Callable, Any

import pygame

from uinex.core.widget import Widget
from uinex.core.themes import ThemeManager
from uinex.core.mixins import HoverableMixin, ClickableMixin


class CheckButton(Widget, HoverableMixin, ClickableMixin):
    """
    Modern CheckButton widget with theming, rounded corners, and state management.

    Args:
        master (Widget or pygame.Surface, optional): Parent widget or surface.
        text (str): Label text next to the checkbox.
        checked (bool): Initial checked state.
        command (callable, optional): Function to call when toggled.
        disabled (bool): If True, disables interaction.
        **kwargs: Additional configuration options.

    Attributes:
        _checked (bool): Whether the checkbox is checked.
        _disabled (bool): Whether the checkbox is disabled.
        _text (str): Label text.
        _font (pygame.Font): Font for label.
        _command (callable): Callback for toggle.
    """

    def __init__(
        self,
        master: Optional[Any] = None,
        text: str = "",
        checked: bool = False,
        command: Optional[Callable[[bool], None]] = None,
        disabled: bool = False,
        **kwargs,
    ):
        Widget.__init__(self, master, **kwargs)
        # NOTE: `width` and `height` are handled in kwargs, so we don't set them here.

        # Bind command if provided
        if command is not None:
            self.bind(pygame.MOUSEBUTTONDOWN, command)

        self._checked = checked
        self._disabled = disabled
        self._text = text

        # Font and theme
        font_ = pygame.font.SysFont(ThemeManager.theme["font"]["family"], ThemeManager.theme["font"]["size"])
        self._font = kwargs.pop("font", font_)

        # Sizing
        width = kwargs.pop("width", 28 + (self._font.size(self._text)[0] + 12 if self._text else 0))
        height = kwargs.pop("height", max(28, self._font.get_height() + 8))

        HoverableMixin.__init__(self)
        ClickableMixin.__init__(self)

    def toggle(self):
        """Toggle the checked state and call the command callback if set."""
        if not self._disabled:
            self._checked = not self._checked
            # if self._command:
            #     self._command(self._checked)

    def set_checked(self, value: bool):
        """Set the checked state."""
        if not self._disabled:
            self._checked = value

    def is_checked(self) -> bool:
        """Return True if checked, else False."""
        return self._checked

    def _perform_draw_(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """
        Draw the checkbutton with a modern look.

        - Draws a rounded rectangle box (checkbox)
        - Fills with accent color if checked
        - Draws border and hover/disabled effects
        - Draws a checkmark if checked
        - Draws label text if provided

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        # Theme colors
        theme = ThemeManager.theme.get("Checkbox", {})
        state = (
            "disabled" if self._disabled else ("hovered" if self.hovered else "selected" if self._checked else "normal")
        )
        box_theme = theme.get(state, theme.get("normal", {}))

        box_rect = pygame.Rect(self._rect.left, self._rect.centery - 12, 24, 24)
        border_radius = box_theme.get("border_radius", 5)
        borderwidth = box_theme.get("borderwidth", 2)
        bordercolor = pygame.Color(box_theme.get("bordercolor", "#339CFF"))
        background = pygame.Color(box_theme.get("background", "#F7FAFC"))

        # Draw checkbox background
        pygame.draw.rect(surface, background, box_rect, border_radius=border_radius)

        # Draw border
        pygame.draw.rect(surface, bordercolor, box_rect, borderwidth, border_radius)

        # Draw checkmark if checked
        if self.clicked:
            accent = pygame.Color(box_theme.get("foreground", "#339CFF"))
            # Draw a modern checkmark
            start = (box_rect.left + 6, box_rect.centery)
            mid = (box_rect.left + 11, box_rect.bottom - 6)
            end = (box_rect.right - 5, box_rect.top + 6)
            pygame.draw.lines(surface, accent, False, [start, mid, end], 3)

        # Draw label text
        if self._text:
            text_color = pygame.Color(box_theme.get("foreground", "#1A2332"))
            label = self._font.render(self._text, True, text_color)
            label_rect = label.get_rect()
            label_rect.midleft = (box_rect.right + 8, box_rect.centery)
            surface.blit(label, label_rect)

    def _handle_event_(self, event: pygame.event.Event, *args, **kwargs) -> None:
        """
        Handle events for the checkbutton.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        self._check_hover(event)
        self._check_click(event)
        if self.clicked and not self._disabled:
            self.toggle()

    def _perform_update_(self, delta: float, *args, **kwargs) -> None:
        """
        Update the widget's logic (state management).

        Args:
            delta (float): Time since last update.
        """
