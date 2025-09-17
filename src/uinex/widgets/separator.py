"""PygameUI Separator Widget

A Separator is a simple visual divider used to separate groups of widgets in a UI layout.
It can be horizontal or vertical, with customizable thickness, color, and padding.

Features:
    - Horizontal or vertical orientation
    - Customizable color, thickness, and padding
    - Integrates with layout managers

Example:
    sep = Separator(master, orientation="horizontal", color=(180,180,180), thickness=2)

Author: Your Name & PygameUI Contributors
License: MIT
"""

from typing import Literal, Optional, Union, Any

import pygame

from uinex.core.widget import Widget

__all__ = ["Separator"]


class Separator(Widget):
    """
    A visual separator (horizontal or vertical line) for grouping widgets.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        orientation (str, optional): "horizontal" or "vertical". Default is "horizontal".
        color (pygame.Color or tuple, optional): Line color. Default is (180, 180, 180).
        thickness (int, optional): Line thickness in pixels. Default is 2.
        padding (int, optional): Space around the separator. Default is 4.
        length (int, optional): Length of the separator. If None, fills parent.
        **kwargs: Additional widget options.

    Attributes:
        orientation (str): "horizontal" or "vertical".
        color (pygame.Color): Line color.
        thickness (int): Line thickness.
        padding (int): Padding around the separator.
        length (int): Length of the separator.
    """

    def __init__(
        self,
        master: Optional[Any] = None,
        length: int = 200,
        thickness: int = 2,
        color: pygame.Color = (58, 141, 255),
        orientation: Literal["horizontal", "vertical"] = "horizontal",
        **kwargs,
    ):

        if orientation == "horizontal":
            width = length if length is not None else 100
            height = thickness
        else:
            width = thickness
            height = length if length is not None else 100

        Widget.__init__(self, master, width, height, **kwargs)

        self._orientation = orientation
        self._thickness = thickness
        self._length = length
        self._color = color

    # region Property

    # endregion

    # region Public

    # endregion

    # region Private

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the separator line."""

        self._surface.fill(self._color)
        surface.blit(self._surface, self._rect)

    def _handle_event_(self, event, *args, **kwargs):
        """Separator does not handle events."""

    def _perform_update_(self, delta, *args, **kwargs):
        """Separator does not perform updates."""

    # endregion


# --------------------------------------------------------------------
# testing and demonstration stuff

if __name__ == "__main__":

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((480, 280))
    pygame.display.set_caption("PygameUI Seperator")
    clock = pygame.time.Clock()

    seperator = Separator(master=screen, orientation="vertical")
    seperator.place(x=20, y=20)

    running: bool = True
    while running:
        delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            seperator.handle(event)
        seperator.update(delta)

        screen.fill("white")
        seperator.draw()

        pygame.display.flip()
