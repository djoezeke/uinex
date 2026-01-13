"""Uinex TextBox Widget

A TextBox is a single-line or multi-line text input field for user text entry.
This widget supports keyboard input, cursor movement, selection, and basic editing.

Features:
    - Single-line or multi-line text input
    - Customizable font, colors, and padding
    - Cursor and selection support
    - Focus and blur handling
    - Optional input validation and max length
    - Callback for text change

Example:
    tb = TextBox(master, width=200, text="Hello", multiline=False)
    tb.on_change = lambda text: print("Text changed:", text)

Author: Sackey Ezekiel Etrue & Uinex Contributors
License: MIT
"""

import pygame

from uinex.widget.base import Widget


class TextBox(Widget):
    """
    A text input widget for single-line or multi-line text entry.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        width (int): Width of the textbox.
        height (int): Height of the textbox.
        text (str, optional): Initial text.
        font (pygame.font.Font, optional): Font for the text.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        border_color (pygame.Color, optional): Border color.
        border_width (int, optional): Border width.
        padding (int, optional): Padding inside the textbox.
        multiline (bool, optional): Enable multi-line input.
        max_length (int, optional): Maximum allowed text length.
        on_change (callable, optional): Callback when text changes.
        **kwargs: Additional widget options.

    Attributes:
        text (str): The current text.
        focused (bool): Whether the textbox is focused.
        cursor_pos (int): Cursor position in the text.
        selection (tuple): Selection start and end positions.
        on_change (callable): Callback for text change.
    """

    def __init__(
        self,
        master,
        width=150,
        height=28,
        text="",
        font=None,
        foreground=(0, 0, 0),
        background=(255, 255, 255),
        border_color=(120, 120, 120),
        border_width=1,
        padding=6,
        multiline=False,
        max_length=None,
        on_change=None,
        **kwargs,
    ):
        self.text = text
        self.font = font or pygame.font.SysFont(None, 20)
        self.foreground = foreground
        self.background = background
        self.border_color = border_color
        self.border_width = border_width
        self.padding = padding
        self.multiline = multiline
        self.max_length = max_length
        self.on_change = on_change

        self.focused = False
        self.cursor_pos = len(text)
        self.selection = None  # (start, end) or None
        self._cursor_visible = True
        self._cursor_timer = 0
        self._blink_interval = 500  # ms

        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the textbox, border, text, and cursor."""
        # Draw background
        surface.fill(self.background)

        # Draw border
        if self.border_width > 0:
            pygame.draw.rect(
                surface,
                self.border_color,
                surface.get_rect(),
                self.border_width,
            )

        # Render text
        text_surf = self.font.render(self.text, True, self.foreground)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (self.padding, (self._rect.height - text_rect.height) // 2)

        # Draw selection highlight if any
        if self.focused and self.selection and self.selection[0] != self.selection[1]:
            sel_start = min(self.selection)
            sel_end = max(self.selection)
            pre_text = self.text[:sel_start]
            sel_text = self.text[sel_start:sel_end]
            pre_width = self.font.size(pre_text)[0]
            sel_width = self.font.size(sel_text)[0]
            sel_rect = pygame.Rect(
                self.padding + pre_width,
                text_rect.top,
                sel_width,
                text_rect.height,
            )
            pygame.draw.rect(surface, (180, 210, 255), sel_rect)

        # Draw text
        surface.blit(text_surf, text_rect)

        # Draw cursor if focused
        if self.focused and self._cursor_visible:
            cursor_x = self.padding + self.font.size(self.text[: self.cursor_pos])[0]
            cursor_y = text_rect.top
            cursor_h = text_rect.height
            pygame.draw.line(
                surface,
                (0, 0, 0),
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_h),
                1,
            )

    def _handle_event_(self, event, *args, **kwargs):
        """Handle keyboard and mouse events for text editing."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                self.focused = True
                # Set cursor position based on click
                rel_x = event.pos[0] - self._rect.x - self.padding
                self.cursor_pos = self._get_cursor_from_x(rel_x)
                self.selection = None
            else:
                self.focused = False
                self.selection = None

        if not self.focused:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.selection and self.selection[0] != self.selection[1]:
                    self._delete_selection()
                elif self.cursor_pos > 0:
                    self.text = self.text[: self.cursor_pos - 1] + self.text[self.cursor_pos :]
                    self.cursor_pos -= 1
                    self._trigger_on_change()
            elif event.key == pygame.K_DELETE:
                if self.selection and self.selection[0] != self.selection[1]:
                    self._delete_selection()
                elif self.cursor_pos < len(self.text):
                    self.text = self.text[: self.cursor_pos] + self.text[self.cursor_pos + 1 :]
                    self._trigger_on_change()
            elif event.key == pygame.K_LEFT:
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.selection:
                        self.selection = (self.cursor_pos + 1, self.cursor_pos)
                    else:
                        self.selection = (self.selection[0], self.cursor_pos)
                else:
                    self.selection = None
            elif event.key == pygame.K_RIGHT:
                if self.cursor_pos < len(self.text):
                    self.cursor_pos += 1
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.selection:
                        self.selection = (self.cursor_pos - 1, self.cursor_pos)
                    else:
                        self.selection = (self.selection[0], self.cursor_pos)
                else:
                    self.selection = None
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
                self.selection = None
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
                self.selection = None
            elif event.key == pygame.K_RETURN:
                if self.multiline:
                    self._insert_text("\n")
                # else: ignore in single-line
            elif event.unicode and (self.max_length is None or len(self.text) < self.max_length):
                self._insert_text(event.unicode)
            self._dirty = True

    def _perform_update_(self, delta, *args, **kwargs):
        """Update cursor blink."""
        if self.focused:
            self._cursor_timer += delta * 1000  # delta in seconds
            if self._cursor_timer >= self._blink_interval:
                self._cursor_visible = not self._cursor_visible
                self._cursor_timer = 0
                self._dirty = True
        else:
            self._cursor_visible = False

    def _insert_text(self, s):
        """Insert text at cursor, replacing selection if any."""
        if self.selection and self.selection[0] != self.selection[1]:
            self._delete_selection()
        self.text = self.text[: self.cursor_pos] + s + self.text[self.cursor_pos :]
        self.cursor_pos += len(s)
        self.selection = None
        self._trigger_on_change()

    def _delete_selection(self):
        """Delete selected text."""
        start, end = sorted(self.selection)
        self.text = self.text[:start] + self.text[end:]
        self.cursor_pos = start
        self.selection = None
        self._trigger_on_change()

    def _get_cursor_from_x(self, x):
        """Get cursor position from x coordinate."""
        acc = 0
        for i, ch in enumerate(self.text):
            w = self.font.size(ch)[0]
            if acc + w // 2 > x:
                return i
            acc += w
        return len(self.text)

    def _trigger_on_change(self):
        """Call on_change callback if set."""
        if self.on_change:
            self.on_change(self.text)

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
            if config == "focused":
                return self.focused
            if config == "max_length":
                return self.max_length
            return super().configure(config)
        if "text" in kwargs:
            self.text = kwargs["text"]
            self.cursor_pos = min(self.cursor_pos, len(self.text))
            self._trigger_on_change()
        if "focused" in kwargs:
            self.focused = kwargs["focused"]
        if "max_length" in kwargs:
            self.max_length = kwargs["max_length"]


