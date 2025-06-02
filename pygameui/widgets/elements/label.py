"""PygameUI Label Widget Element"""

from typing import Union, Tuple, Optional, Any

import pygame

from pygameui.widgets.theme.theme import ThemeManager
from pygameui.widgets.core.widget import Widget
from pygameui.widgets.core.mixins import HoverableMixin

__all__ = ["Label"]


class Label(Widget, HoverableMixin):
    """
    Label with rounded corners, border, hover effect.

    Usage:
        ```python
        label = Label(master=screen, text="My Label")
        label.place(x=100,y=100)
        ...
            label.handel(event)
            label.update()
            label.draw()
        ...
        ```
    For detailed information check out the documentation.
    """

    def __init__(
        self,
        master: Optional[Union[Widget, pygame.Surface]] = None,
        width: int = 200,
        height: int = 40,
        text: str = "Label",
        font: Optional[Union[Tuple, pygame.Font]] = None,
        image: Union[pygame.Surface, None] = None,
        background: Optional[pygame.Color] = None,
        foreground: Optional[pygame.Color] = None,
        **kwargs
    ):
        """
        **kwargs (Dict):
            Other optional keyword arguments.
        """

        # Text
        self._text: str = text
        self._wraplenght: bool = kwargs.pop("wraplength", True)
        self._underline: bool = kwargs.pop("underline", False)

        # Font
        font_: pygame.Font = pygame.font.SysFont(
            ThemeManager.theme["font"]["family"], ThemeManager.theme["font"]["size"]
        )
        self._font: pygame.Font = font_ if font is None else font

        # Image/Icon
        self._image: pygame.Surface = image

        # shape
        self._border_radius: int = kwargs.pop(
            "border_radius",
            pygame.Color(ThemeManager.theme["Label"]["border_radius"]),
        )

        self._borderwidth: int = kwargs.pop(
            "borderwidth",
            pygame.Color(ThemeManager.theme["Label"]["borderwidth"]),
        )

        # Color
        self._foreground: pygame.Color = pygame.Color(
            ThemeManager.theme["Label"]["normal"]["foreground"]
            if foreground is None
            else foreground
        )
        self._background: pygame.Color = pygame.Color(
            ThemeManager.theme["Label"]["normal"]["background"]
            if background is None
            else background
        )

        self._hovercolor: pygame.Color = kwargs.pop(
            "hovercolor",
            pygame.Color(ThemeManager.theme["Label"]["hovered"]["foreground"]),
        )
        self._hoverbackground: pygame.Color = kwargs.pop(
            "hoverbackground",
            pygame.Color(ThemeManager.theme["Label"]["hovered"]["background"]),
        )

        self._bordercolor: pygame.Color = kwargs.pop(
            "bordercolor",
            pygame.Color(ThemeManager.theme["Label"]["bordercolor"]),
        )

        # other
        self._state: str = kwargs.pop("state", "normal")

        Widget.__init__(
            self, master, width, height, self._foreground, self._background, **kwargs
        )
        HoverableMixin.__init__(self)

    # region Public

    def get_text(self) -> str:
        """Get Label Text"""
        return self.configure(config="text")

    def set_text(self, new_text: str) -> None:
        """Set Label Text"""
        return self.configure(config=None, **{"text": new_text})

    # endregion

    # region Private

    def _set_state_(self, state: str = None) -> None:
        """Set the state of the label.
        If state is None, it will determine the state based on the current conditions.
        """

        if state is None:
            if self.hovered:
                self._state = "hovered"
            else:
                self._state = "normal"
        else:
            self._state = state

    def _get_state_foreground_(self) -> pygame.Color:
        """Get the foreground color based on the current state"""

        if self._state == "hovered":
            return self._hovercolor

        return self._foreground

    def _get_state_background_(self) -> pygame.Color:
        """Get the background color based on the current state"""

        if self._state == "hovered":
            return self._hoverbackground

        return self._background

    def _configure_set_(self, **kwargs) -> None:
        """Configure method to set custom attributes"""

        self._text = kwargs.pop("text", self._text)
        self._font = kwargs.pop("font", self._font)
        self._image = kwargs.pop("image", self._image)
        self._state = kwargs.pop("state", self._state)
        self._underline = kwargs.pop("underline", self._underline)

        self._hovercolor = kwargs.pop("hovercolor", self._hovercolor)
        self._hoverbackground = kwargs.pop("hoverbackground", self._hoverbackground)

        self._bordercolor = kwargs.pop("bordercolor", self._bordercolor)
        self._borderwidth = kwargs.get("borderwidth", self._borderwidth)
        self._border_radius = kwargs.get("border_radius", self._border_radius)

        super()._configure_set_(**kwargs)

    def _configure_get_(self, attribute: str) -> Any:
        """Configure method to get the current value of an attribute"""

        if attribute == "text":
            return self._text
        if attribute == "font":
            return self._font
        if attribute == "image":
            return self._image
        if attribute == "state":
            return self._state
        if attribute == "underline":
            return self._underline

        if attribute == "hovercolor":
            return self._hovercolor
        if attribute == "hoverbackground":
            return self._hoverbackground

        if attribute == "bordercolor":
            return self._bordercolor

        if attribute == "border_radius":
            return self._border_radius

        return super()._configure_get_(attribute)

    def _perform_draw_(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """Draw the widget on the given surface."""

        foreground = self._get_state_foreground_()
        background = self._get_state_background_()

        # Draw Label Background
        pygame.draw.rect(
            self._master,
            background,
            self._rect,
            border_radius=self._border_radius,
        )

        # Draw Label Border
        pygame.draw.rect(
            self._master,
            self._bordercolor,
            self._rect,
            self._borderwidth,
            self._border_radius,
        )

        # Draw Label Text
        btn_text = self._font.render(self._text, True, foreground)
        btn_text_rect = btn_text.get_rect(center=self._rect.center)
        self._master.blit(btn_text, btn_text_rect)

    def _handel_event_(self, event: pygame.Event, *args, **kwargs) -> None:
        """Handle an event for the widget."""
        self._check_hover(event)

    def _perform_update_(self, delta: float, *args, **kwargs) -> None:
        """Update the widget's logic."""
        self._set_state_()

    # endregion


# --------------------------------------------------------------------
# testing and demonstration stuff

if __name__ == "__main__":

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((480, 280))
    pygame.display.set_caption("PygameUI Label")

    label = Label(master=screen, text="My Label")

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            label.handel(event)
        label.update()

        screen.fill((10, 30, 50))
        label.draw()
        pygame.display.flip()

    pygame.quit()
