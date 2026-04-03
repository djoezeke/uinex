"""Uinex Widget Manager

Provides ``WidgetManager``, the main entry point for managing a collection of
widgets in a Uinex-powered project.

The manager handles:
- Widget registration / unregistration
- Layered drawing order (higher layer → drawn on top, receives events first)
- Event processing that returns *unconsumed* events to the host application
- Convenient ``update_all`` / ``draw_all`` helpers

Typical usage::

    import pygame
    from uinex import Button, Label, WidgetManager

    manager = WidgetManager()
    manager.register(label)
    manager.register(button)

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000
        events = pygame.event.get()

        # Pass only un-consumed events to game logic
        unconsumed = manager.process_events(events, dt=dt)
        for event in unconsumed:
            if event.type == pygame.QUIT:
                running = False

        screen.fill((10, 10, 20))
        manager.draw_all(screen)
        pygame.display.flip()

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & Uinex Contributors
License: MIT
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from pygame import Surface

    from uinex.widget.base import Widget

__all__ = ["WidgetManager"]


class BaseManager:
    """Internal base class for layered widget management."""

    _enabled = False

    DEFAULT_LAYER = 0
    OVERLAY_LAYER = 10

    def __init__(self):
        self._surfaces: dict[int, Surface] = {}
        self.children: dict[int, list[Widget]] = defaultdict(list)

    # ─────────────────────────────────────────────────
    # Registration
    # ─────────────────────────────────────────────────

    def register(self, widget: Widget, *, layer: int = DEFAULT_LAYER) -> None:
        """Register a widget with the manager.

        Widgets on a higher layer are drawn above (and receive events before)
        those on a lower layer.  Layer 10 is reserved for overlay components
        such as tooltips or dialogs.

        Args:
            widget: The widget to register.
            layer: Layer index (default 0).
        """
        if not self.is_registered(widget):
            widget.parent = self
            self.children[layer].append(widget)

    def unregister(self, widget: Widget) -> None:
        """Unregister a widget from the manager.

        Args:
            widget: The widget to remove.
        """
        for layer_widgets in self.children.values():
            if widget in layer_widgets:
                layer_widgets.remove(widget)
                widget.parent = None
                return

    def is_registered(self, widget: Widget) -> bool:
        """Return ``True`` if *widget* is already registered."""
        return any(widget in layer_widgets for layer_widgets in self.children.values())

    def walk_widgets(
        self,
        *,
        root: Widget | None = None,
        layer: int | None = DEFAULT_LAYER,
    ) -> Iterable[Widget]:
        """Walk the widget tree in reverse draw order (top-most widget first).

        Args:
            root: Starting widget (walks its children).  When *None* the
                *layer* parameter selects the layer to walk.
            layer: Layer to search.  Pass ``None`` to walk all layers.
        """
        if layer is None:
            layers = sorted(self.children.keys(), reverse=True)
        else:
            layers = [layer]

        for lyr in layers:
            children = root.children if root else self.children[lyr]
            for child in reversed(list(children)):
                yield from self.walk_widgets(root=child)
                yield child

    def clear(self) -> None:
        """Remove all registered widgets."""
        for layer_widgets in self.children.values():
            for widget in list(layer_widgets):
                self.unregister(widget)

    # ─────────────────────────────────────────────────
    # Event processing
    # ─────────────────────────────────────────────────

    def process_events(
        self,
        events: list[pygame.event.Event],
        *,
        dt: float = 0.0,
    ) -> list[pygame.event.Event]:
        """Distribute *events* to widgets and return un-consumed events.

        Events are dispatched to widgets from the highest layer downward.
        Within a layer, widgets are visited in reverse registration order
        (last-registered = on top).  A widget that returns a truthy value
        from :meth:`~uinex.widget.base.Widget.handle` is considered to have
        consumed the event; the event is then **excluded** from the returned
        list.

        After processing events, ``update()`` is called on every widget.

        Args:
            events: The event list from ``pygame.event.get()``.
            dt: Elapsed time since the last frame (seconds).

        Returns:
            Events **not** consumed by any widget.
        """
        unconsumed: list[pygame.event.Event] = []

        # Sorted layers: highest first so overlay widgets receive events first
        sorted_layers = sorted(self.children.keys(), reverse=True)

        for event in events:
            consumed = False
            for lyr in sorted_layers:
                for widget in reversed(self.children[lyr]):
                    if widget.handle(event):
                        consumed = True
                        break
                if consumed:
                    break
            if not consumed:
                unconsumed.append(event)

        # Update all widgets
        for lyr in sorted_layers:
            for widget in self.children[lyr]:
                widget.update(delta=dt)

        return unconsumed

    # ─────────────────────────────────────────────────
    # Drawing / updating helpers
    # ─────────────────────────────────────────────────

    def draw_all(self, surface: Surface) -> None:
        """Draw all registered widgets onto *surface*.

        Widgets on lower layers are drawn first (underneath higher layers).

        Args:
            surface: The ``pygame.Surface`` to draw on.
        """
        for lyr in sorted(self.children.keys()):
            for widget in self.children[lyr]:
                widget.draw(surface=surface)

    def update_all(self, dt: float = 0.0) -> None:
        """Call ``update()`` on every registered widget.

        Args:
            dt: Elapsed time since the last frame (seconds).
        """
        for layer_widgets in self.children.values():
            for widget in layer_widgets:
                widget.update(delta=dt)

    # ─────────────────────────────────────────────────
    # Dunder helpers
    # ─────────────────────────────────────────────────

    def __len__(self) -> int:
        return sum(len(w) for w in self.children.values())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(widgets={len(self)})"


class WidgetManager(BaseManager):
    """Public widget manager.  Use this class in your projects.

    See :class:`BaseManager` for full documentation.
    """
