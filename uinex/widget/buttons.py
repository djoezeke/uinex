"""Uinex Button Widget Element

This module defines the Button widget for Uinex, supporting rounded corners,
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

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & Uinex Contributors
License: MIT
"""

from collections.abc import Callable
from typing import Any

import pygame

from uinex.theme.manager import ThemeManager
from uinex.utils.mixins import ClickableMixin
from uinex.utils.mixins import DoubleClickMixin
from uinex.utils.mixins import HoverableMixin
from uinex.widget.base import Widget


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
        master: Any | None = None,
        width: int = 100,
        height: int = 40,
        text: str = "Button",
        state: str = "normal",
        disabled: bool = False,
        font: tuple | pygame.font.Font | None = None,
        image: pygame.Surface | None = None,
        background: pygame.Color | None = None,
        text_color: pygame.Color | None = None,
        hovercolor: pygame.Color | None = None,
        border_color: pygame.Color | None = None,
        command: Callable[[], Any] | None | None = None,
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
            ThemeManager.theme["Font"]["family"], ThemeManager.theme["font"]["size"]
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
        self._theme.update(ThemeManager.theme.get(self.__class__.__name__, {}))
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
    pygame.display.set_caption("Uinex Label")
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

"""Uinex CheckButton Widget

This module defines the CheckButton widget for Uinex, supporting modern theming,
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

Author: Sackey Ezekiel Etrue & Uinex Contributors
License: MIT
"""


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
        master: Any | None = None,
        text: str = "",
        checked: bool = False,
        command: Callable[[bool], None] | None = None,
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


"""Uinex RadioButton Widget

A RadioButton is a circular button that can be selected or deselected, typically used in groups
where only one button can be selected at a time. This widget provides a customizable radio button
with label, group management, and event handling.

Features:
    - Customizable size, colors, and label
    - Grouping support (only one button in a group can be selected)
    - Mouse interaction (select on click)
    - Callback support for selection changes

Example:
    rb1 = RadioButton(master, text="Option 1", group="group1", checked=True)
    rb2 = RadioButton(master, text="Option 2", group="group1")
    rb1.on_change = lambda checked: print("rb1 checked:", checked)

Author: Sackey Ezekiel Etrue & Uinex Contributors
License: MIT
"""

# Internal registry for radio button groups
_RADIO_GROUPS = {}


class RadioButton(Widget):
    """
    A circular radio button widget with label and group support.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        text (str): Label text for the radio button.
        group (str, optional): Group name for mutual exclusivity.
        checked (bool, optional): Initial checked state.
        radius (int, optional): Radius of the radio button circle.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        circle_color (pygame.Color, optional): Color of the radio circle.
        check_color (pygame.Color, optional): Color of the inner dot when checked.
        font (pygame.font.Font, optional): Font for the label.
        on_change (callable, optional): Callback when checked state changes.
        **kwargs: Additional widget options.

    Attributes:
        checked (bool): Whether the radio button is selected.
        text (str): The label text.
        group (str): The group name.
        on_change (callable): Callback for checked state changes.
    """

    def __init__(
        self,
        master,
        text="",
        group=None,
        checked=False,
        radius=12,
        foreground=(0, 0, 0),
        background=(255, 255, 255, 0),
        circle_color=(80, 80, 80),
        check_color=(30, 144, 255),
        font=None,
        on_change=None,
        **kwargs,
    ):
        self.text = text
        self.group = group
        self.checked = checked
        self.radius = radius
        self.circle_color = circle_color
        self.check_color = check_color
        self.on_change = on_change
        self.font = font or pygame.font.SysFont(None, 20)
        self._label_surface = self.font.render(self.text, True, foreground)
        width = 2 * radius + 8 + self._label_surface.get_width()
        height = max(2 * radius, self._label_surface.get_height()) + 4
        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

        # Register in group
        if group:
            _RADIO_GROUPS.setdefault(group, []).append(self)

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the radio button and label."""
        # Draw background
        if self._background:
            surface.fill(self._background)

        # Draw radio circle
        center = (self.radius + 4, self._rect.centery)
        pygame.draw.circle(surface, self.circle_color, center, self.radius, 2)

        # Draw checked dot
        if self.checked:
            pygame.draw.circle(surface, self.check_color, center, self.radius - 5)

        # Draw label
        label_pos = (
            2 * self.radius + 8,
            (self._rect.height - self._label_surface.get_height()) // 2,
        )
        surface.blit(self._label_surface, label_pos)

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse click to toggle checked state."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                if not self.checked:
                    self.select()

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic (not used for static radio button)."""

    def select(self):
        """Select this radio button and unselect others in the group."""
        if self.group:
            for rb in _RADIO_GROUPS.get(self.group, []):
                if rb is not self and rb.checked:
                    rb.checked = False
                    if rb.on_change:
                        rb.on_change(False)
        if not self.checked:
            self.checked = True
            if self.on_change:
                self.on_change(True)
        self._dirty = True

    def deselect(self):
        """Deselect this radio button."""
        if self.checked:
            self.checked = False
            if self.on_change:
                self.on_change(False)
        self._dirty = True

    def configure(self, config=None, **kwargs):
        """
        Get or set configuration options.

        Args:
            config (str, optional): Name of config to get.
            **kwargs: Configs to set.

        Returns:
            Any: Value of config if requested.
        """
        if config is not None:
            if config == "checked":
                return self.checked
            if config == "text":
                return self.text
            if config == "group":
                return self.group
            return super().configure(config)
        if "checked" in kwargs:
            if kwargs["checked"]:
                self.select()
            else:
                self.deselect()
        if "text" in kwargs:
            self.text = kwargs["text"]
            self._label_surface = self.font.render(self.text, True, self._foreground)
        if "group" in kwargs:
            old_group = self.group
            self.group = kwargs["group"]
            if old_group and self in _RADIO_GROUPS.get(old_group, []):
                _RADIO_GROUPS[old_group].remove(self)
            if self.group:
                _RADIO_GROUPS.setdefault(self.group, []).append(self)


