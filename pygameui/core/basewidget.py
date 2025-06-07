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
from typing import Union, Optional, Any, List, Type
from pygame.event import Event
from pygame import Surface
import pygame

from pygameui.core.geometry import Grid, Pack, Place

__all__ = ["_Widget"]


class PygameuiError(Exception):
    """
    If Pygameui Error Occurs.
    """

    def __init__(self, *args):
        super().__init__(*args)


class _Widget(Place, Grid, Pack):
    """
    Base class for all PygameUI widgets.

    Inherits geometry managers (Pack, Place, Grid) and provides:
        - Surface and rect management
        - Visibility control
        - Theming and style hooks
        - Abstract methods for drawing, event handling, and updating

    Args:
        master (_Widget or pygame.Surface, optional): Parent widget or surface.
        width (int or float): Width of the widget.
        height (int or float): Height of the widget.
        foreground (pygame.Color, optional): Foreground/text color.
        background (pygame.Color, optional): Background color.
        cursor (pygame.Cursor, optional): Mouse cursor for the widget.
        shadow (bool, optional): Whether to draw a shadow.
        shadowoffset (tuple[int, int], optional): Shadow offset.
        shadowcolor (pygame.Color or str, optional): Shadow color.
        **kwargs: Additional configuration options.

    Attributes:
        _surface (pygame.Surface): The widget's surface.
        _rect (pygame.Rect): The widget's rectangle.
        _master (pygame.Surface): The parent surface.
        _visible (bool): _Widget visibility.
        _style (Style): _Widget style object.
        _blendmode (int): Pygame blend mode.
        blit_data (list): Data for blitting the widget.
    """

    def __init__(
        self,
        master: Optional[Union["_Widget", pygame.Surface]] = None,
        width: Union[float, int] = 100,
        height: Union[float, int] = 100,
        foreground: pygame.Color = None,
        background: pygame.Color = None,
        **kwargs,
    ) -> "_Widget":
        """
        Initialize the _Widget.

        Args:
            master (_Widget or pygame.Surface, optional): Parent widget or surface.
            width (int or float): Width of the widget.
            height (int or float): Height of the widget.
            foreground (pygame.Color, optional): Foreground/text color.
            background (pygame.Color, optional): Background color.
            **kwargs: Additional configuration options.
        """
        # """
        # Button widget.

        # The arguments and unknown keyword arguments are passed to the ``onreturn``
        # function:

        # .. code-block:: python

        #     onreturn(*args, **kwargs)

        # .. note::

        #     Button accepts all transformations.

        # :param title: Button title
        # :param button_id: Button ID
        # :param onreturn: Callback when pressing the button
        # :param args: Optional arguments for callbacks
        # :param kwargs: Optional keyword arguments
        # """

        # Master Surface and Rect
        if isinstance(master, pygame.Rect):
            self._master: pygame.Surface = None
            self._master_rect: pygame.Rect = master
        if isinstance(master, pygame.Surface):
            self._master: pygame.Surface = master
            self._master_rect: pygame.Rect = master.get_rect()
        elif isinstance(master, _Widget):
            self._master: pygame.Surface = master._surface
            self._master_rect: pygame.Rect = master._rect
        else:
            self._master: pygame.Surface = None
            self._master_rect: pygame.Rect = None

        # Surface and rect setup
        self._surface = pygame.Surface(
            (width, height), pygame.SRCALPHA, 32
        )  # Surface of the widget
        self._rect: pygame.Rect = self._surface.get_rect(
            topleft=(0, 0)
        )  # To position the widget

        # Blending and Blitting Data
        self._blendmode: int = pygame.BLEND_RGBA_ADD
        self.blit_data: Union[tuple, list] = [
            self._surface,
            self._rect,
            None,
            self._blendmode,
        ]

        self._cursor: pygame.Cursor = kwargs.pop("cursor", None)

        self._events = []

        # Widget transforms
        self._angle = 0  # Rotation angle (degrees)
        self._flip = (False, False)  # x, y
        self._scale = [False, 1, 1, False]  # do_scale, x, y, smooth
        self._scale_factor = (1, 1)  # Transformed/Original in x, y
        self._translate = (0, 0)

        # Inputs Events
        self._keyboard_enabled = True  # Enable/Accept Keyboard interaction
        self._joystick_enabled = False  # Enable/Accept Joystick interaction
        self._touchscreen_enabled = False  # Enable/Accept Touch interaction
        self._mouse_enabled = True  # Enable/Accept Mouse interaction

        # State, interactivity and Visibility
        self._state = "normal"  # Use set_state() to modify this status
        self._disabled = False  # Use enable() or disable() to modify this status
        self._focused = False  # Use focus() or unfocus() to modify this status
        self._visible = True  # Use show() or hide() to modify this status

        self._dirty = True  # Set if widget need to be redrawn or not

        # Widget Attributes
        self._height = height
        self._width = width
        self._background: pygame.Color = background
        self._foreground: pygame.Color = foreground

        # Widget Border Attributes
        self._border_color = (0, 0, 0)
        self._border_inflate = (0, 0)
        self._border_position = "none"
        self._border_width = (0, 0, 0, 0)  # left, right, top, bottom
        self._border_radius: int = kwargs.pop(
            "border_radius", 0
        )  # left, right, top, bottom

        # Widget Shadow Attributes
        self._shadow_enable: bool = kwargs.pop("shadow", False)
        self._shadow_width = 0
        self._shadowoffset: tuple[int, int] = kwargs.pop("shadowoffset", (5, 5))
        if self._shadow_enable:
            self._shadowcolor: pygame.Color = kwargs.pop("shadowcolor", (0, 0, 0))
            if isinstance(self._shadowcolor, str):
                self._shadowcolor = pygame.Color(self._shadowcolor)

        # Initialize geometry managers
        Place.__init__(self)
        Grid.__init__(self)
        Pack.__init__(self)

    # def draw(
    #     self, surface: Optional["pygame.Surface"] = None, clear_surface: bool = False
    # ) -> "Menu":
    #     """
    #     Draw the **current** Menu into the given surface.

    #     .. warning::

    #         This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
    #         for example, ``menu.get_current().draw(...)``

    #     :param surface: Pygame surface to draw the Menu. If None, the Menu will use the provided ``surface`` from the constructor
    #     :param clear_surface: Clear surface using theme ``surface_clear_color``
    #     :return: Self reference **(current)**
    #     """
    #     if surface is None:
    #         surface = self._surface
    #     assert isinstance(surface, pygame.Surface)
    #     assert isinstance(clear_surface, bool)

    #     # Update last surface
    #     self._surface_last = surface

    #     if not self.is_enabled():
    #         self._current._runtime_errors.throw(
    #             self._current._runtime_errors.draw, "menu is not enabled"
    #         )
    #         return self._current
    #     elif self._current._disable_draw:
    #         return self._current

    #     # Render menu; if True, the surface widget has changed, thus cache should
    #     # change if enabled
    #     render = self._current._render()

    #     # Updates title
    #     if (
    #         self._current._theme.title_updates_pygame_display
    #         and pygame.display.get_caption()[0] != self._current.get_title()
    #     ):
    #         pygame.display.set_caption(self._current.get_title())

    #     # Clear surface
    #     if clear_surface:
    #         surface.fill(self._current._theme.surface_clear_color)

    #     # Call background function (set from mainloop)
    #     if self._top._background_function[1] is not None:
    #         if self._top._background_function[0]:
    #             self._top._background_function[1](self._current)
    #         else:
    #             self._top._background_function[1]()

    #     # Draw the prev decorator
    #     self._current._decorator.draw_prev(surface)

    #     # Draw widgets, update cache if enabled
    #     if (
    #         not self._current._widget_surface_cache_enabled
    #         or render
    #         or self._current._widget_surface_cache_need_update
    #     ):
    #         # This should be updated before drawing widgets. As widget
    #         # draw may trigger surface cache updating. Don't move this
    #         # line or unexpected errors may occur
    #         self._current._widget_surface_cache_need_update = False

    #         # Fill the scrolling surface (clear previous state)
    #         self._current._widgets_surface.fill((255, 255, 255, 0))

    #         # Call scrollarea draw decorator. This must be done before filling the
    #         # surface. ScrollArea post decorator is drawn on _scroll.draw(surface) call
    #         scrollarea_decorator = self._current._scrollarea.get_decorator()
    #         scrollarea_decorator.force_cache_update()
    #         scrollarea_decorator.draw_prev(self._current._widgets_surface)

    #         # Iterate through widgets and draw them
    #         selected_widget_draw: Tuple[
    #             Optional["_Widget"], Optional["pygame.Surface"]
    #         ] = (None, None)

    #         for widget in self._current._widgets:
    #             # Widgets within frames are not drawn as it's frame draw these widgets
    #             if widget.get_frame() is not None:
    #                 continue
    #             elif widget.is_selected():
    #                 selected_widget_draw = widget, self._current._widgets_surface
    #             widget.draw(self._current._widgets_surface)

    #         if selected_widget_draw[0] is not None:
    #             selected_widget_draw[0].draw_after_if_selected(selected_widget_draw[1])

    #         self._current._stats.draw_update_cached += 1

    #     self._current._scrollarea.draw(surface)
    #     self._current._menubar.draw(surface)

    #     # Draw focus on selected if the widget is active
    #     self._current._draw_focus_widget(surface, self._current.get_selected_widget())
    #     self._current._decorator.draw_post(surface)
    #     self._current._stats.draw += 1

    #     # Update cursor if not mainloop
    #     if self._current._mainloop:
    #         check_widget_mouseleave()

    #     return self._current

    # def mainloop(
    #     self,
    #     surface: Optional["pygame.Surface"] = None,
    #     bgfun: Optional[Union[Callable[["Menu"], Any], CallableNoArgsType]] = None,
    #     **kwargs,
    # ) -> "Menu":
    #     """
    #     Main loop of the **current** Menu. In this function, the Menu handle
    #     exceptions and draw. The Menu pauses the application and checks :py:mod:`pygame`
    #     events itself.

    #     This method returns until the Menu is updated (a widget status has changed).

    #     The execution of the mainloop is at the current Menu level.

    #     .. code-block:: python

    #         menu = pygame_menu.Menu(...)
    #         menu.mainloop(surface)

    #     The ``bgfun`` callable (if not None) can receive 1 argument maximum, if so,
    #     the Menu instance is provided:

    #     .. code-block:: python

    #         draw(...):
    #             bgfun(menu) <or> bgfun()

    #     Finally, mainloop can be disabled externally if menu.disable() is called.

    #     kwargs (Optional)
    #         - ``clear_surface``     (bool) – If ``True`` surface is cleared using ``theme.surface_clear_color``. Default equals to ``True``
    #         - ``disable_loop``      (bool) – If ``True`` the mainloop only runs once. Use for running draw and update in a single call
    #         - ``fps_limit``         (int) – Maximum FPS of the loop. Default equals to ``theme.fps``. If ``0`` there's no limit
    #         - ``wait_for_event``    (bool) – Holds the loop until an event is provided, useful to save CPU power

    #     .. warning::

    #         This method should not be used along :py:meth:`pygame_menu.menu.Menu.get_current`,
    #         for example, ``menu.get_current().mainloop(...)``.

    #     :param surface: Pygame surface to draw the Menu. If None, the Menu will use the provided ``surface`` from the constructor
    #     :param bgfun: Background function called on each loop iteration before drawing the Menu
    #     :param kwargs: Optional keyword arguments
    #     :return: Self reference **(current)**
    #     """
    #     # Unpack kwargs
    #     clear_surface = kwargs.get("clear_surface", True)
    #     disable_loop = kwargs.get("disable_loop", False)
    #     fps_limit = kwargs.get("fps_limit", self._theme.fps)
    #     wait_for_event = kwargs.get("wait_for_event", False)

    #     if surface is None:
    #         surface = self._surface

    #     assert isinstance(clear_surface, bool)
    #     assert isinstance(disable_loop, bool)
    #     assert isinstance(fps_limit, NumberInstance)
    #     assert isinstance(surface, pygame.Surface)
    #     assert isinstance(wait_for_event, bool)

    #     assert fps_limit >= 0, "fps limit cannot be negative"

    #     # NOTE: For Menu accessor, use only _current, as the Menu pointer can
    #     # change through the execution
    #     if not self.is_enabled():
    #         self._current._runtime_errors.throw(
    #             self._current._runtime_errors.mainloop, "menu is not enabled"
    #         )
    #         return self._current

    #     # Check background function
    #     bgfun_accept_menu = False
    #     if bgfun:
    #         assert callable(
    #             bgfun
    #         ), "background function must be callable (function-type) object"
    #         try:
    #             bgfun(self._current)
    #             bgfun_accept_menu = True
    #         except TypeError:
    #             pass
    #     self._current._background_function = (bgfun_accept_menu, bgfun)

    #     # Change state
    #     self._current._mainloop = True

    #     # Force rendering before loop
    #     self._current._widgets_surface = None

    #     # Start loop
    #     while True:
    #         self._current._stats.loop += 1
    #         self._current._clock.tick(fps_limit)

    #         # Draw the menu
    #         self.draw(surface=surface, clear_surface=clear_surface)

    #         # Gather events by Menu
    #         if wait_for_event:
    #             self.update([pygame.event.wait()])
    #         if (not wait_for_event or pygame.event.peek()) and self.is_enabled():
    #             self.update(pygame.event.get())

    #         # Flip contents to screen
    #         pygame.display.flip()

    #         # Menu closed or disabled
    #         if not self.is_enabled() or disable_loop:
    #             self._current._mainloop = False
    #             check_widget_mouseleave(force=True)
    #             return self._current

    # def mouseleave(
    #     self, event: EventType, check_all_widget_mouseleave: bool = True
    # ) -> "_Widget":
    #     """
    #     Run the ``onmouseleave`` callback if the mouse is placed outside the _Widget.
    #     The callback receive the _Widget object reference and the mouse event:

    #     .. code-block:: python

    #         onmouseleave(widget, event) <or> onmouseleave()

    #     .. warning::

    #         This method does not evaluate if the mouse is placed over the _Widget.
    #         Only executes the callback and updates the cursor if enabled.

    #     :param event: ``MOUSEMOVE`` pygame event
    #     :param check_all_widget_mouseleave: Check widget leave statutes
    #     :return: Self reference
    #     """

    def __getitem__(self, config: str) -> Any:
        """Get an item from the widget's configuration."""
        return self.configure(config=config)

    def __setitem__(self, key: str, value: Any) -> None:
        """Set an item in the widget's configuration."""
        self.configure(config=None, **{key: value})

    def __copy__(self) -> "_Widget":
        """
        Copy method.

        :return: Raises copy exception
        """
        raise PygameuiError("_Widget class cannot be copied")

    def __deepcopy__(self, memodict: dict) -> "_Widget":
        """
        Deep-copy method.

        :param memodict: Memo dict
        :return: Raises copy exception
        """
        raise PygameuiError("_Widget class cannot be deep-copied")

    def __str__(self):
        """Return a string representation of the widget."""
        return f"<{self.__class__.__name__} widget at {self._rect.topleft} of size {self._rect.size}>"

    def __repr__(self):
        """Return a string representation of the widget."""
        return f"{self.__class__.__name__}()"

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
    def angle(self) -> int:
        """Get or Set the angle of the widget."""
        return self._angle

    @angle.setter
    def angle(self, value: int):
        if value < 0:
            raise ValueError(f"Invalid Angle {value}")
        self._angle = value

    @property
    def keyboard(self) -> bool:
        """Get or Set Keyboard Interaction of widget."""
        return self._keyboard_enabled

    @keyboard.setter
    def keyboard(self, value: bool):
        self._keyboard_enabled = value

    @property
    def mouse(self) -> bool:
        """Get or Set Mouse Interaction of widget."""
        return self._mouse_enabled

    @mouse.setter
    def mouse(self, value: bool):
        self._mouse_enabled = value

    @property
    def joystick(self) -> bool:
        """Get or Set Joystick Interaction of widget."""
        return self._joystick_enabled

    @joystick.setter
    def joystick(self, value: bool):
        self._joystick_enabled = value

    @property
    def touchscreen(self) -> bool:
        """Get or Set Touchscreen Interaction of widget."""
        return self._touchscreen_enabled

    @touchscreen.setter
    def touchscreen(self, value: bool):
        self._touchscreen_enabled = value

    @property
    def dirty(self) -> bool:
        """Get or Set if widget need to be redrawn."""
        return self._dirty

    @dirty.setter
    def dirty(self, value: bool):
        self._dirty = value

    @property
    def focused(self) -> bool:
        """Get or Set the widget is focused."""
        return self._focused

    @focused.setter
    def focused(self, value: bool):
        self._focused = value

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

    # endregion Properties

    # region Public

    def draw(self, *args, surface: Surface = None, **kwargs) -> None:
        """
        Draw the widget on the given surface.

        Args:
            surface (pygame.Surface, optional): The surface to draw on.
        """
        if self._visible and self.__class__.__name__ == "_Widget":
            if self._master is not None:
                surface = self._master
            pygame.draw.rect(
                surface, self._background, self._rect.inflate(-20, -20), border_radius=1
            )
        else:
            if self._master is not None:
                surface = self._master
            self._perform_draw_(surface, *args, **kwargs)

    def handle(self, event: Event, *args, **kwargs) -> None:
        """
        Handle an event for the widget.

        Args:
            event (pygame.Event): The event to handle.
        """
        self._handle_event_(event, *args, **kwargs)

    def update(self, *args, delta: float = 0.0, **kwargs) -> None:
        """
        Update the widget's logic.

        Args:
            delta (float): Time since last update.
        """
        if self._visible:
            self._perform_update_(delta, *args, **kwargs)

    def hide(self) -> None:
        """Hide the widget (set visibility to False)."""
        self._set_visible_(False)

    def show(self) -> None:
        """Show the widget (set visibility to True)."""
        self._set_visible_(True)

    def enable(self) -> None:
        """Enable the widget (set disabled to False)."""
        self.show()
        self._disabled = False
        self.state = "normal"

    def disable(self) -> None:
        """Disable the widget (set disabled to True)."""
        self.state = "disabled"
        self._disabled = True

    def focus(self) -> None:
        """Focus the widget (set it to be Focused)."""
        self._focused = False

    def unfocus(self) -> None:
        """Unfocus the widget (set it not to be Focused)."""
        self._focused = True

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

    # endregion

    # region Private

    def _configure_set_(self, **kwargs) -> None:
        """
        Set widget configuration options.

        Args:
            **kwargs: Configuration options to set.
        """
        self._height = kwargs.pop("height", self._height)
        self._width = kwargs.pop("width", self._width)
        self._background = kwargs.pop("background", self._background)
        self._foreground = kwargs.pop("foreground", self._foreground)
        self._cursor = kwargs.pop("cursor", self._cursor)

    def _configure_get_(self, attribute: str) -> Any:
        """
        Get a widget configuration value.

        Args:
            attribute (str): The attribute name.

        Returns:
            Any: The value of the attribute.
        """
        if attribute == "height":
            return self._height
        if attribute == "width":
            return self._width
        if attribute == "background":
            return self._background
        if attribute == "foreground":
            return self._foreground
        if attribute == "cursor":
            return self._cursor
        return None

    def _set_visible_(self, value) -> None:
        """Set the widget's visibility (True or False)."""
        self._visible = value

    def _get_visible_(self) -> bool:
        """Return the widget's visibility."""
        return self._visible

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
    def _handle_mouse_event_(self, event: Event, *args, **kwargs) -> None:
        """
        Handle Mouse events for the widget.

        Args:
            event (pygame.Event): The event to handle.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def _handle_keyboard_event_(self, event: Event, *args, **kwargs) -> None:
        """
        Handle Keyboard events for the widget.

        Args:
            event (pygame.Event): The event to handle.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def _handle_joystick_event_(self, event: Event, *args, **kwargs) -> None:
        """
        Handle Joystick events for the widget.

        Args:
            event (pygame.Event): The event to handle.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def _handle_touchscreen_event_(self, event: Event, *args, **kwargs) -> None:
        """
        Handle Touch Screen events for the widget.

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

    # @staticmethod
    # def _get(
    #     params: Dict[str, Any],
    #     key: str,
    #     allowed_types: Optional[Union[Type, str, List[Type], Tuple[Type, ...]]] = None,
    #     default: Any = None,
    # ) -> Any:
    #     """
    #     Return a value from a dictionary.

    #     Custom types (str)
    #         -   alignment           – pygame-menu alignment (locals)
    #         -   callable            – Is callable type, same as ``"function"``
    #         -   color               – Check color
    #         -   color_image         – Color or :py:class:`pygame_menu.baseimage.BaseImage`
    #         -   color_image_none    – Color, :py:class:`pygame_menu.baseimage.BaseImage`, or None
    #         -   color_none          – Color or None
    #         -   cursor              – Cursor object (pygame)
    #         -   font                – Font type
    #         -   image               – Value must be ``BaseImage``
    #         -   none                – None only
    #         -   position            – pygame-menu position (locals)
    #         -   position_vector     – pygame-menu position (str or vector)
    #         -   tuple2              – Only valid numeric tuples ``(x, y)`` or ``[x, y]``
    #         -   tuple2int           – Only valid integer tuples ``(x, y)`` or ``[x, y]``
    #         -   tuple3              – Only valid numeric tuples ``(x, y, z)`` or ``[x, y, z]``
    #         -   tuple3int           – Only valid integer tuples ``(x, y, z)`` or ``[x, y, z]``
    #         -   type                – Type-class (bool, str, etc...)

    #     :param params: Parameters dictionary
    #     :param key: Key to look for
    #     :param allowed_types: List of allowed types
    #     :param default: Default value to return
    #     :return: The value associated to the key
    #     """
    #     value = params.pop(key, default)
    #     if allowed_types is not None:
    #         other_types = []  # Contain other types to check from
    #         if not isinstance(allowed_types, VectorInstance):
    #             allowed_types = (allowed_types,)
    #         for val_type in allowed_types:

    #             if val_type == "alignment":
    #                 assert_alignment(value)

    #             elif (
    #                 val_type == callable
    #                 or val_type == "function"
    #                 or val_type == "callable"
    #             ):
    #                 assert callable(value), "value must be callable type"

    #             elif val_type == "color":
    #                 value = assert_color(value)

    #             elif val_type == "color_image":
    #                 if not isinstance(value, BaseImage):
    #                     value = assert_color(value)

    #             elif val_type == "color_image_none":
    #                 if not (value is None or isinstance(value, BaseImage)):
    #                     value = assert_color(value)

    #             elif val_type == "color_none":
    #                 if value is not None:
    #                     value = assert_color(value)

    #             elif val_type == "cursor":
    #                 assert_cursor(value)

    #             elif val_type == "font":
    #                 assert_font(value)

    #             elif val_type == "image":
    #                 assert isinstance(value, BaseImage), "value must be BaseImage type"

    #             elif val_type == "none":
    #                 assert value is None

    #             elif val_type == "position":
    #                 assert_position(value)

    #             elif val_type == "position_vector":
    #                 assert_position_vector(value)

    #             elif val_type == "type":
    #                 assert isinstance(value, type), "value is not type-class"

    #             elif val_type == "tuple2":
    #                 assert_vector(value, 2)

    #             elif val_type == "tuple2int":
    #                 assert_vector(value, 2, int)

    #             elif val_type == "tuple3":
    #                 assert_vector(value, 3)

    #             elif val_type == "tuple3int":
    #                 assert_vector(value, 3, int)

    #             else:  # Unknown type
    #                 assert isinstance(
    #                     val_type, type
    #                 ), f'allowed type "{val_type}" is not a type-class'
    #                 other_types.append(val_type)

    #         # Check other types
    #         if len(other_types) > 0:
    #             others = tuple(other_types)
    #             assert isinstance(
    #                 value, others
    #             ), f"Theme.{key} type shall be in {others} types (got {type(value)})"

    #     return value

    # def rotate(self, angle: int, auto_checkpoint: bool = True) -> None:
    #     """
    #     Unfiltered counterclockwise rotation. The angle argument represents degrees
    #     and can be any floating point value. Negative angle amounts will rotate
    #     clockwise.

    #     .. note::

    #         Unless rotating by 90 degree increments, the image will be padded
    #         larger to hold the new size. If the image has pixel alphas, the padded
    #         area will be transparent. Otherwise, pygame will pick a color that matches
    #         the image color-key or the topleft pixel value.

    #     .. warning::

    #         Image should be rotated once. If this method is called once the Class
    #         rotates the previously check-pointed state. If you wish to rotate the
    #         current image use ``checkpoint`` to update the surface. This may
    #         increase the image size, because the bounding rectangle of a rotated
    #         image is always greater than the bounding rectangle of the original
    #         image (except some rotations by multiples of 90 degrees). The image
    #         gets distort because of the multiply copies. Each rotation generates
    #         a small error (inaccuracy). The sum of the errors is growing and the
    #         images decays.

    #     :param angle: Rotation angle (degrees ``0-360``)
    #     :param auto_checkpoint: Checkpoint after first rotation to avoid rotating the same image. If multiple rotations are applied to the same surface it will increase its size very fast because of inaccuracies
    #     :return: Self reference
    #     """
    #     assert isinstance(angle, int)
    #     if angle == self._angle:
    #         return self
    #     elif not self._rotated and auto_checkpoint:
    #         self.checkpoint()
    #     if self._rotated:
    #         self.restore()
    #     self._rotated = True
    #     self._surface = pygame.transform.rotate(self._surface, angle)
    #     self._angle = angle % 360
    #     return self

    def get_angle(self) -> int:
        """
        Return the image angle.

        :return: Angle in degrees
        """
        return self._angle

    # endregion
