"""Manager"""

from collections import defaultdict
from collections.abc import Iterable

from pygame import Surface
from uinex.widget.base import Widget


class BaseManager:
    _enabled = False

    DEFAULT_LAYER = 0
    OVERLAY_LAYER = 10

    def __init__(self):
        self._surfaces: dict[int, Surface] = {}
        self.children: dict[int, list[Widget]] = defaultdict(list)

    # region Registration

    def register(self, widget: type[Widget], *, layer=DEFAULT_LAYER) -> None:
        """
        Register a widget to the :class:`WidgetManager`.

        The WidgetManager supports layered setups, widgets added to a
        higher layer are drawn above lower layers and receive events first.
        The layer 10 is reserved for overlaying components like tooltips.

        Raises:
            AlreadyRegistered: If the widget is already registered.

        Args:
            widget: widget to register
            layer: layer which the widget should be added to.
        """

        if self.is_registered(widget):
            pass
        widget.parent = self
        self.children[layer].append(widget)

    def unregister(self, widget: Widget) -> None:
        """
        Unregister a widget from the :class:`WidgetManager`.

        Raises:
            NotRegistered: If the widget is not registered.

        Args:
            widget: widget to unregester.
        """
        if not self.is_registered(widget):
            pass

        for children in self.children.values():
            if widget in children:
                children.remove(widget)
                widget.parent = None

    def is_registered(self, widget) -> bool:
        """Return True if an widget is registered."""

        for children in self.children.values():
            if widget in children:
                return True
        return False

    def walk_widgets(self, *, root: Widget | None = None, layer=DEFAULT_LAYER) -> Iterable[Widget]:
        """Walks through widget tree, in reverse draw order (most top drawn widget first)

        Args:
            root: root widget to start from, if None, the layer is used
            layer: layer to search, None will search through all layers
        """

        if layer is None:
            layers = sorted(self.children.keys(), reverse=True)
        else:
            layers = [layer]

        for layer in layers:
            children = root.children if root else self.children[layer]
            for child in reversed(children):
                yield from self.walk_widgets(root=child)
                yield child

    def clear(self) -> None:
        """Remove all registered widget from the :class:`WidgetManager`."""

        for layer in self.children.values():
            for widget in layer[:]:
                self.unregister(widget)

    # endregion


class WidgetManager(BaseManager): ...
