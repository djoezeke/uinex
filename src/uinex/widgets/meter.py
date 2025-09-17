"""PygameUI Meter Widget

A Meter is a visual widget that displays a value as a filled bar or arc, commonly used for meter,
capacity, or gauge indicators. It supports horizontal, vertical, and circular styles, value bounds,
custom colors, and value display.

Features:
    - Horizontal, vertical, or circular meter styles
    - Customizable min, max, and current value
    - Customizable colors and thickness
    - Optional value display (numeric or percent)
    - Callback for value change
    - Mouse interaction (optional, for setting value)

Example:
    meter = Meter(master, min_value=0, max_value=100, value=50, style="horizontal")
    meter.set_value(75)

Author: Your Name & PygameUI Contributors
License: MIT
"""

import math
from typing import Literal, Optional, Union, Any

import pygame

from uinex.widgets.progressbar import Progressbar

__all__ = ["Meter"]


class Meter(Progressbar):
    """Modern Meter Widget.

    A widget that shows the status of a long-running operation
    with an optional text indicator.

    Similar to the `Floodgauge`, this widget can operate in
    two modes. *determinate* mode shows the amount completed
    relative to the total amount of work to be done, and
    *indeterminate* mode provides an animated display to let the
    user know that something is happening.

    Examples:

        ```python
        from pygameui import Meter

        gauge = ttk.Meter(
            master=screen,
            lenght=300,
            thickness=20,
            orientation="circular",
            mask='Memory Used {}%',
        )
        gauge.pack(x=20, y=100)

        # autoincrement the gauge
        gauge.start()

        # stop the autoincrement
        gauge.stop()

        # manually update the gauge value
        gauge.configure(value=25)

        # increment the value by 10 steps
        gauge.step(10)
        ```
    """

    def __init__(
        self,
        master: Optional[Any] = None,
        text: str = None,
        width: int = 200,
        height: int = 24,
        mask: Optional[str] = None,
        value: Union[float, int] = 0,
        minimum: Union[float, int] = 0,
        maximum: Union[float, int] = 100,
        font: Optional[pygame.font.Font] = None,
        mode: Literal["determinate", "indeterminate"] = "determinate",
        style: Literal["circular", "horizontal", "vertical"] = "circular",
        **kwargs,
    ):
        """
        Initialize a Meter  Widget.

        Args:
            master (Widget or pygame.Surface, optional): Parent widget or surface.

            length (int, optional):
                Specifies the length of the long axis of the Meter.
                (width if style = horizontal, height if if vertical);

            thickness (int, optional):
                Specifies the length of the long axis of the meter.
                (height if orientation = horizontal, width if if vertical);

            maximum (int or float): Maximum value. Defaults to 100.
            value (int or float): Initial value. Defaults to 0.

            font (pygame.Font, optional): Font for text.

            mode ('determinate', 'indeterminate'):
                Use `indeterminate` if you cannot accurately measure the
                relative meter of the underlying process. In this mode,
                a rectangle bounces back and forth between the ends of the
                widget once you use the `Meter.start()` method.
                Otherwise, use `determinate` if the relative meter can be
                calculated in advance.

            style ('circular', 'horizontal', 'vertical'):
                Specifies the style of the widget.

            mask (str, optional):
                A string format that can be used to update the Meter
                label every time the value is updated. For example, the
                string "{}% Storage Used" with a widget value of 45 would
                show "45% Storage Used" on the Meter label. If a
                mask is set, then the `text` option is ignored.

            **kwargs: Additional configuration options.
        """

        if style == "circular":
            width = height = max(width, height)

        Progressbar.__init__(
            self, master, text, width, height, mask, value, minimum, maximum, font, mode, style, **kwargs
        )

    # region Private

    def _perform_draw_(self, surface, *args, **kwargs):
        """
        Draw the meter with a modern look.

        - Draws a rounded background bar
        - Draws a filled accent bar for meter
        - Optionally displays percentage or value text

        Args:
            surface (pygame.Surface): The surface to draw on.
        """

        if self.orientation == "circular":

            foreground = self._theme["bar_color"]
            background = self._theme["background"]

            rect = self._rect

            percent = (self._value - self._minimum) / (self._maximum - self._minimum)
            percent = max(0.0, min(1.0, percent))

            center = rect.center
            radius = min(rect.width, rect.height) // 2 - self._borderwidth
            start_angle = -90
            end_angle = start_angle + int(360 * percent)
            pygame.draw.circle(surface, background, center, radius)

            if percent > 0:
                # Draw arc as filled pie
                points = [center]
                for angle in range(start_angle, end_angle + 1, 2):
                    rad = angle * 3.14159 / 180
                    x = center[0] + int(radius * math.cos(rad))
                    y = center[1] + int(radius * math.sin(rad))
                    points.append((x, y))
                if len(points) > 2:
                    pygame.draw.polygon(surface, foreground, points)

            pygame.draw.circle(surface, foreground, center, radius, self._borderwidth)

            if self._text:
                percent_val = int(percent * 100)
                if self._mask:
                    text = self._mask.format(percent_val)
                else:
                    text = f"{percent_val}%"
                txt_surf = self._font.render(text, True, self._theme["text_color"])
                txt_rect = txt_surf.get_rect(center=rect.center)
                surface.blit(txt_surf, txt_rect)
        else:
            super()._perform_draw_(surface, *args, **kwargs)

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse events for interactive value setting (optional)."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = (event.pos[0] - self._rect.x, event.pos[1] - self._rect.y)
            if self.orientation == "circular":
                # Optional: implement circular click-to-set
                percent = None
                value = self._minimum + percent * (self._maximum - self._maximum)
                self.set(value)
            else:
                super()._handle_event_(event, *args, **kwargs)

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for Meter (not used)."""

    # endregion


# --------------------------------------------------------------------
# testing and demonstration stuff

if __name__ == "__main__":

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((480, 280))
    pygame.display.set_caption("PygameUI Meter")
    clock = pygame.time.Clock()

    meter = Meter(master=screen, text="Pro")
    meter.pack()

    running: bool = True
    while running:
        delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            meter.handle(event)
        meter.update(delta)

        screen.fill("white")
        meter.draw()

        pygame.display.flip()
