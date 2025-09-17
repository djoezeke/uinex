"""PygameUI Floodgauge Widget

A Floodgauge is a modern progress indicator that visually fills as progress increases.
It supports theming, rounded corners, smooth animation, and optional text display.

Features:
    - Modern theming via ThemeManager
    - Rounded corners and accent color
    - Smooth fill animation
    - Optional percentage or custom text display
    - Value range and step control

Example:
    flood = Floodgauge(master=screen, width=200, height=24, maximum=100)
    flood.set(50)
    flood.draw()

Author: Sackey Ezekiel Etrue & PygameUI Contributors
License: MIT
"""

from typing import Literal, Optional, Union, Any

import pygame

from uinex.widgets.progressbar import Progressbar


class Floodgauge(Progressbar):
    """Modern Floodgauge Widget.

    A widget that shows the status of a long-running operation
    with an optional text indicator.

    Similar to the `Progressbar`, this widget can operate in
    two modes. *determinate* mode shows the amount completed
    relative to the total amount of work to be done, and
    *indeterminate* mode provides an animated display to let the
    user know that something is happening.

    Examples:

        ```python
        from pygameui import Floodgauge

        gauge = ttk.Floodgauge(
            master=screen,
            lenght=300,
            thickness=20,
            orientation="horizontal",
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
        text: str = "flood",
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
        Initialize a Floodgauge  Widget.

        Args:
            master (Widget or pygame.Surface, optional): Parent widget or surface.

            length (int, optional):
                Specifies the length of the long axis of the floodgauge.
                (width if orientation = horizontal, height if if vertical);

            thickness (int, optional):
                Specifies the length of the long axis of the floodgauge.
                (height if orientation = horizontal, width if if vertical);

            maximum (int or float): Maximum value. Defaults to 100.
            value (int or float): Initial value. Defaults to 0.

            font (pygame.Font, optional): Font for text.

            mode ('determinate', 'indeterminate'):
                Use `indeterminate` if you cannot accurately measure the
                relative progress of the underlying process. In this mode,
                a rectangle bounces back and forth between the ends of the
                widget once you use the `Floodgauge.start()` method.
                Otherwise, use `determinate` if the relative progress can be
                calculated in advance.

            orientation ('horizontal', 'vertical'):
                Specifies the orientation of the widget.

            mask (str, optional):
                A string format that can be used to update the Floodgauge
                label every time the value is updated. For example, the
                string "{}% Storage Used" with a widget value of 45 would
                show "45% Storage Used" on the Floodgauge label. If a
                mask is set, then the `text` option is ignored.

            **kwargs: Additional configuration options.
        """

        Progressbar.__init__(
            self, master, text, length, thickness, mask, value, minimum, maximum, font, mode, orientation, **kwargs
        )

    # region Private

    def _perform_draw_(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """
        Draw the floodgauge with a modern look.

        - Draws a rounded background bar
        - Draws a filled accent bar for progress
        - Optionally displays percentage or value text

        Args:
            surface (pygame.Surface): The surface to draw on.
        """

        super()._perform_draw_(surface, *args, **kwargs)

    def _handle_event_(self, event: pygame.event.Event, *args, **kwargs) -> None:
        """Floodgauge does not handle events."""

        super()._handle_event_(event, *args, **kwargs)

    def _perform_update_(self, delta: float, *args, **kwargs) -> None:
        """Floodgauge does not update state."""

        super()._perform_update_(delta, *args, **kwargs)

    # endregion


# --------------------------------------------------------------------
# testing and demonstration stuff

if __name__ == "__main__":

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((480, 280))
    pygame.display.set_caption("PygameUI Label")
    clock = pygame.time.Clock()

    gauge = Floodgauge(master=screen, text="Pro", value=20, orientation="vertical")

    running: bool = True
    while running:
        delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            gauge.handle(event)
        gauge.update(delta)

        screen.fill("white")
        gauge.draw()

        pygame.display.flip()
