"""PygameUI Progressbar Widget

A Progressbar is a visual indicator of progress for a task, typically displayed as a horizontal or vertical bar
that fills as progress increases. It supports value bounds, orientation, colors, and optional value display.

Features:
    - Horizontal or vertical orientation
    - Customizable min, max, and current value
    - Customizable colors and border
    - Optional value display (numeric or percent)
    - Callback for value change

Example:
    pb = Progressbar(master, lenght=200, thickness=24, value=50)
    pb.set(50)

Author: Your Name & PygameUI Contributors
License: MIT
"""

from typing import Literal, Optional, Union, Any
import pygame

from pygameui.core.widget import Widget

__all__ = ["Progressbar"]


class Progressbar(Widget):
    """Modern Progressbar Widget.

    A widget that shows the status of a long-running operation
    with an optional text indicator.

    Similar to the `Floodgauge`, this widget can operate in
    two modes. *determinate* mode shows the amount completed
    relative to the total amount of work to be done, and
    *indeterminate* mode provides an animated display to let the
    user know that something is happening.

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
    """

    def __init__(
        self,
        master: Optional[Any] = None,
        text: str = None,
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
        """Start Autoincrementing."""

    def step(self, value: float):
        """Increment value by step."""

    def stop(self):
        """Stop Autoincrementing."""

    def set(self, value: float):
        """Set the current value (clamped to [0, maximum])."""
        value = max(self._minimum, min(float(value), self._maximum))
        if value != self._value:
            self._value = value
            self._dirty = True

    def get(self) -> float:
        """Get the current value."""
        return self._value

    def set_max(self, maximum: float):
        """Set the maximum value."""
        if maximum != self._maximum:
            self._maximum = maximum
            self._value = max(self._minimum, min(float(self._value), self._maximum))
            self._dirty = True

    def set_min(self, minimum: float):
        """Set the minimum value."""
        if minimum != self._minimum:
            self._minimum = minimum
            self._value = max(self._minimum, min(float(self._value), self._maximum))
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
        if self._text:
            percent_val = int(percent * 100)
            if self._mask:
                text = self._mask.format(percent_val)
            else:
                text = f"{percent_val}%"
            txt_surf = self._font.render(text, True, self._theme["text_color"])
            txt_rect = txt_surf.get_rect(center=rect.center)
            surface.blit(txt_surf, txt_rect)

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse events for interactive value setting (optional)."""

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = (event.pos[0] - self._rect.x, event.pos[1] - self._rect.y)

            if self.orientation == "horizontal":
                percent = (mouse[0] - self._borderwidth) / (self._rect.width - 2 * self._borderwidth)
            elif self.orientation == "vertical":
                percent = 1.0 - (mouse[1] - self._borderwidth) / (self._rect.height - 2 * self._borderwidth)

            value = self._minimum + percent * (self._maximum - self._maximum)
            self.set(value)

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for Progressbar (not used)."""

    def _configure_get_(self, attribute: str) -> Any:
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

        if "value" in kwargs:
            self.set_value(kwargs["value"])
        if "minimum" in kwargs:
            self._minimum = kwargs["minimum"]
            self.set_value(self._value)
        if "maximum" in kwargs:
            self._maximum = kwargs["maximum"]
            self.set_value(self._value)
        if "orientation" in kwargs:
            self.orientation = kwargs["orientation"]

        return super()._configure_set_(**kwargs)

    # endregion


# --------------------------------------------------------------------
# testing and demonstration stuff

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