"""Uinex ListBox Widget

A ListBox is a widget that displays a list of items, allowing the user to select one or more items.
It supports keyboard and mouse navigation, customizable appearance, and callbacks for selection changes.

Features:
    - Single or multiple selection modes
    - Customizable font, colors, and item height
    - Scroll support for long lists
    - Mouse and keyboard interaction
    - Callback for selection change

Example:
    lb = ListBox(master, items=["Apple", "Banana", "Cherry"])
    lb.on_select = lambda idx, value: print("Selected:", idx, value)

Author: Sackey Ezekiel Etrue & Uinex Contributors
License: MIT
"""


class ListBox(Widget):
    """
    A widget for displaying and selecting from a list of items.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        items (list, optional): List of items to display.
        width (int, optional): Width of the listbox.
        height (int, optional): Height of the listbox.
        font (pygame.font.Font, optional): Font for item text.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        select_color (pygame.Color, optional): Selected item background color.
        item_height (int, optional): Height of each item row.
        multi (bool, optional): Enable multiple selection.
        on_select (callable, optional): Callback when selection changes.
        **kwargs: Additional widget options.

    Attributes:
        items (list): List of items.
        selected (list): List of selected indices.
        on_select (callable): Callback for selection change.
    """

    def __init__(
        self,
        master,
        items=None,
        width=120,
        height=160,
        font=None,
        foreground=(0, 0, 0),
        background=(255, 255, 255),
        select_color=(200, 220, 255),
        item_height=24,
        multi=False,
        on_select=None,
        **kwargs,
    ):
        self.items = items or []
        self.selected = []
        self.multi = multi
        self.on_select = on_select

        self.font = font or pygame.font.SysFont(None, 20)
        self.foreground = foreground
        self.background = background
        self.select_color = select_color
        self.item_height = item_height

        self._scroll = 0  # For future scroll support

        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the listbox and its items."""
        surface.fill(self.background)
        rect = surface.get_rect()
        visible_count = rect.height // self.item_height
        start = self._scroll
        end = min(start + visible_count, len(self.items))
        for idx in range(start, end):
            y = (idx - start) * self.item_height
            item_rect = pygame.Rect(0, y, rect.width, self.item_height)
            if idx in self.selected:
                pygame.draw.rect(surface, self.select_color, item_rect)
            item_surf = self.font.render(str(self.items[idx]), True, self.foreground)
            surface.blit(item_surf, (8, y + (self.item_height - item_surf.get_height()) // 2))
            # Optional: draw separator line
            pygame.draw.line(
                surface,
                (220, 220, 220),
                (0, y + self.item_height - 1),
                (rect.width, y + self.item_height - 1),
            )

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse and keyboard events for selection."""
        rect = self._rect
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos[0] - rect.x, event.pos[1] - rect.y
            idx = self._scroll + my // self.item_height
            if 0 <= idx < len(self.items):
                if self.multi:
                    if idx in self.selected:
                        self.selected.remove(idx)
                    else:
                        self.selected.append(idx)
                else:
                    self.selected = [idx]
                if self.on_select:
                    self.on_select(idx, self.items[idx])
                self._dirty = True
        elif event.type == pygame.KEYDOWN:
            if not self.items:
                return
            if not self.selected:
                self.selected = [0]
                self._dirty = True
                return
            idx = self.selected[-1]
            if event.key == pygame.K_UP:
                if idx > 0:
                    idx -= 1
                    self.selected = [idx]
                    if self.on_select:
                        self.on_select(idx, self.items[idx])
                    self._dirty = True
            elif event.key == pygame.K_DOWN:
                if idx < len(self.items) - 1:
                    idx += 1
                    self.selected = [idx]
                    if self.on_select:
                        self.on_select(idx, self.items[idx])
                    self._dirty = True

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for ListBox (not used)."""
        pass

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
            if config == "items":
                return self.items
            if config == "selected":
                return self.selected
            return super().configure(config)
        if "items" in kwargs:
            self.items = kwargs["items"]
            self.selected = []
            self._dirty = True
        if "selected" in kwargs:
            self.selected = kwargs["selected"]
            self._dirty = True
        return super().configure(**kwargs)


"""Uinex SpinBox Widget

