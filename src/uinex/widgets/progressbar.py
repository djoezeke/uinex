"""PygameUI Progressbar Widget

A Progressbar is a visual indicator of progress for a task, typically displayed as a horizontal or vertical bar
that fills as progress increases. It supports value bounds, orientation, colors, and optional value display.

Features:
    - Horizontal or vertical orientation
    - Determinate and indeterminate modes
    - Customizable min, max, and current value
    - Customizable colors and border
    - Optional value display (numeric or percent)
    - Callback for value change (extendable)
    - Mouse interaction for value setting

Example:
    pb = Progressbar(master=screen, length=200, thickness=24, value=50)
    pb.set(50)
    pb.start()  # For indeterminate mode
    pb.step(10) # Increment by 10
    pb.stop()   # Stop indeterminate animation

Author: Your Name & PygameUI Contributors
License: MIT
"""

import time
from typing import Literal, Optional, Union, Any

import pygame

from uinex.core.widget import Widget

__all__ = ["Progressbar"]


class Progressbar(Widget):
    """A modern, customizable progress bar widget for PygameUI.

    The Progressbar visually represents the progress of a task. It can operate in two modes:
    - Determinate: Shows the amount completed relative to the total.
    - Indeterminate: Shows an animated bar to indicate ongoing activity when progress cannot be measured.

    Supports horizontal and vertical orientations, color customization, and optional percentage display.

    Examples:

        ```python
        from pygameui import Progressbar

        progress = ttk.Progressbar(
            master=screen,
            lenght=300,
            thickness=20,
            orientation="horizontal",
        )
        progress.pack(x=20, y=100)

        # autoincrement the bar
        progress.start()

        # stop the autoincrement
        progress.stop()

        # manually update the bar value
        progress.configure(value=25)

        # increment the value by 10 steps
        progress.step(10)
        ```

    Attributes:
        text (str): Optional label or text to display.
        mode (str): 'determinate' or 'indeterminate'.
        mask (str): Optional string format for the label (e.g., '{}% Complete').
        orientation (str): 'horizontal' or 'vertical'.
        minimum (float): Minimum value.
        maximum (float): Maximum value.
        value (float): Current value.
        indeterminate (bool): Whether indeterminate animation is active.
        indet_pos (float): Current position of the indeterminate bar.
        indet_speed (float): Speed of the indeterminate animation (pixels/sec).
        step_amount (float): Default step increment.
        last_update (float): Last update time for animation.
        font (pygame.font.Font): Font for text display.
        theme (dict): Color and style settings.

    """

    def __init__(
        self,
        master: Optional[Any] = None,
        text: str = "progress",
        length: int = 200,
        thickness: int = 24,
        mask: Optional[str] = None,
        value: Union[float, int] = 0,
        minimum: Union[float, int] = 0,
        maximum: Union[float, int] = 100,
        font: Optional[pygame.font.Font] = None,
        mode: Literal["determinate", "indeterminate"] = "determinate",
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        **kwargs,
    ):
        """
        Initialize a Progressbar Widget.

        Args:
            master (Widget or pygame.Surface, optional): Parent widget or surface.

            length (int, optional):
                Specifies the length of the long axis of the progressbar.
                (width if orientation = horizontal, height if if vertical);

            thickness (int, optional):
                Specifies the length of the long axis of the progressbar.
                (height if orientation = horizontal, width if if vertical);

            maximum (int or float): Maximum value. Defaults to 100.
            value (int or float): Initial value. Defaults to 0.

            font (pygame.Font, optional): Font for text.

            mode ('determinate', 'indeterminate'):
                Use `indeterminate` if you cannot accurately measure the
                relative progress of the underlying process. In this mode,
                a rectangle bounces back and forth between the ends of the
                widget once you use the `Progressbar.start()` method.
                Otherwise, use `determinate` if the relative progress can be
                calculated in advance.

            orientation ('horizontal', 'vertical'):
                Specifies the orientation of the widget.

            mask (str, optional):
                A string format that can be used to update the Progressbar
                label every time the value is updated. For example, the
                string "{}% Storage Used" with a widget value of 45 would
                show "45% Storage Used" on the Progressbar label. If a
                mask is set, then the `text` option is ignored.

            **kwargs: Additional configuration options.
        """

        if orientation == "horizontal":
            width = length
            height = thickness
        else:
            width = thickness
            height = length

        Widget.__init__(self, master, width, height, **kwargs)

        self._text = text
        self._mode = mode
        self._mask = mask
        self.orientation = orientation
        self._minimum = min(0, float(minimum))
        self._maximum = max(1, float(maximum))
        self._value = max(self._minimum, min(float(value), self._maximum))

        self._indeterminate = False
        self._indet_pos = 0.0
        self._indet_speed = kwargs.get("indeterminate_speed", 100)  # pixels per second
        self._step_amount = 1.0
        self._last_update = time.time()

        self._font = font or pygame.font.SysFont(None, 18)

        custom_theme = {
            "background": (0, 120, 215),
            "text_color": (255, 255, 255),
            "bar_color": (0, 90, 180),
            "border_color": (0, 90, 180),
            "hover_color": (0, 90, 180),
            "disable_color": (0, 90, 180),
        }
        self._theme.update(custom_theme)

    # region Property

    # endregion

    # region Public

    def start(self):
        """Start Autoincrementing (indeterminate mode)."""
        if self._mode == "indeterminate":
            self._indeterminate = True
            self._indet_pos = 0.0
            self._last_update = time.time()

    def stop(self):
        """Stop indeterminate animation."""
        self._indeterminate = False

    def step(self, value: float = None):
        """Increment the progressbar value by a step.

        Args:
            value (float, optional): Amount to increment. If None, uses default step amount.
        """
        if value is None:
            value = self._step_amount
        self.set(self._value + value)

    def set(self, value: float):
        """Set the current value (clamped to [minimum, maximum]).

        Args:
            value (float): New value to set.
        """
        value = max(self._minimum, min(float(value), self._maximum))
        if value != self._value:
            self._value = value
            self._dirty = True

    def get(self) -> float:
        """Get the current value.

        Returns:
            float: The current value of the progressbar.
        """
        return self._value

    def set_max(self, maximum: float):
        """Set the maximum value.

        Args:
            maximum (float): New maximum value.
        """
        if maximum != self._maximum:
            self._maximum = maximum
            self._value = max(self._minimum, min(float(self._value), self._maximum))
            self._dirty = True

    def set_min(self, minimum: float):
        """Set the minimum value.

        Args:
            minimum (float): New minimum value.
        """
        if minimum != self._minimum:
            self._minimum = minimum
            self._value = max(self._minimum, min(float(self._value), self._maximum))
            self._dirty = True

    def set_orientation(self, orientation: Literal["horizontal", "vertical"]):
        """Set the orientation of the progressbar.

        Args:
            orientation (str): 'horizontal' or 'vertical'.
        """
        if orientation not in ["horizontal", "vertical"]:
            raise ValueError("Orientation must be 'horizontal' or 'vertical'.")
        if orientation != self.orientation:
            self.orientation = orientation
            self._dirty = True

    # endregion

    # region Private

    def _perform_draw_(self, surface, *args, **kwargs):
        """
        Draw the progressbar with a modern look.

        - Draws a rounded background bar
        - Draws a filled accent bar for progress
        - Optionally displays percentage or value text

        Args:
            surface (pygame.Surface): The surface to draw on.
        """

        foreground = self._theme["bar_color"]
        background = self._theme["background"]
        bordercolor = self._theme["border_color"]

        rect = self._rect

        # Draw filled rounded rectangle for button background
        pygame.draw.rect(surface, background, self._rect, border_radius=self._border_radius)

        # Draw border (rounded)
        if self._borderwidth > 0:
            pygame.draw.rect(surface, bordercolor, self._rect, self._borderwidth, self._border_radius)

        percent = (self._value - self._minimum) / (self._maximum - self._minimum)
        percent = max(0.0, min(1.0, percent))

        if self._mode == "indeterminate" and self._indeterminate:
            # Draw moving bar for indeterminate mode
            bar_length = rect.width if self.orientation == "horizontal" else rect.height
            indet_width = int(bar_length * 0.3)
            pos = int(self._indet_pos)
            if self.orientation == "horizontal":
                fill_rect = pygame.Rect(
                    rect.left + pos,
                    rect.top + self._borderwidth,
                    indet_width,
                    rect.height - 2 * self._borderwidth,
                )
            else:
                fill_rect = pygame.Rect(
                    rect.left + self._borderwidth,
                    rect.top + pos,
                    rect.width - 2 * self._borderwidth,
                    indet_width,
                )
            pygame.draw.rect(surface, foreground, fill_rect)
        else:
            # ...existing determinate drawing code...
            if self.orientation == "horizontal":
                fill_width = int((rect.width - 2 * self._borderwidth) * percent)
                fill_rect = pygame.Rect(
                    rect.left + self._borderwidth,
                    rect.top + self._borderwidth,
                    fill_width,
                    rect.height - 2 * self._borderwidth,
                )
                pygame.draw.rect(surface, foreground, fill_rect)
            elif self.orientation == "vertical":
                fill_height = int((rect.height - 2 * self._borderwidth) * percent)
                fill_rect = pygame.Rect(
                    rect.left + self._borderwidth,
                    rect.bottom - self._borderwidth - fill_height,
                    rect.width - 2 * self._borderwidth,
                    fill_height,
                )
                pygame.draw.rect(surface, foreground, fill_rect)

        # Draw text (percentage) if enabled
        if self._text and self._mode == "determinate":
            percent_val = int(percent * 100)
            if self._mask:
                text = self._mask.format(percent_val)
            else:
                text = f"{percent_val}%"
            txt_surf = self._font.render(text, True, self._theme["text_color"])
            txt_rect = txt_surf.get_rect(center=rect.center)
            surface.blit(txt_surf, txt_rect)

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse events for interactive value setting (optional).

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not self._rect.collidepoint(event.pos):
                return
            mouse = (event.pos[0] - self._rect.x, event.pos[1] - self._rect.y)
            if self.orientation == "horizontal":
                percent = (mouse[0] - self._borderwidth) / (self._rect.width - 2 * self._borderwidth)
            elif self.orientation == "vertical":
                percent = 1.0 - (mouse[1] - self._borderwidth) / (self._rect.height - 2 * self._borderwidth)
            value = self._minimum + percent * (self._maximum - self._minimum)
            self.set(value)

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for Progressbar (handles indeterminate animation).

        Args:
            delta (float): Time since last update (seconds).
        """
        if self._mode == "indeterminate" and self._indeterminate:
            now = time.time()
            elapsed = now - self._last_update
            self._last_update = now
            bar_length = self._rect.width if self.orientation == "horizontal" else self._rect.height
            self._indet_pos += self._indet_speed * elapsed
            if self._indet_pos > bar_length:
                self._indet_pos = 0.0
            self._dirty = True

    def _configure_get_(self, attribute: str) -> Any:
        """Get configuration attribute value.

        Args:
            attribute (str): Attribute name.

        Returns:
            Any: Attribute value.
        """
        if attribute is not None:
            if attribute == "value":
                return self._value
            if attribute == "minimum":
                return self._minimum
            if attribute == "maximum":
                return self._maximum
            if attribute == "orientation":
                return self.orientation
            return super()._configure_get_(attribute)

    def _configure_set_(self, **kwargs) -> None:
        """Set configuration attributes.

        Args:
            **kwargs: Attribute values to set.
        """
        if "value" in kwargs:
            self.set(kwargs["value"])
        if "minimum" in kwargs:
            self._minimum = kwargs["minimum"]
            self.set(self._value)
        if "maximum" in kwargs:
            self._maximum = kwargs["maximum"]
            self.set(self._value)
        if "orientation" in kwargs:
            self.orientation = kwargs["orientation"]
        return super()._configure_set_(**kwargs)

    # endregion


# --------------------------------------------------------------------
# Example usage and demonstration

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((480, 280))
    pygame.display.set_caption("PygameUI Progressbar")
    clock = pygame.time.Clock()

    progress = Progressbar(master=screen, text="Pro", value=20, orientation="horizontal", mask="{}% Storage Used")
    progress.pack()

    running: bool = True
    while running:
        delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            progress.handle(event)
        progress.update(delta)

        screen.fill("white")
        progress.draw()
        pygame.display.flip()