"""Uinex MenuButton Widget

A MenuButton is a button that displays a dropdown menu when clicked. It is commonly used
for toolbars, context menus, and navigation bars. The MenuButton supports custom labels,
menu items, callbacks, and integrates with the Uinex event and layout system.

Features:
    - Displays a dropdown menu on click
    - Customizable label, font, and colors
    - Supports menu item callbacks
    - Keyboard and mouse interaction
    - Integrates with layout managers

Example:
    mb = MenuButton(master, text="File", menu_items=[("Open", on_open), ("Save", on_save)])
    mb.on_select = lambda label: print("Selected:", label)

Author: Sackey Ezekiel Etrue & Uinex Contributors
License: MIT
"""


class MenuButton(Widget):
    """
    A button that displays a dropdown menu when clicked.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        text (str): Button label.
        menu_items (list): List of (label, callback) tuples for menu items.
        width (int, optional): Width of the button.
        height (int, optional): Height of the button.
        font (pygame.font.Font, optional): Font for the label.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        menu_background (pygame.Color, optional): Menu background color.
        menu_foreground (pygame.Color, optional): Menu text color.
        on_select (callable, optional): Callback when a menu item is selected.
        **kwargs: Additional widget options.

    Attributes:
        text (str): Button label.
        menu_items (list): List of (label, callback) tuples.
        menu_open (bool): Whether the menu is open.
        selected_index (int): Index of the currently hovered menu item.
        on_select (callable): Callback for menu item selection.
    """

    def __init__(
        self,
        master,
        text="Menu",
        menu_items=None,
        width=100,
        height=32,
        font=None,
        foreground=(0, 0, 0),
        background=(230, 230, 230),
        menu_background=(255, 255, 255),
        menu_foreground=(0, 0, 0),
        on_select=None,
        **kwargs,
    ):
        self.text = text
        self.menu_items = menu_items or []
        self.menu_open = False
        self.selected_index = -1
        self.on_select = on_select

        self.font = font or pygame.font.SysFont(None, 20)
        self.foreground = foreground
        self.background = background
        self.menu_background = menu_background
        self.menu_foreground = menu_foreground

        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the button and dropdown menu if open."""
        rect = surface.get_rect()
        # Draw button background
        surface.fill(self.background)
        # Draw button border
        pygame.draw.rect(surface, (120, 120, 120), rect, 1)
        # Draw label
        label_surf = self.font.render(self.text, True, self.foreground)
        label_rect = label_surf.get_rect(center=rect.center)
        surface.blit(label_surf, label_rect)
        # Draw dropdown arrow
        arrow_x = rect.right - 18
        arrow_y = rect.centery
        pygame.draw.polygon(
            surface,
            self.foreground,
            [
                (arrow_x, arrow_y - 4),
                (arrow_x + 8, arrow_y - 4),
                (arrow_x + 4, arrow_y + 4),
            ],
        )
        # Draw menu if open
        if self.menu_open and self.menu_items:
            menu_width = rect.width
            menu_height = rect.height * len(self.menu_items)
            menu_rect = pygame.Rect(rect.left, rect.bottom, menu_width, menu_height)
            pygame.draw.rect(surface, self.menu_background, menu_rect)
            pygame.draw.rect(surface, (120, 120, 120), menu_rect, 1)
            for i, (label, _) in enumerate(self.menu_items):
                item_rect = pygame.Rect(
                    menu_rect.left,
                    menu_rect.top + i * rect.height,
                    menu_rect.width,
                    rect.height,
                )
                if i == self.selected_index:
                    pygame.draw.rect(surface, (200, 220, 255), item_rect)
                item_surf = self.font.render(str(label), True, self.menu_foreground)
                surface.blit(
                    item_surf,
                    (
                        item_rect.left + 8,
                        item_rect.centery - item_surf.get_height() // 2,
                    ),
                )

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse and keyboard events for menu interaction."""
        rect = self._rect
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = (event.pos[0] - rect.x, event.pos[1] - rect.y)
            if rect.collidepoint(event.pos):
                self.menu_open = not self.menu_open
                self.selected_index = -1
                self._dirty = True
            elif self.menu_open:
                menu_rect = pygame.Rect(
                    rect.left,
                    rect.bottom,
                    rect.width,
                    rect.height * len(self.menu_items),
                )
                if menu_rect.collidepoint(event.pos[0] - rect.x, event.pos[1] - rect.y):
                    idx = (event.pos[1] - rect.y - rect.height) // rect.height
                    if 0 <= idx < len(self.menu_items):
                        self.selected_index = idx
                        self._select_menu_item(idx)
                else:
                    self.menu_open = False
                    self.selected_index = -1
                    self._dirty = True
        elif event.type == pygame.MOUSEMOTION and self.menu_open:
            menu_rect = pygame.Rect(
                rect.left,
                rect.bottom,
                rect.width,
                rect.height * len(self.menu_items),
            )
            mx, my = event.pos[0] - rect.x, event.pos[1] - rect.y
            if menu_rect.collidepoint(mx, my):
                idx = (my - rect.height) // rect.height
                if 0 <= idx < len(self.menu_items):
                    if self.selected_index != idx:
                        self.selected_index = idx
                        self._dirty = True
                else:
                    if self.selected_index != -1:
                        self.selected_index = -1
                        self._dirty = True
            else:
                if self.selected_index != -1:
                    self.selected_index = -1
                    self._dirty = True
        elif event.type == pygame.KEYDOWN and self.menu_open:
            if event.key == pygame.K_DOWN:
                if self.selected_index < len(self.menu_items) - 1:
                    self.selected_index += 1
                    self._dirty = True
            elif event.key == pygame.K_UP:
                if self.selected_index > 0:
                    self.selected_index -= 1
                    self._dirty = True
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if 0 <= self.selected_index < len(self.menu_items):
                    self._select_menu_item(self.selected_index)
            elif event.key == pygame.K_ESCAPE:
                self.menu_open = False
                self.selected_index = -1
                self._dirty = True

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for MenuButton (not used)."""
        pass

    def _select_menu_item(self, idx):
        """Select a menu item and trigger callback."""
        self.menu_open = False
        label, callback = self.menu_items[idx]
        if self.on_select:
            self.on_select(label)
        if callable(callback):
            callback()
        self.selected_index = -1
        self._dirty = True

    def configure(self, config=None, **kwargs):
        """
        Get or set configuration options.

        Args:
            config (str, optional): Name of config to get.
            **kwargs: Configs to set.

        Returns:
            Any: Value of config if requested.
        """
        if config is not None:
            if config == "text":
                return self.text
            if config == "menu_items":
                return self.menu_items
            if config == "menu_open":
                return self.menu_open
            return super().configure(config)
        if "text" in kwargs:
            self.text = kwargs["text"]
        if "menu_items" in kwargs:
            self.menu_items = kwargs["menu_items"]
