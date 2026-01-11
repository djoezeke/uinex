"""
PygameUI (Modern GUI With Pygame)

PygameUI provides classes for the display, positioning, and
control of modern GUI widgets using Pygame.

Available Widgets:
    - Frame
    - Label
    - Entry
    - Meter
    - Scale
    - CheckButton
    - RadioButton
    - MenuButton
    - Button
    - ComboBox
    - TextBox
    - SpinBox
    - ListBox
    - TreeView
    - SizeGrip
    - Separator
    - Floodgauge
    - Progressbar

Widget properties are specified with keyword arguments,
which match the corresponding resource names.

Widgets are positioned using one of the geometry managers:
Place, Pack, or Grid. These are accessed via the methods
`.place()`, `.pack()`, and `.grid()` available on every Widget.

Actions can be bound to events via resources (e.g., the
`command` keyword argument) or with the `.bind()` method.

Example (Hello, World):
    ```python
    import pygameui
    from pygameui import Label

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((480, 280))
    pygame.display.set_caption("PygameUI Label")

    label = Label(master=screen, text="Hello, World")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            label.handle(event)
        label.update()
        screen.fill((10, 30, 50))
        label.draw()
        pygame.display.flip()

    pygame.quit()
    ```
For detailed information, see the documentation.

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & PygameUI Contributors
License: MIT
"""

from uinex.utils.version import vernum

__version__ = str(vernum)

# Base Classes
# Theme/Manager Classes
from uinex.core.themes import ThemeManager
from uinex.widget.base import Widget
from uinex.widget.button import Button
from uinex.widget.checkbutton import CheckButton
from uinex.widget.combobox import ComboBox
from uinex.widget.entry import Entry
from uinex.widget.floodgauge import Floodgauge

# Widget Classes
from uinex.widget.frame import Frame
from uinex.widget.label import Label
from uinex.widget.listbox import ListBox
from uinex.widget.menubutton import MenuButton
from uinex.widget.meter import Meter
from uinex.widget.progressbar import Progressbar
from uinex.widget.radiobutton import RadioButton
from uinex.widget.scale import Scale
from uinex.widget.separator import Separator
from uinex.widget.sizegrip import SizeGrip
from uinex.widget.spinbox import SpinBox
from uinex.widget.textbox import TextBox
from uinex.widget.treeview import TreeView

# Utility Functions


def set_default_color_theme(color_string: str):
    """
    Set the color theme or load a custom theme file by passing the path.

    Args:
        color_string (str): Name of the theme or path to a custom theme file.
    """
    ThemeManager.load_theme(color_string)
    _apply_theme_to_all_widgets()


def _apply_theme_to_all_widgets():
    """
    Enhance: Apply the loaded theme to all registered widgets.
    This ensures all widgets update their appearance when the theme changes.
    """
    widget_classes = [
        Widget,
        Frame,
        Label,
        Entry,
        Meter,
        Scale,
        Button,
        TextBox,
        SpinBox,
        ListBox,
        SizeGrip,
        TreeView,
        ComboBox,
        Separator,
        MenuButton,
        Floodgauge,
        CheckButton,
        RadioButton,
        Progressbar,
    ]
    for widget_cls in widget_classes:
        if hasattr(widget_cls, "set_theme") and callable(widget_cls.set_theme):
            widget_cls.set_theme(ThemeManager.theme)
        # Optionally, update all existing widget instances if you keep a registry


# Optionally, you can provide a function to reload theme at runtime for all widgets
def reload_theme_for_all_widgets():
    """
    Reload and apply the current theme to all widgets at runtime.
    Call this after changing the theme to ensure all widgets reflect the new styles.
    """
    _apply_theme_to_all_widgets()
