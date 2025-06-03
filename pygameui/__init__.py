"""
PygameUI (Modern GUI With Pygame)

PygameUI provides classes which allow the display, positioning and
control of widgets.

Available Widgets are :
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
    - Floodguage
    - Progressbar

Properties of the widgets are specified with keyword arguments.
Keyword arguments have the same name as the corresponding resources.

Widgets are positioned with one of the geometry managers Place, Pack
or Grid. These managers can be called with methods place, pack, grid
available in every Widget.

Actions are bound to events by resources (e.g. keyword argument
command) or with the method bind.

Example (Hello, World):
    ```python

    import pygameui
    from pygameui import Label

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((480, 280))
    pygame.display.set_caption("PygameUI Label")

    label = Label(master=screen, text="Hello, World")

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            label.handel(event)
        label.update()

        screen.fill((10, 30, 50))
        label.draw()
        pygame.display.flip()

    pygame.quit()
    ```
    For detailed information check out the documentation.

    Author: Sackey Ezekiel Etrue ![djoezeke](https://github.com/djoezeke) & PygameUI Framework Contributors
    License: MIT
"""

# Base Classes
from pygameui.core.widget import Widget

# Manager Classes
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
from pygameui.widgets.floodgauge import Floodguage
from pygameui.widgets.separator import Separator

from pygameui.widgets.meter import Meter
from pygameui.widgets.scale import Scale

from pygameui.widgets.sizegrip import SizeGrip
from pygameui.widgets.treeview import TreeView

# Other Classes


# Methods annd Functions


def set_default_color_theme(color_string: str):
    """set color theme or load custom theme file by passing the path"""
    ThemeManager.load_theme(color_string)