A SpinBox is a widget that allows the user to select a numeric value by either typing it
or using increment/decrement buttons. It supports value bounds, step size, and callbacks
for value changes.

Features:
    - Integer or float value support
    - Customizable min, max, and step
    - Optional editable text field
    - Increment and decrement buttons
    - Callback for value change
    - Keyboard and mouse interaction

Example:
    sb = SpinBox(master, min_value=0, max_value=10, step=1, value=5)
    sb.on_change = lambda v: print("SpinBox value:", v)

Author: Sackey Ezekiel Etrue & Uinex Contributors
License: MIT
"""


class SpinBox(Widget):
    """
    A numeric input widget with increment and decrement buttons.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        min_value (int or float, optional): Minimum allowed value.
        max_value (int or float, optional): Maximum allowed value.
        step (int or float, optional): Step size for increment/decrement.
        value (int or float, optional): Initial value.
        width (int, optional): Width of the spinbox.
        height (int, optional): Height of the spinbox.
        font (pygame.font.Font, optional): Font for the value display.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        button_color (pygame.Color, optional): Color of the buttons.
        editable (bool, optional): Allow direct text editing.
        on_change (callable, optional): Callback when value changes.
        **kwargs: Additional widget options.

    Attributes:
        value (int or float): The current value.
        min_value (int or float): Minimum allowed value.
        max_value (int or float): Maximum allowed value.
        step (int or float): Step size for increment/decrement.
        editable (bool): Whether the value can be edited directly.
        on_change (callable): Callback for value change.
    """

    def __init__(
        self,
        master,
        min_value=0,
        max_value=100,
        step=1,
        value=0,
        width=100,
        height=32,
        font=None,
        foreground=(0, 0, 0),
        background=(255, 255, 255),
        button_color=(200, 200, 200),
        editable=True,
        on_change=None,
        **kwargs,
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = value
        self.editable = editable
        self.on_change = on_change

        self.font = font or pygame.font.SysFont(None, 20)
        self.foreground = foreground
        self.background = background
        self.button_color = button_color

        self._text = str(self.value)
        self._focused = False
        self._cursor_visible = True
        self._cursor_timer = 0
        self._blink_interval = 500  # ms
        self._cursor_pos = len(self._text)
        self._editing = False

        # Button rects
        self._button_width = height
        self._up_rect = pygame.Rect(width - self._button_width, 0, self._button_width, height // 2)
        self._down_rect = pygame.Rect(width - self._button_width, height // 2, self._button_width, height // 2)

        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the spinbox, value, and buttons."""
        # Draw background
        # surface.fill(self.background)

        # Draw value text
        text_surf = self.font.render(self._text, True, self.foreground)
        text_rect = text_surf.get_rect()
        text_rect.centery = self._rect.height // 2
        text_rect.x = 8

        # Draw selection/cursor if focused and editable
        if self.editable and self._focused and self._editing:
            cursor_x = text_rect.x + self.font.size(self._text[: self._cursor_pos])[0]
            cursor_y = text_rect.y
            cursor_h = text_rect.height
            if self._cursor_visible:
                pygame.draw.line(
                    surface,
                    (0, 0, 0),
                    (cursor_x, cursor_y),
                    (cursor_x, cursor_y + cursor_h),
                    1,
                )

        surface.blit(text_surf, text_rect)

        # Draw up/down buttons
        pygame.draw.rect(surface, self.button_color, self._up_rect)
        pygame.draw.rect(surface, self.button_color, self._down_rect)
        # Draw up arrow
        pygame.draw.polygon(
            surface,
            (60, 60, 60),
            [
                (self._up_rect.centerx, self._up_rect.top + 6),
                (self._up_rect.left + 6, self._up_rect.bottom - 6),
                (self._up_rect.right - 6, self._up_rect.bottom - 6),
            ],
        )
        # Draw down arrow
        pygame.draw.polygon(
            surface,
            (60, 60, 60),
            [
                (self._down_rect.centerx, self._down_rect.bottom - 6),
                (self._down_rect.left + 6, self._down_rect.top + 6),
                (self._down_rect.right - 6, self._down_rect.top + 6),
            ],
        )

        # Draw border
        pygame.draw.rect(surface, (120, 120, 120), surface.get_rect(), 1)

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse and keyboard events for spinbox."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            rel_pos = (event.pos[0] - self._rect.x, event.pos[1] - self._rect.y)
            if self._up_rect.collidepoint(rel_pos):
                self.increment()
            elif self._down_rect.collidepoint(rel_pos):
                self.decrement()
            elif self.editable and self._rect.collidepoint(event.pos):
                self._focused = True
                self._editing = True
                # Set cursor position based on click
                rel_x = rel_pos[0] - 8
                self._cursor_pos = self._get_cursor_from_x(rel_x)
            else:
                self._focused = False
                self._editing = False

        if not self._focused or not self.editable:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.increment()
            elif event.key == pygame.K_DOWN:
                self.decrement()
            elif event.key == pygame.K_RETURN:
                self._commit_text()
                self._editing = False
            elif event.key == pygame.K_ESCAPE:
                self._text = str(self.value)
                self._editing = False
            elif event.key == pygame.K_BACKSPACE:
                if self._cursor_pos > 0:
                    self._text = self._text[: self._cursor_pos - 1] + self._text[self._cursor_pos :]
                    self._cursor_pos -= 1
            elif event.key == pygame.K_DELETE:
                if self._cursor_pos < len(self._text):
                    self._text = self._text[: self._cursor_pos] + self._text[self._cursor_pos + 1 :]
            elif event.key == pygame.K_LEFT:
                if self._cursor_pos > 0:
                    self._cursor_pos -= 1
            elif event.key == pygame.K_RIGHT:
                if self._cursor_pos < len(self._text):
                    self._cursor_pos += 1
            elif event.unicode and (event.unicode.isdigit() or (event.unicode == "." and "." not in self._text)):
                self._text = self._text[: self._cursor_pos] + event.unicode + self._text[self._cursor_pos :]
                self._cursor_pos += 1
            self._dirty = True

    def _perform_update_(self, delta, *args, **kwargs):
        """Update cursor blink."""
        if self._focused and self.editable and self._editing:
            self._cursor_timer += delta * 1000  # delta in seconds
            if self._cursor_timer >= self._blink_interval:
                self._cursor_visible = not self._cursor_visible
                self._cursor_timer = 0
                self._dirty = True
        else:
            self._cursor_visible = False

    def increment(self):
        """Increase the value by step, up to max_value."""
        new_value = self.value + self.step
        if new_value > self.max_value:
            new_value = self.max_value
        self.set_value(new_value)

    def decrement(self):
        """Decrease the value by step, down to min_value."""
        new_value = self.value - self.step
        if new_value < self.min_value:
            new_value = self.min_value
        self.set_value(new_value)

    def set_value(self, v):
        """Set the value, clamp to min/max, and update text."""
        try:
            v = type(self.value)(v)
        except Exception:
            v = self.min_value
        v = max(self.min_value, min(self.max_value, v))
        if v != self.value:
            self.value = v
            self._text = str(self.value)
            self._cursor_pos = len(self._text)
            if self.on_change:
                self.on_change(self.value)
            self._dirty = True

    def _commit_text(self):
        """Commit the text field to the value."""
        try:
            v = float(self._text) if "." in self._text else int(self._text)
        except Exception:
            v = self.value
        self.set_value(v)
        self._text = str(self.value)
        self._cursor_pos = len(self._text)

    def _get_cursor_from_x(self, x):
        """Get cursor position from x coordinate in the text field."""
        acc = 0
        for i, ch in enumerate(self._text):
            w = self.font.size(ch)[0]
            if acc + w // 2 > x:
                return i
            acc += w
        return len(self._text)

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
            if config == "min_value":
                return self.min_value
            if config == "max_value":
                return self.max_value
            if config == "step":
                return self.step
            return super().configure(config)
        if "value" in kwargs:
            self.set_value(kwargs["value"])
        if "min_value" in kwargs:
            self.min_value = kwargs["min_value"]
            self.set_value(self.value)
        if "max_value" in kwargs:
            self.max_value = kwargs["max_value"]
            self.set_value(self.value)
        if "step" in kwargs:
            self.step


