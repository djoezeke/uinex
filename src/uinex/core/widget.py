"""PygameUI Base Widget

This module defines the base Widget class for PygameUI, providing geometry management,
theming, visibility, and core widget functionality. All widgets should inherit from this class.

Features:
    - Geometry management via Pack, Place, and Grid
    - Theming and style support
    - Visibility control (show/hide)
    - Surface and rect management
    - Abstract methods for drawing, event handling, and updating

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & PygameUI Contributors
License: MIT
"""

from abc import abstractmethod
from inspect import signature
from typing import Union, Optional, Any, Callable
from pygame.event import Event
from pygame import Surface
import pygame
import time

from uinex.core.geometry import Grid, Pack, Place
from uinex.core.exceptions import PygameuiError

__all__ = ["Widget"]


class Widget(Place, Grid, Pack):
    """
    Base class for all PygameUI widgets.

    Features:
        - Geometry management (Pack, Place, Grid)
        - Theming and style support
        - Visibility and enable/disable control
        - Tooltip support
        - Focus and keyboard navigation
        - Z-order management (raise/lower)
        - Surface and rect management
        - Abstract methods for drawing, event handling, and updating

    Usage Example:
        widget = Widget(master=screen, width=100, height=40, tooltip="Info")
        widget.show()
        widget.focus()
        widget.handle(event)
        widget.update(delta=dt)
        widget.draw(surface=screen)
    """

    def __init__(
        self,
        master: Optional[Union["Widget", pygame.Surface]] = None,
        width: Union[float, int] = 100,
        height: Union[float, int] = 100,
        **kwargs,
    ) -> "Widget":
        """
        Initialize the Widget.

        Args:
            master (Widget or pygame.Surface, optional): Parent widget or surface.
            width (int or float): Width of the widget.
            height (int or float): Height of the widget.
            foreground (pygame.Color, optional): Foreground/text color.
            background (pygame.Color, optional): Background color.
            **kwargs: Additional configuration options.
        """
        pygame.font.init()
        self._cursor: pygame.Cursor = kwargs.pop("cursor", None)

        # Default theme
        self._theme: dict = {}

        custom_theme = {
            "background": (0, 120, 215),
            "disable_color": (0, 90, 180),
            "border_color": (0, 90, 180),
        }

        self._theme.update(custom_theme)

        if kwargs.pop("theme", None) is not None:
            self._theme.update(kwargs.pop("theme"))

        # Command/event handler registry
        self._handler: dict[int, Callable] = {}
        self._commands: dict[str, Callable] = {}

        # Inputs Events
        self._keyboard_enabled = True  # Enable/Accept Keyboard interaction
        self._joystick_enabled = False  # Enable/Accept Joystick interaction
        self._touchscreen_enabled = False  # Enable/Accept Touch interaction
        self._mouse_enabled = True  # Enable/Accept Mouse interaction

        # State, interactivity and Visibility
        self._state: str = "normal"  # Use set_state() to modify this status
        self._disabled: bool = False  # Use enable() or disable() to modify this status
        self._focused: bool = False  # Use focus() or unfocus() to modify this status
        self._visible: bool = True  # Use show() or hide() to modify this status

        # Set if widget need to be redrawn or not
        self._dirty: bool = True  # Use dirty property to modify this status

        # Widget Attributes
        self._height: int = height
        self._width: int = width

        # Border color, radius and width
        self._border_position: str = "none"

        self._border_radius: int = kwargs.pop("border_radius", 0)
        self._border_radius: Union[dict, int] = kwargs.pop("border_radius", 0)
        if isinstance(self._border_radius, dict):
            try:
                for side in ["left", "right", "top", "bottom"]:
                    self._border_radius[side] = int(self._border_radius.get(side, 0))
            except KeyError:
                self._border_radius = 0
        if isinstance(self._border_radius, int):
            self._border_radius = self._border_radius

        self._borderwidth: Union[dict, int] = kwargs.pop("borderwidth", 0)
        if isinstance(self._borderwidth, dict):
            try:
                for side in ["left", "right", "top", "bottom"]:
                    self._borderwidth[side] = int(self._borderwidth.get(side, 0))
            except KeyError:
                self._borderwidth = 0
        if isinstance(self._borderwidth, int):
            self._borderwidth = self._borderwidth

        # Shadow support
        self._shadow: bool = kwargs.pop("shadow", False)
        self._shadow_width: int = kwargs.pop("shadow_width", 0)
        self._shadowoffset: tuple[int, int] = kwargs.pop("shadowoffset", (5, 5))
        self._shadowcolor: pygame.Color = kwargs.pop("shadowcolor", (0, 0, 0))
        if isinstance(self._shadowcolor, str):
            self._shadowcolor = pygame.Color(self._shadowcolor)

        # Surface and rect setup
        self._surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        self._rect: pygame.Rect = self._surface.get_rect(topleft=(0, 0))
        self._blendmode: int = pygame.BLEND_RGBA_ADD
        self.blit_data = [self._surface, self._rect, None, self._blendmode]

        # Widget transforms
        self._angle: int = kwargs.pop("angle", 0)  # Rotation angle (degrees)
        self._flipx: bool = kwargs.pop("flipx", False)
        self._flipy: bool = kwargs.pop("flip", False)

        # Master Surface and Rect
        if isinstance(master, pygame.Rect):
            self._master: pygame.Surface = None
            self._master_rect: pygame.Rect = master
        if isinstance(master, pygame.Surface):
            self._master: pygame.Surface = master
            self._master_rect: pygame.Rect = master.get_rect()
        elif isinstance(master, Widget):
            self._master: pygame.Surface = master._surface
            self._master_rect: pygame.Rect = master._rect
        else:
            self._master: pygame.Surface = None
            self._master_rect: pygame.Rect = None

        # Widget Tooltip
        self._tooltip: str = self._kwarg_get(kwargs, "tooltip", "")
        self._show_tooltip: bool = False
        self._tooltip_delay: float = kwargs.pop("tooltip_delay", 0.5)  # seconds
        self._tooltip_timer: float = 0.0

        # Surface and rect setup
        self._surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)  # Surface of the widget
        self._rect: pygame.Rect = self._surface.get_rect(topleft=(0, 0))  # To position the widget

        # Blending and Blitting Data
        self._blendmode: int = pygame.BLEND_RGBA_ADD
        self.blit_data: Union[tuple, list] = [
            self._surface,
            self._rect,
            None,
            self._blendmode,
        ]

        # Initialize geometry managers
        Place.__init__(self)
        Grid.__init__(self)
        Pack.__init__(self)

        self._after_queue = []  # List of (run_at, callable, args, kwargs)

    def __getitem__(self, config: str) -> Any:
        """Get an item from the widget's configuration."""
        return self.configure(config=config)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set an item in the widget's configuration."""
        self.configure(config=None, **{key: value})

    def __repr__(self):
        """Return a string representation of the widget."""
        return f"{self.__class__.__name__}()"

    def __str__(self):
        """Return a string representation of the widget."""
        return f"<{self.__class__.__name__} widget at {self._rect.topleft} of size {self._rect.size}>"

    def __copy__(self) -> "Widget":
        """
        Copy method.

        :return: Raises copy exception
        """
        raise PygameuiError("Widget class cannot be copied")

    def __deepcopy__(self, memodict: dict) -> "Widget":
        """
        Deep-copy method.

        :param memodict: Memo dict
        :return: Raises copy exception
        """
        raise PygameuiError("Widget class cannot be deep-copied")

    # region Properties

    @property
    def state(self) -> str:
        """Get or Set the current state of the widget."""
        return self._state

    @state.setter
    def state(self, value: str):
        if len(value) < 6:
            raise ValueError(f"Unknown State {value}")
        self._state = value

    @property
    def focused(self) -> bool:
        """Get or Set the widget is focused."""
        return self._focused

    @focused.setter
    def focused(self, value: bool):
        self._focused = value

    @property
    def dirty(self) -> bool:
        """Get or Set the widget is dirty."""
        return self._dirty

    @dirty.setter
    def dirty(self, value: bool):
        self._dirty = value

    @property
    def keyboard(self) -> bool:
        """Get or Set the widget keyboard interaction."""
        return self._keyboard_enabled

    @keyboard.setter
    def keyboard(self, value: bool):
        self._keyboard_enabled = value

    @property
    def mouse(self) -> bool:
        """Get or Set the widget mouse interaction."""
        return self._mouse_enabled

    @mouse.setter
    def mouse(self, value: bool):
        self._mouse_enabled = value

    @property
    def joystick(self) -> bool:
        """Get or Set the widget joystick interaction."""
        return self._joystick_enabled

    @joystick.setter
    def joystick(self, value: bool):
        self._joystick_enabled = value

    @property
    def touchscreen(self) -> bool:
        """Get or Set the widget touchscreen interaction."""
        return self._touchscreen_enabled

    @touchscreen.setter
    def touchscreen(self, value: bool):
        self._touchscreen_enabled = value

    @property
    def width(self) -> int:
        """Get or set the width of the widget."""
        return self._width

    @width.setter
    def width(self, value: int):
        if value < 0:
            raise ValueError("Width must be a non-negative integer")
        self._width = value

    @property
    def height(self) -> int:
        """Get or set the height of the widget."""
        return self._height

    @height.setter
    def height(self, value: int):
        if value < 0:
            raise ValueError("Height must be a non-negative integer")
        self._height = value

    @property
    def visible(self) -> bool:
        """Get or set the widget's visibility."""
        return self._get_visible_()

    @visible.setter
    def visible(self, value) -> None:
        self._set_visible_(value)

    @property
    def surface(self) -> Surface:
        """Get or set the widget's surface."""
        return self._surface

    @surface.setter
    def surface(self, value: Surface) -> None:
        self._surface = value
        self.blit_data[0] = self._surface

    @property
    def rect(self) -> pygame.Rect:
        """Get or set the widget's rectangle."""
        return self._rect

    @rect.setter
    def rect(self, value) -> None:
        self._rect = value
        self.blit_data[1] = self._rect

    @property
    def blendmode(self) -> int:
        """Get or set the widget's blend mode."""
        return self._blendmode

    @blendmode.setter
    def blendmode(self, value: int) -> None:
        self._blendmode = value
        self.blit_data[3] = self._blendmode

    @property
    def theme(self) -> Optional[str]:
        """Return the name of the widget's theme."""
        return "light"

    @property
    def style(self) -> dict:
        """Get or set the widget's Style Theme."""
        return self._theme

    @property
    def disabled(self) -> bool:
        """Return True if the widget is disabled."""
        return self._disabled

    # endregion Properties

    # region Abstracts

    @abstractmethod
    def _perform_draw_(self, surface: Surface, *args, **kwargs) -> None:
        """
        Draw the widget on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def _handle_event_(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for the widget.

        Args:
            event (pygame.Event): The event to handle.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def _perform_update_(self, delta: float, *args, **kwargs) -> None:
        """
        Update the widget's logic.

        Args:
            delta (float): Time since last update.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    # endregion Abstracts

    @classmethod
    def set_theme(cls, theme_dict):
        """Set the widget's theme."""
        cls._theme = theme_dict.get(cls.__name__, {})

    # region Public

    def draw(self, *args, surface: Surface = None, **kwargs) -> None:
        """
        Draw the widget on the given surface.

        Args:
            surface (pygame.Surface, optional): The surface to draw on.
        """
        if self._visible:
            if self.__class__.__name__ == "Widget":
                if self._master is not None:
                    surface = self._master
                pygame.draw.rect(surface, self._theme["background"], self._rect.inflate(-20, -20), border_radius=1)
                self._dirty = False
            else:
                if self._master is not None:
                    surface = surface or self._master
                self._perform_draw_(surface, *args, **kwargs)
            self._draw_tooltip_(surface)
            self._dirty = False

    def handle(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for the widget.

        Args:
            event (pygame.Event): The event to handle.
        """
        if event.type == pygame.KEYDOWN and self._focused:
            self.on_keydown(event)
        elif event.type == pygame.KEYUP and self._focused:
            self.on_keyup(event)
        self._handle_event_(event, *args, **kwargs)
        try:
            command = self._handler[event.type]
            command()
        except KeyError:
            pass

    def update(self, *args, delta: float = 0.0, **kwargs) -> None:
        """
        Update the widget's logic.

        Args:
            delta (float): Time since last update.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self._visible:
            self._process_after_queue()
            self._perform_update_(delta, *args, **kwargs)
            self._update_tooltip_(mouse_pos, delta)

    def configure(self, config=None, **kwargs):
        """
        Configure the options for this widget.

        Args:
            config (str, optional): If provided, gets the value of this config.
            **kwargs: If provided, sets the given configuration options.

        Returns:
            Any: The value of the config if requested, otherwise None.
        """
        if config is not None:
            return self._configure_get_(config)
        return self._configure_set_(**kwargs)

    def setconfig(self, **kwargs):
        """
        Configure the options for this widget.

        Args:
            **kwargs: Sets the given configuration options.
        """
        return self._configure_set_(**kwargs)

    def getconfig(self, config=None):
        """
        Get configuration options for this widget.

        Args:
            config (str): Gets the value of this config.

        Returns:
            Any: The value of the config if requested, otherwise None.
        """
        return self._configure_get_(config)

    def bind(self, event: int, function: Optional[Callable] = None):
        """
        Bind a function to a button event.

        Args:
            event (int): Pygame event type.
            function (callable, optional): Function to call.
        """
        if function is None:
            return

        if callable(function):
            num_params = len(signature(function).parameters)
            if num_params == 0:
                self._handler[event] = function
            elif num_params == 1:
                self._handler[event] = lambda: function(self)
            else:
                raise ValueError("Command function signatures can have 0 or 1 parameter.")
        else:
            raise TypeError("Command function must be callable")

    def unbind(self, event: int):
        """
        Unbind a function from a Widget event.

        Args:
            event (int): Pygame event type.
        """
        return self._handler.pop(event, None)

    def post(self, event: int, data: Optional[dict[str, Any]] = None):
        """
        Widget to trigger/post an event.

        Args:
            event (int): The event to trigger.
            data (dict, optional): Event data.
        """
        if data is None:
            data = {}
        data.update({"widget": self})
        pygame.event.post(pygame.event.Event(event, data))

    def after(self, ms: int, function: Union[Callable, str], *args, **kwargs) -> str:
        """
        Call function once after given time (in milliseconds).
        Args:
            ms (int): Time in milliseconds.
            function (callable or str): Function or command name.
            *args, **kwargs: Arguments to pass to the function.
        """
        run_at = time.time() + ms / 1000.0
        if isinstance(function, str):

            def callback():
                self.call(function, *args, **kwargs)

        elif callable(function):

            def callback():
                function(*args, **kwargs)

        else:
            raise TypeError("Function must be a callable or command name string.")
        self._after_queue.append((run_at, callback))
        return str(float(run_at))  # Return a handle (timestamp string)

    def _process_after_queue(self):
        """Check and run scheduled after callbacks."""
        now = time.time()
        to_run = [item for item in self._after_queue if item[0] <= now]
        self._after_queue = [item for item in self._after_queue if item[0] > now]
        for _, callback in to_run:
            try:
                callback()
            except Exception:
                pass

    def mainloop(self, *args, surface: Surface = None, **kwargs) -> None:
        """
        Draw the widget on the given surface. Basically for testing.

        Args:
            surface (pygame.Surface, optional): The surface to draw on.
        """
        pygame.init()
        pygame.font.init()

        fps = kwargs.get("fps", 60)
        assert isinstance(fps, int)

        if surface is None:
            surface = pygame.display.set_mode((self._rect.width + 100, self._rect.height + 100))
            pygame.display.set_caption(f"PygameUI {self.__class__.__name__} ")
            self._master = surface
            self.pack(anchor="center")
        else:
            assert isinstance(surface, pygame.Surface)

        clock = pygame.time.Clock()

        # Start loop
        running: bool = True
        while running:
            delta = clock.tick(fps) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.handle(event)
            self.update(delta)
            self.draw()
            pygame.display.flip()

    def hide(self) -> None:
        """Hide the widget (set visibility to False)."""
        self._set_visible_(False)

    def focus(self):
        """Set focus to this widget."""
        self._focused = True

    def unfocus(self):
        """Remove focus from this widget."""
        self._focused = False

    def on_focus(self):
        """Override: Called when widget receives focus."""

    def on_unfocus(self):
        """Override: Called when widget loses focus."""

    def on_keydown(self, event: Event):
        """Override: Called when a key is pressed while focused."""

    def on_keyup(self, event: Event):
        """Override: Called when a key is released while focused."""

    def show(self) -> None:
        """Show the widget (set visibility to True)."""
        self._set_visible_(True)

    def set_tooltip(self, text: str, delay: float = 0.5):
        """Set the tooltip text and optional delay (in seconds)."""
        self._tooltip = text
        self._tooltip_delay = delay

    def enable(self):
        """Enable the widget for interaction."""
        if self._disabled:
            self._disabled = False
            self._state = "normal"
            self._enable_()

    def disable(self):
        """Disable the widget (no interaction)."""
        if not self._disabled:
            self._disabled = True
            self._state = "disabled"
            self._disable_()

    def lift(self):
        """Bring this widget to the top of its parent's stacking order."""
        if hasattr(self._master, "widgets"):
            self._master.widgets.remove(self)
            self._master.widgets.append(self)

    def lower(self):
        """Send this widget to the bottom of its parent's stacking order."""
        if hasattr(self._master, "widgets"):
            self._master.widgets.remove(self)
            self._master.widgets.insert(0, self)

    def resize(self, width, height):
        """Resize this widget"""
        self._width = width
        self._height = height

    # endregion

    # region Private

    def _configure_set_(self, **kwargs) -> None:
        """
        Set widget configuration options.

        Args:
            **kwargs: Configuration options to set.
        """

        self._height = self._kwarg_get(kwargs, "height", self._height)
        self._width = self._kwarg_get(kwargs, "width", self._width)
        self._cursor = self._kwarg_get(kwargs, "cursor", self._cursor)
        self._theme = self._kwarg_get(kwargs, "cursor", self._theme)
        self._state = self._kwarg_get(kwargs, "state", self._state)
        self._disabled = self._kwarg_get(kwargs, "disabled", self._disabled)
        self._focused = self._kwarg_get(kwargs, "focused", self._focused)
        self._visible = self._kwarg_get(kwargs, "visible", self._visible)
        self._dirty = self._kwarg_get(kwargs, "dirty", self._dirty)

        self._shadow = self._kwarg_get(kwargs, "shadow", self._shadow)
        self._shadow_width = self._kwarg_get(kwargs, "shadow_width", self._shadow_width)
        self._shadowoffset = self._kwarg_get(kwargs, "shadowoffset", self._shadowoffset)
        self._shadowcolor = self._kwarg_get(kwargs, "shadowcolor", self._shadowcolor)

        self._surface = self._kwarg_get(kwargs, "surface", self._surface)
        self._rect = self._kwarg_get(kwargs, "rect", self._rect)

        self._angle = self._kwarg_get(kwargs, "angle", self._angle)
        self._flipx = self._kwarg_get(kwargs, "flipx", self._flipx)
        self._flipy = self._kwarg_get(kwargs, "flipy", self._flipy)

        self._master = self._kwarg_get(kwargs, "master", self._master)
        self._master_rect = self._kwarg_get(kwargs, "master_rect", self._master_rect)

        self._tooltip = self._kwarg_get(kwargs, "shadow", self._shadow)
        self._show_tooltip = self._kwarg_get(kwargs, "show_tooltip", self._show_tooltip)
        self._tooltip_delay = self._kwarg_get(kwargs, "tooltip_delay", self._tooltip_delay)
        self._tooltip_timer = self._kwarg_get(kwargs, "tooltip_timer", self._tooltip_timer)

        self._border_radius = self._kwarg_get(kwargs, "border_radius", self._border_radius)
        self._borderwidth = self._kwarg_get(kwargs, "borderwidth", self._borderwidth)
        self._bordermode = self._kwarg_get(kwargs, "bordermode", self._bordermode)
        self._border_position = self._kwarg_get(kwargs, "border_position", self._border_position)

        # background
        # disable_color
        # shadowcolor
        # bordercolor

    def _configure_get_(self, attribute: str) -> Any:
        """
        Get a widget configuration value.

        Args:
            attribute (str): The attribute name.

        Returns:
            Any: The value of the attribute.
        """
        if attribute == "surface":
            return self._surface
        if attribute == "rect":
            return self._rect
        if attribute == "master":
            return self._master
        if attribute == "master_rect":
            return self._master_rect
        if attribute == "height":
            return self._height
        if attribute == "width":
            return self._width
        if attribute == "cursor":
            return self._cursor
        if attribute == "theme":
            return self._theme
        if attribute == "state":
            return self._state
        if attribute == "disabled":
            return self._disabled
        if attribute == "focused":
            return self._focused
        if attribute == "visible":
            return self._visible
        if attribute == "dirty":
            return self._dirty
        if attribute == "shadow":
            return self._shadow
        if attribute == "shadow_width":
            return self._shadow_width
        if attribute == "shadowoffset":
            return self._shadowoffset
        if attribute == "shadowcolor":
            return self._shadowcolor
        if attribute == "angle":
            return self._angle
        if attribute == "flipx":
            return self._flipx
        if attribute == "flipy":
            return self._flipy
        if attribute == "tooltip":
            return self._tooltip
        if attribute == "show_tooltip":
            return self._show_tooltip
        if attribute == "tooltip_delay":
            return self._tooltip_delay
        if attribute == "tooltip_timer":
            return self._tooltip_timer
        if attribute == "border_radius":
            return self._border_radius
        if attribute == "borderwidth":
            return self._borderwidth
        if attribute == "bordermode":
            return self._bordermode
        if attribute == "border_position":
            return self._border_position

        if attribute == "background":
            return
        if attribute == "disable_color":
            return
        if attribute == "shadowcolor":
            return
        if attribute == "bordercolor":
            return

        return None

    def _set_visible_(self, value) -> None:
        """Set the widget's visibility (True or False)."""
        self._visible = value

    def _get_visible_(self) -> bool:
        """Return the widget's visibility."""
        return self._visible

    def _update_tooltip_(self, mouse_pos, delta):
        """Update tooltip display logic. Call in update()."""
        if self._tooltip:
            if self._rect.collidepoint(mouse_pos):
                self._tooltip_timer += delta
                if self._tooltip_timer >= self._tooltip_delay:
                    self._show_tooltip = True
            else:
                self._tooltip_timer = 0.0
                self._show_tooltip = False

    def _draw_tooltip_(self, surface):
        """Draw the tooltip if needed. Call in draw()."""
        if self._show_tooltip:
            font = pygame.font.SysFont("Arial", 16)
            text_surf = font.render(self._tooltip, True, (255, 255, 255))
            bg_rect = text_surf.get_rect()
            bg_rect.topleft = (self._rect.right + 8, self._rect.top)
            pygame.draw.rect(surface, (0, 0, 0, 180), bg_rect.inflate(8, 8))
            surface.blit(text_surf, bg_rect)

    def _enable_(self):
        """Run by subclass after enable()"""

    def _disable_(self):
        """Run by subclass after disable()"""

    def _set_theme_color_(self):
        """
        Set the widget's theme color.

        Can be overridden by subclasses, but super method must be called at the beginning.
        """

    def _get_theme_color_(self):
        """
        Get the widget's appearance mode as a string, 'light' or 'dark'.

        Can be overridden by subclasses.
        """

    def _kwarg_get(
        self, params: dict[str, Any], key: str, default: Any = None, value_type: Optional[str] = None
    ) -> Any:
        """
        Return a value from a dictionary.

        Custom types (str)
            -   color       – Color or :py:class:`pygame.Color`
            -   border      – Border
            -   rect        – Color or :py:class:`pygame.Rect`
            -   surface     – Color :py:class:`pygame.Surface`

        :param params: Parameters dictionary
        :param key: Key to look for
        :param default: Default value to return
        :param value_type: type of output
        :return: The value associated to the key
        """

        if not isinstance(params, dict):
            raise Exception("Params must be of type dict.")

        if not isinstance(key, str):
            raise Exception("Key must be of type str.")

        value = params.pop(key, default)

        if value_type is not None:
            if isinstance(value_type, str):
                if value_type == "color":
                    if isinstance(value, pygame.Color):
                        return value
                    if isinstance(value, str):
                        return pygame.Color(value)
                    raise Exception(f"Value Cant be Of type {value_type}")
                if value_type == "surface":
                    if isinstance(value, pygame.Surface):
                        return value
                    if isinstance(value, "Widget"):
                        return value._surface
                    raise Exception(f"Value Cant be Of type {value_type}")
                if value_type == "rect":
                    if isinstance(value, pygame.Rect):
                        return value
                    if isinstance(value, pygame.Surface):
                        return value.get_rect()
                    if isinstance(value, "Widget"):
                        return value._rect
                    raise Exception(f"Value Cant be Of type {value_type}")
                if value_type == "border":
                    if isinstance(value, int):
                        return value
                    if isinstance(value, dict):
                        try:
                            for side in ["left", "right", "top", "bottom"]:
                                value[side] = int(value.get(side))
                            return value
                        except KeyError:
                            raise Exception("Invalid sides")
                    raise Exception(f"Value Cant be Of type {value_type}")
                if value_type == "angle":
                    if isinstance(value, int):
                        if value >= 0 and value <= 360:
                            return value
                        raise Exception(f"Angle must range 0-360 not {value}")
                    raise Exception(f"Value Cant be Of type {value_type}")

        return value

    def rotate(self, angle: int) -> "Widget":
        """Rotation Widget angle (degrees ``0-360``)"""
        assert isinstance(angle, int)
        if angle == self._angle:
            return self
        self._surface = pygame.transform.rotate(self._surface, angle)
        self._angle = angle % 360
        return self

    # endregion
