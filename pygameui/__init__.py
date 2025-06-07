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

# Base Classes
from pygameui.core.widget import Widget

# Theme/Manager Classes
from pygameui.theme.theme import ThemeManager

# Widget Classes
from pygameui.widgets.frame import Frame
from pygameui.widgets.label import Label
from pygameui.widgets.entry import Entry
from pygameui.widgets.checkbutton import CheckButton
from pygameui.widgets.radiobutton import RadioButton
from pygameui.widgets.menubutton import MenuButton
from pygameui.widgets.button import Button
from pygameui.widgets.combobox import ComboBox
from pygameui.widgets.textbox import TextBox
from pygameui.widgets.spinbox import SpinBox
from pygameui.widgets.listbox import ListBox
from pygameui.widgets.progressbar import Progressbar
from pygameui.widgets.floodgauge import Floodgauge
from pygameui.widgets.separator import Separator
from pygameui.widgets.meter import Meter
from pygameui.widgets.scale import Scale
from pygameui.widgets.sizegrip import SizeGrip
from pygameui.widgets.treeview import TreeView

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
        Frame,
        Label,
        Entry,
        Meter,
        Scale,
        CheckButton,
        RadioButton,
        MenuButton,
        Button,
        ComboBox,
        TextBox,
        SpinBox,
        ListBox,
        TreeView,
        SizeGrip,
        Separator,
        Floodgauge,
        Progressbar,
    ]
    for widget_cls in widget_classes:
        if hasattr(widget_cls, "set_theme") and callable(
            getattr(widget_cls, "set_theme")
        ):
            widget_cls.set_theme(ThemeManager.theme)
        # Optionally, update all existing widget instances if you keep a registry


# Optionally, you can provide a function to reload theme at runtime for all widgets
def reload_theme_for_all_widgets():
    """
    Reload and apply the current theme to all widgets at runtime.
    Call this after changing the theme to ensure all widgets reflect the new styles.
    """
    _apply_theme_to_all_widgets()