"""Uinex ComboBox Widget

A ComboBox is a widget that combines a text field with a dropdown list of options.
It allows the user to select one item from a list or type a custom value (optional).
ComboBoxes are commonly used for forms, settings, and anywhere a compact selection
widget is needed.

Features:
    - Dropdown list of selectable items
    - Optional editable text field
    - Customizable font, colors, and size
    - Mouse and keyboard interaction
    - Callback for selection change

Example:
    cb = ComboBox(master, items=["One", "Two", "Three"], width=120)
    cb.on_select = lambda idx, value: print("Selected:", idx, value)

Author: Sackey Ezekiel Etrue & Uinex Contributors
License: MIT
"""


class ComboBox(Widget):
    """
    A dropdown selection widget with optional text entry.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        items (list, optional): List of items to display.
        width (int, optional): Width of the combobox.
        height (int, optional): Height of the combobox.
        font (pygame.font.Font, optional): Font for item text.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        select_color (pygame.Color, optional): Selected item background color.
        editable (bool, optional): Allow text entry. Default is False.
        on_select (callable, optional): Callback when selection changes.
        **kwargs: Additional widget options.

    Attributes:
        items (list): List of items.
        selected (int): Index of selected item.
        text (str): Current text (selected or entered).
        dropdown_open (bool): Whether the dropdown is open.
        on_select (callable): Callback for selection change.
    """

    def __init__(
        self,
        master,
        items=None,
        width=120,
        height=32,
        font=None,
        foreground=(0, 0, 0),
        background=(255, 255, 255),
        select_color=(200, 220, 255),
        editable=False,
        on_select=None,
        **kwargs,
    ):
        self.items = items or []
        self.selected = 0 if self.items else -1
        self.text = self.items[self.selected] if self.selected >= 0 else ""
        self.dropdown_open = False
        self.on_select = on_select
        self.editable = editable

        self.font = font or pygame.font.SysFont(None, 20)
        self.foreground = foreground
        self.background = background
        self.select_color = select_color

        self._cursor_visible = True
        self._cursor_timer = 0
        self._blink_interval = 500  # ms
        self._cursor_pos = len(self.text)
        self._editing = False

        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the combobox, text, and dropdown list if open."""
        rect = surface.get_rect()
        # Draw background and border
        surface.fill(self.background)
        pygame.draw.rect(surface, (120, 120, 120), rect, 1)

        # Draw text or selected item
        text_surf = self.font.render(self.text, True, self.foreground)
        text_rect = text_surf.get_rect()
        text_rect.centery = rect.centery
        text_rect.x = 8
        surface.blit(text_surf, text_rect)

        # Draw cursor if editing
        if self.editable and self._editing and self._cursor_visible:
            cursor_x = text_rect.x + self.font.size(self.text[: self._cursor_pos])[0]
            cursor_y = text_rect.y
            cursor_h = text_rect.height
            pygame.draw.line(
                surface,
                (0, 0, 0),
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_h),
                1,
            )

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

        # Draw dropdown list if open
        if self.dropdown_open and self.items:
            menu_width = rect.width
            menu_height = rect.height * len(self.items)
            menu_rect = pygame.Rect(rect.left, rect.bottom, menu_width, menu_height)
            pygame.draw.rect(surface, self.background, menu_rect)
            pygame.draw.rect(surface, (120, 120, 120), menu_rect, 1)
            for i, item in enumerate(self.items):
                item_rect = pygame.Rect(
                    menu_rect.left,
                    menu_rect.top + i * rect.height,
                    menu_rect.width,
                    rect.height,
                )
                if i == self.selected:
                    pygame.draw.rect(surface, self.select_color, item_rect)
                item_surf = self.font.render(str(item), True, self.foreground)
                surface.blit(
                    item_surf,
                    (
                        item_rect.left + 8,
                        item_rect.centery - item_surf.get_height() // 2,
                    ),
                )

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse and keyboard events for ComboBox."""
        rect = self._rect
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = (event.pos[0] - rect.x, event.pos[1] - rect.y)
            if rect.collidepoint(event.pos):
                if self.editable:
                    self._editing = True
                self.dropdown_open = not self.dropdown_open
                self._dirty = True
            elif self.dropdown_open:
                menu_rect = pygame.Rect(
                    rect.left,
                    rect.bottom,
                    rect.width,
                    rect.height * len(self.items),
                )
                if menu_rect.collidepoint(event.pos[0] - rect.x, event.pos[1] - rect.y):
                    idx = (event.pos[1] - rect.y - rect.height) // rect.height
                    if 0 <= idx < len(self.items):
                        self.selected = idx
                        self.text = self.items[idx]
                        self.dropdown_open = False
                        self._editing = False
                        if self.on_select:
                            self.on_select(idx, self.text)
                        self._dirty = True
                else:
                    self.dropdown_open = False
                    self._editing = False
                    self._dirty = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.dropdown_open = False
            self._editing = False
            self._dirty = True

        if self.editable and self._editing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._editing = False
                    self.dropdown_open = False
                    if self.on_select:
                        self.on_select(self.selected, self.text)
                elif event.key == pygame.K_ESCAPE:
                    self._editing = False
                    self.dropdown_open = False
                elif event.key == pygame.K_BACKSPACE:
                    if self._cursor_pos > 0:
                        self.text = self.text[: self._cursor_pos - 1] + self.text[self._cursor_pos :]
                        self._cursor_pos -= 1
                elif event.key == pygame.K_DELETE:
                    if self._cursor_pos < len(self.text):
                        self.text = self.text[: self._cursor_pos] + self.text[self._cursor_pos + 1 :]
                elif event.key == pygame.K_LEFT:
                    if self._cursor_pos > 0:
                        self._cursor_pos -= 1
                elif event.key == pygame.K_RIGHT:
                    if self._cursor_pos < len(self.text):
                        self._cursor_pos += 1
                elif event.unicode:
                    self.text = self.text[: self._cursor_pos] + event.unicode + self.text[self._cursor_pos :]
                    self._cursor_pos += 1
                self._dirty = True
        elif self.dropdown_open and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.selected < len(self.items) - 1:
                    self.selected += 1
                    self.text = self.items[self.selected]
                    self._dirty = True
            elif event.key == pygame.K_UP:
                if self.selected > 0:
                    self.selected -= 1
                    self.text = self.items[self.selected]
                    self._dirty = True
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.dropdown_open = False
                self._editing = False
                if self.on_select:
                    self.on_select(self.selected, self.text)
                self._dirty = True
            elif event.key == pygame.K_ESCAPE:
                self.dropdown_open = False
                self._editing = False
                self._dirty = True

    def _perform_update_(self, delta, *args, **kwargs):
        """Update cursor blink if editing."""
        if self.editable and self._editing:
            self._cursor_timer += delta * 1000
            if self._cursor_timer >= self._blink_interval:
                self._cursor_visible = not self._cursor_visible
                self._cursor_timer = 0
                self._dirty = True
        else:
            self._cursor_visible = False

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
            if config == "items":
                return self.items
            if config == "selected":
                return self.selected
            if config == "text":
                return self.text
            return super().configure(config)
        if "items" in kwargs:
            self.items = kwargs["items"]
            self.selected = 0 if self.items else -1
            self.text = self.items[self.selected] if self.selected >= 0 else ""
            self._dirty = True
        if "selected" in kwargs:
            self.selected = kwargs["selected"]
            self.text = self.items[self.selected] if 0 <= self.selected < len(self.items) else ""
            self._dirty = True
        if "text" in kwargs:
            self.text = kwargs["text"]
            self._dirty = True
        return
