"""Uinex Event System

Provides a clean, non-intrusive event handling layer for Uinex widgets so that
UI events do not accidentally interfere with the host project's own event loop.

Key design goals
----------------
1. **Transparent** – the host game calls ``UIEventDispatcher.process(events)``
   which returns only the events that were **not consumed** by any widget.
2. **No side-effects** – widgets never pop events from pygame's global queue.
   They receive a pre-filtered list and report back whether they consumed it.
3. **Simple integration** – a project only needs to replace::

       for event in pygame.event.get():
           widget.handle(event)

   with::

       from uinex.core.events import UIEventDispatcher
       dispatcher = UIEventDispatcher()
       dispatcher.register(widget)

       events = pygame.event.get()
       unconsumed = dispatcher.process(events)
       for event in unconsumed:
           # game handles its own events here

Usage example
-------------
::

    dispatcher = UIEventDispatcher()
    dispatcher.register(button)
    dispatcher.register(label)

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000
        events = pygame.event.get()
        unconsumed = dispatcher.process(events, dt=dt)
        for event in unconsumed:
            if event.type == pygame.QUIT:
                running = False

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & Uinex Contributors
License: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from uinex.widget.base import Widget

__all__ = ["UIEventDispatcher"]


class UIEventDispatcher:
    """Central event dispatcher for Uinex widgets.

    Distributes a list of pygame events to registered widgets and returns the
    subset that was **not consumed** by any widget, so the host application can
    handle its own events without interference.

    A widget is considered to have *consumed* an event when its ``handle``
    method returns a truthy value.  If a widget does not return a value (or
    returns ``None``) the event is treated as *not consumed* and is passed to
    remaining widgets as well as returned to the caller.

    Attributes:
        _widgets (list[Widget]): Ordered list of registered widgets.
            Widgets registered later receive events last (lower priority).
    """

    def __init__(self):
        self._widgets: list[Widget] = []

    # ─────────────────────────────────────────────────
    # Registration
    # ─────────────────────────────────────────────────

    def register(self, widget: Widget) -> None:
        """Register a widget with this dispatcher.

        Args:
            widget: The widget to register.
        """
        if widget not in self._widgets:
            self._widgets.append(widget)

    def unregister(self, widget: Widget) -> None:
        """Unregister a widget from this dispatcher.

        Args:
            widget: The widget to remove.
        """
        try:
            self._widgets.remove(widget)
        except ValueError:
            pass

    def clear(self) -> None:
        """Remove all registered widgets."""
        self._widgets.clear()

    # ─────────────────────────────────────────────────
    # Event processing
    # ─────────────────────────────────────────────────

    def process(
        self,
        events: Sequence[pygame.event.Event],
        *,
        dt: float = 0.0,
        draw_surface: pygame.Surface | None = None,
    ) -> list[pygame.event.Event]:
        """Process a list of pygame events through all registered widgets.

        For each event, every registered widget gets a chance to handle it.
        Widgets that return a truthy value from ``handle()`` are considered to
        have consumed the event; the event is then **not** included in the
        returned list.

        After event processing, each widget's ``update()`` is called with the
        given *dt*.  If *draw_surface* is provided, ``draw()`` is called too.

        Args:
            events: Sequence of ``pygame.event.Event`` objects, typically the
                result of ``pygame.event.get()``.
            dt: Time elapsed since last frame (seconds).
            draw_surface: If provided, widgets are drawn to this surface after
                updating.

        Returns:
            A list of events that were **not consumed** by any widget.  Pass
            these to your game's own event handling code.
        """
        unconsumed: list[pygame.event.Event] = []

        for event in events:
            consumed = False
            for widget in self._widgets:
                result = widget.handle(event)
                if result:
                    consumed = True
                    break  # stop propagating this event once consumed
            if not consumed:
                unconsumed.append(event)

        # Update (and optionally draw) all widgets
        for widget in self._widgets:
            widget.update(delta=dt)
            if draw_surface is not None:
                widget.draw(surface=draw_surface)

        return unconsumed

    def update_all(self, dt: float = 0.0) -> None:
        """Call ``update()`` on every registered widget.

        Args:
            dt: Time elapsed since last frame (seconds).
        """
        for widget in self._widgets:
            widget.update(delta=dt)

    def draw_all(self, surface: pygame.Surface) -> None:
        """Call ``draw()`` on every registered widget.

        Args:
            surface: The surface to draw on.
        """
        for widget in self._widgets:
            widget.draw(surface=surface)

    # ─────────────────────────────────────────────────
    # Dunder helpers
    # ─────────────────────────────────────────────────

    def __len__(self) -> int:
        return len(self._widgets)

    def __contains__(self, widget: Widget) -> bool:
        return widget in self._widgets

    def __repr__(self) -> str:
        return f"UIEventDispatcher(widgets={len(self._widgets)})"
