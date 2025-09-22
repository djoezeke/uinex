"""PygameUI Scale Widget

A Scale is a slider widget that allows the user to select a numeric value by dragging a handle
along a track. It supports horizontal and vertical orientation, value bounds, step size, and callbacks
for value changes.

Features:
    - Horizontal or vertical orientation
    - Customizable min, max, and step
    - Customizable colors and handle size
    - Mouse interaction (drag to change value)
    - Callback for value change
    - Optional value display

Example:
    scale = Scale(master, from_=0, to=100, value=50, orientation="horizontal")
    scale.on_change = lambda v: print("Scale value:", v)

Author: Your Name & PygameUI Contributors
License: MIT
"""

import pygame

from uinex.core.widget import Widget
from uinex.core.themes import ThemeManager

__all__ = ["Scale"]


class Scale(Widget):
    """
    A slider widget for selecting a numeric value.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        from_ (int or float): Minimum value of the scale.
        to (int or float): Maximum value of the scale.
        value (int or float, optional): Initial value.
        step (int or float, optional): Step size for value changes.
        orientation (str, optional): "horizontal" or "vertical". Default is "horizontal".
        width (int, optional): Width of the scale.
        height (int, optional): Height of the scale.
        track_color (pygame.Color or tuple, optional): Color of the track.
        handle_color (pygame.Color or tuple, optional): Color of the handle.
        handle_radius (int, optional): Radius of the handle.
        show_value (bool, optional): Whether to display the value.
        font (pygame.font.Font, optional): Font for value display.
        on_change (callable, optional): Callback when value changes.
        **kwargs: Additional widget options.

    Attributes:
        value (int or float): The current value.
        from_ (int or float): Minimum value.
        to (int or float): Maximum value.
        step (int or float): Step size.
        orientation (str): "horizontal" or "vertical".
        on_change (callable): Callback for value change.
    """

    def __init__(
        self,
        master,
        from_=0,
        to=100,
        value=None,
        step=1,
        orientation="horizontal",
        width=200,
        height=32,
        track_color=(180, 180, 180),
        handle_color=(30, 144, 255),
        handle_radius=10,
        show_value=True,
        font=None,
        on_change=None,
        **kwargs,
    ):
        self.from_ = from_
        self.to = to
        self.step = step
        self.orientation = orientation
        self.value = value if value is not None else from_
        self.track_color = track_color
        self.handle_color = handle_color
        self.handle_radius = handle_radius
        self.show_value = show_value
        self.font = font or pygame.font.SysFont(None, 18)
        self.on_change = on_change

        self._dragging = False

        if orientation == "horizontal":
            w, h = width, height
        else:
            w, h = height, width

        super().__init__(
            master,
            width=w,
            height=h,
            background=(0, 0, 0, 0),
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the scale track, handle, and value."""
        rect = surface.get_rect()
        # Draw track
        if self.orientation == "horizontal":
            track_y = rect.centery
            pygame.draw.line(
                surface,
                self.track_color,
                (self.handle_radius, track_y),
                (rect.width - self.handle_radius, track_y),
                4,
            )
            # Draw handle
            handle_x = self._value_to_pos(self.value)
            pygame.draw.circle(
                surface,
                self.handle_color,
                (int(handle_x), track_y),
                self.handle_radius,
            )
            # Draw value
            if self.show_value:
                value_surf = self.font.render(str(self.value), True, (0, 0, 0))
                surface.blit(
                    value_surf,
                    (
                        handle_x - value_surf.get_width() // 2,
                        track_y - self.handle_radius - value_surf.get_height() - 2,
                    ),
                )
        else:
            track_x = rect.centerx
            pygame.draw.line(
                surface,
                self.track_color,
                (track_x, self.handle_radius),
                (track_x, rect.height - self.handle_radius),
                4,
            )
            handle_y = self._value_to_pos(self.value)
            pygame.draw.circle(
                surface,
                self.handle_color,
                (track_x, int(handle_y)),
                self.handle_radius,
            )
            if self.show_value:
                value_surf = self.font.render(str(self.value), True, (0, 0, 0))
                surface.blit(
                    value_surf,
                    (
                        track_x + self.handle_radius + 4,
                        handle_y - value_surf.get_height() // 2,
                    ),
                )

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse events for dragging the handle."""
        rect = self._rect
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = (event.pos[0] - rect.x, event.pos[1] - rect.y)
            if self._handle_hit_test(mouse):
                self._dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._dragging = False
        elif event.type == pygame.MOUSEMOTION and self._dragging:
            mouse = (event.pos[0] - rect.x, event.pos[1] - rect.y)
            new_value = self._pos_to_value(mouse)
            self.set_value(new_value)

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for Scale (not used)."""
        pass

    def _value_to_pos(self, value):
        """Convert value to pixel position along the track."""
        vmin, vmax = self.from_, self.to
        if self.orientation == "horizontal":
            px_min = self.handle_radius
            px_max = self._rect.width - self.handle_radius
            pos = px_min + (float(value) - vmin) / (vmax - vmin) * (px_max - px_min)
            return pos
        else:
            px_min = self.handle_radius
            px_max = self._rect.height - self.handle_radius
            pos = px_max - (float(value) - vmin) / (vmax - vmin) * (px_max - px_min)
            return pos

    def _pos_to_value(self, pos):
        """Convert mouse position to value."""
        vmin, vmax = self.from_, self.to
        if self.orientation == "horizontal":
            px_min = self.handle_radius
            px_max = self._rect.width - self.handle_radius
            x = min(max(pos[0], px_min), px_max)
            ratio = (x - px_min) / (px_max - px_min)
            value = vmin + ratio * (vmax - vmin)
        else:
            px_min = self.handle_radius
            px_max = self._rect.height - self.handle_radius
            y = min(max(pos[1], px_min), px_max)
            ratio = (px_max - y) / (px_max - px_min)
            value = vmin + ratio * (vmax - vmin)
        # Snap to step
        value = round((value - vmin) / self.step) * self.step + vmin
        value = min(max(value, vmin), vmax)
        if isinstance(self.from_, int) and isinstance(self.to, int) and isinstance(self.step, int):
            value = int(value)
        return value

    def _handle_hit_test(self, mouse):
        """Check if mouse is over the handle."""
        if self.orientation == "horizontal":
            handle_x = self._value_to_pos(self.value)
            handle_y = self._rect.height // 2
            dx = mouse[0] - handle_x
            dy = mouse[1] - handle_y
        else:
            handle_x = self._rect.width // 2
            handle_y = self._value_to_pos(self.value)
            dx = mouse[0] - handle_x
            dy = mouse[1] - handle_y
        return dx * dx + dy * dy <= self.handle_radius * self.handle_radius

    def set_value(self, value):
        """Set the scale's value and trigger callback if changed."""
        value = min(max(value, self.from_), self.to)
        if value != self.value:
            self.value = value
            if self.on_change:
                self.on_change(self.value)
            self._dirty = True

    def get_value(self):
        """Return the current value of the scale."""
        return self.value

    def set_range(self, from_, to):
        """Set the minimum and maximum values of the scale."""
        self.from_ = from_
        self.to = to
        self.value = min(max(self.value, self.from_), self.to)
        self._dirty = True

    def set_step(self, step):
        """Set the step size for the scale."""
        self.step = step

    def set_orientation(self, orientation):
        """Set the orientation of the scale."""
        if orientation not in ("horizontal", "vertical"):
            raise ValueError("Orientation must be 'horizontal' or 'vertical'")
        self.orientation = orientation
        self._dirty = True

    def reset(self):
        """Reset the scale to its minimum value."""
        self.set_value(self.from_)

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
            if config == "value":
                return self.value
            if config == "from_":
                return self.from_
            if config == "to":
                return self.to
            if config == "step":
                return self.step
            if config == "orientation":
                return self.orientation
            return super().configure(config)
        if "value" in kwargs:
            self.set_value(kwargs["value"])
        if "from_" in kwargs:
            self.from_ = kwargs["from_"]
        if "to" in kwargs:
            self.to = kwargs["to"]
        if "step" in kwargs:
            self.step = kwargs["step"]
        if "orientation" in kwargs:
            self.orientation = kwargs["orientation"]
