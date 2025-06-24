"""PygameUI Geometry Managers

This module provides geometry manager base classes for widget layout in PygameUI.

Supported managers:
    - Pack:   Side-based packing (like Tkinter's pack)
    - Grid:   Table/grid-based placement (like Tkinter's grid)
    - Place:  Absolute or relative placement (like Tkinter's place)

Each manager provides methods and properties for flexible widget layout.

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & PygameUI Framework Contributors
License: MIT
"""

from typing import Optional, Union, Literal, TypeAlias

__all__ = ["Pack", "Grid", "Place"]

Anchor: TypeAlias = Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]
Compound: TypeAlias = Literal["top", "left", "center", "right", "bottom", "none"]
Relief: TypeAlias = Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]
Bordermode: TypeAlias = Literal["inside", "outside", "ignore"]
Side: TypeAlias = Literal["left", "right", "top", "bottom"]
ScreenUnits: TypeAlias = Union[int, float]
Fill: TypeAlias = Literal["none", "x", "y", "both"]


class Pack:
    """
    Geometry manager Pack.

    Provides side-based packing for widgets, similar to Tkinter's pack manager.
    Widgets can be packed to the top, bottom, left, or right of their parent,
    with options for padding, filling, expansion, and anchor.

    Attributes:
        _anchor (str): Anchor position (e.g., 'n', 's', 'e', 'w', 'center').
        _expand (bool): Whether widget expands when parent grows.
        _fill (str): Fill direction ('none', 'x', 'y', 'both').
        _side (str): Side of parent to pack to ('top', 'bottom', 'left', 'right').
        _ipadx (int): Internal padding (x).
        _ipady (int): Internal padding (y).
        _padx (int or tuple): External padding (x).
        _pady (int or tuple): External padding (y).
    """

    def __init__(self):
        """
        Initialize packing options to defaults.
        """
        self._fill: Fill = None
        self._side: Side = None
        self._anchor: Anchor = None
        self._ipadx: ScreenUnits = 0
        self._ipady: ScreenUnits = 0
        self._expand: Union[bool, Literal[0, 1]] = False
        self._padx: Union[ScreenUnits, tuple[ScreenUnits, ScreenUnits]] = 0
        self._pady: Union[ScreenUnits, tuple[ScreenUnits, ScreenUnits]] = 0

    # region Properties

    @property
    def anchor(self) -> Optional[str]:
        """
        Anchor position of the widget (e.g., 'n', 's', 'e', 'w', 'center').
        """
        return self._anchor

    @anchor.setter
    def anchor(self, value: str):
        if value not in ("n", "s", "e", "w", "ne", "nw", "se", "sw", "center"):
            raise ValueError("Anchor must be one of NSEW or a combination thereof")
        self._anchor = value

    @property
    def expand(self) -> bool:
        """
        Whether the widget should expand when the parent grows.
        """
        return self._expand

    @expand.setter
    def expand(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Expand must be a boolean value")
        self._expand = value

    @property
    def fill(self) -> Optional[str]:
        """
        How the widget should fill the available space ('none', 'x', 'y', 'both').
        """
        return self._fill

    @fill.setter
    def fill(self, value: str):
        if value not in ("none", "x", "y", "both"):
            raise ValueError("Fill must be 'none', 'x', 'y', or 'both'")
        self._fill = value

    @property
    def side(self) -> Optional[str]:
        """
        Side of the parent widget where the widget should be placed.
        """
        return self._side

    @side.setter
    def side(self, value: str):
        if value not in ("top", "bottom", "left", "right"):
            raise ValueError("Side must be 'top', 'bottom', 'left', or 'right'")
        self._side = value

    @property
    def ipadx(self) -> int:
        """
        Internal padding in the x direction.
        """
        return self._ipadx

    @ipadx.setter
    def ipadx(self, value: int):
        if value < 0:
            raise ValueError("Internal padding in x direction must be a non-negative integer")
        self._ipadx = value

    @property
    def ipady(self) -> int:
        """
        Internal padding in the y direction.
        """
        return self._ipady

    @ipady.setter
    def ipady(self, value: int):
        if value < 0:
            raise ValueError("Internal padding in y direction must be a non-negative integer")
        self._ipady = value

    @property
    def padx(self) -> Union[int, tuple]:
        """
        External padding in the x direction.
        """
        return self._padx

    @padx.setter
    def padx(self, value: int):
        if value < 0:
            raise ValueError("Padding in x direction must be a non-negative integer")
        self._padx = value

    @property
    def pady(self) -> Union[int, tuple]:
        """
        External padding in the y direction.
        """
        return self._pady

    @pady.setter
    def pady(self, value: int):
        if value < 0:
            raise ValueError("Padding in y direction must be a non-negative integer")
        self._pady = value

    # endregion Properties

    # region Public

    def pack(
        self,
        anchor: Anchor = None,
        ipadx: ScreenUnits = 0,
        ipady: ScreenUnits = 0,
        expand: Union[bool, Literal[0, 1]] = False,
        fill: Literal["none", "x", "y", "both"] = None,
        side: Literal["left", "right", "top", "bottom"] = "top",
        padx: Union[ScreenUnits, tuple[ScreenUnits, ScreenUnits]] = 0,
        pady: Union[ScreenUnits, tuple[ScreenUnits, ScreenUnits]] = 0,
        **kwargs,
    ):
        """
        Pack a widget in the parent widget.

        Args:
            anchor (str, optional): Position widget according to given direction.
            expand (bool, optional): Expand widget if parent size grows.
            fill (str, optional): Fill widget if widget grows ('none', 'x', 'y', 'both').
            ipadx (int, optional): Internal padding in x direction.
            ipady (int, optional): Internal padding in y direction.
            padx (int or tuple, optional): Padding in x direction.
            pady (int or tuple, optional): Padding in y direction.
            side (str, optional): Where to add this widget ('top', 'bottom', 'left', 'right').
            after, before: Not implemented, for compatibility.
            **kwargs: Additional options (ignored).
        """
        # NOTE: This method assumes the widget has _rect and _master attributes.

        self._side = side or self._side or "top"
        self._anchor = anchor or self._anchor or "center"
        self._fill = fill or self._fill or "none"
        self._expand = expand or self._expand or False
        self._ipadx = ipadx
        self._ipady = ipady
        self._padx = padx
        self._pady = pady

        master = getattr(self, "_master", None)
        rect = getattr(self, "_rect", None)
        if master is None or rect is None:
            return

        # Calculate padding
        padx = self._padx if isinstance(self._padx, (int, float)) else sum(self._padx)
        pady = self._pady if isinstance(self._pady, (int, float)) else sum(self._pady)
        ipadx = self._ipadx or 0
        ipady = self._ipady or 0

        # Fill and expand
        if self._fill in ("x", "both"):
            rect.width = master.get_width() - 2 * padx
        if self._fill in ("y", "both"):
            rect.height = master.get_height() - 2 * pady
        if self._expand:
            if self._side in ("top", "bottom"):
                rect.width = master.get_width() - 2 * padx
            elif self._side in ("left", "right"):
                rect.height = master.get_height() - 2 * pady

        # Internal padding
        rect.width += 2 * ipadx
        rect.height += 2 * ipady

        # Positioning based on side
        if self._side == "top":
            rect.x = padx
            rect.y = pady
        elif self._side == "bottom":
            rect.x = padx
            rect.y = master.get_height() - rect.height - pady
        elif self._side == "left":
            rect.x = padx
            rect.y = pady
        elif self._side == "right":
            rect.x = master.get_width() - rect.width - padx
            rect.y = pady

        # Anchor adjustment (center, n, s, e, w, etc.)
        if self._anchor == "center":
            rect.center = master.get_rect().center
        elif self._anchor == "n":
            rect.midtop = master.get_rect().midtop
        elif self._anchor == "s":
            rect.midbottom = master.get_rect().midbottom
        elif self._anchor == "e":
            rect.midright = master.get_rect().midright
        elif self._anchor == "w":
            rect.midleft = master.get_rect().midleft
        elif self._anchor == "ne":
            rect.topright = master.get_rect().topright
        elif self._anchor == "nw":
            rect.topleft = master.get_rect().topleft
        elif self._anchor == "se":
            rect.bottomright = master.get_rect().bottomright
        elif self._anchor == "sw":
            rect.bottomleft = master.get_rect().bottomleft

    def pack_info(self) -> dict:
        """
        Return a dictionary of the current packing options for this widget.
        """
        return {
            "anchor": self._anchor,
            "expand": self._expand,
            "fill": self._fill,
            "side": self._side,
            "ipadx": self._ipadx,
            "ipady": self._ipady,
            "padx": self._padx,
            "pady": self._pady,
        }

    info = pack_info

    # endregion Public


class Grid:
    """Geometry manager Grid.

    Provides table/grid-based placement for widgets, similar to Tkinter's grid manager.
    Widgets can be placed in specific rows and columns, with options for spanning,
    padding, and internal padding.

    Class Attributes:
        num_rows (int): Number of rows in the grid.
        num_columns (int): Number of columns in the grid.
    """

    num_rows = 3
    num_columns = 3

    def __init__(self):
        """Initialize grid options to None."""
        self._row: int = 0
        self._column: int = 0
        self._rowspan: int = 1
        self._columnspan: int = 1
        self._ipadx: ScreenUnits = 0
        self._ipady: ScreenUnits = 0
        self._sticky: Literal["n", "s", "w", "e"] = None
        self._padx: Union[ScreenUnits, tuple[ScreenUnits, ScreenUnits]] = 0
        self._pady: Union[ScreenUnits, tuple[ScreenUnits, ScreenUnits]] = 0

    # region Properties

    @property
    def column(self):
        """Column of the widget in the grid."""
        return self._column

    @column.setter
    def column(self, value: int):
        if value < 0:
            raise ValueError("Column must be a non-negative integer")
        self._column = value

    @property
    def columnspan(self):
        """Column span of the widget in the grid."""
        return self._columnspan

    @columnspan.setter
    def columnspan(self, value: int):
        if value < 1:
            raise ValueError("Column span must be a positive integer")
        self._columnspan = value

    @property
    def row(self):
        """Row of the widget in the grid."""
        return self._row

    @row.setter
    def row(self, value: int):
        if value < 0:
            raise ValueError("Row must be a non-negative integer")
        self._row = value

    @property
    def rowspan(self):
        """Row span of the widget in the grid."""
        return self._rowspan

    @rowspan.setter
    def rowspan(self, value: int):
        if value < 1:
            raise ValueError("Row span must be a positive integer")
        self._rowspan = value

    @property
    def ipadx(self):
        """Internal padding in x direction."""
        return self._ipadx

    @ipadx.setter
    def ipadx(self, value: int):
        if value < 0:
            raise ValueError("Internal padding in x direction must be a non-negative integer")
        self._ipadx = value

    @property
    def ipady(self):
        """Internal padding in y direction."""
        return self._ipady

    @ipady.setter
    def ipady(self, value: int):
        if value < 0:
            raise ValueError("Internal padding in y direction must be a non-negative integer")
        self._ipady = value

    @property
    def padx(self):
        """External padding in x direction."""
        return self._padx

    @padx.setter
    def padx(self, value: int):
        if value < 0:
            raise ValueError("Padding in x direction must be a non-negative integer")
        self._padx = value

    @property
    def pady(self):
        """External padding in y direction."""
        return self._pady

    @pady.setter
    def pady(self, value: int):
        if value < 0:
            raise ValueError("Padding in y direction must be a non-negative integer")
        self._pady = value

    # endregion Properties

    # region Classmethod

    @classmethod
    def set_grid_size(cls, rows: int, columns: int):
        """Set the size of the grid.

        Args:
            rows (int): Number of rows.
            columns (int): Number of columns.
        """
        if rows < 1 or columns < 1:
            raise ValueError("Rows and columns must be positive integers")
        cls.num_rows = rows
        cls.num_columns = columns

    @classmethod
    def get_grid_size(cls):
        """Get the current size of the grid.

        Returns:
            tuple: (num_rows, num_columns)
        """
        return cls.num_rows, cls.num_columns

    @classmethod
    def reset_grid_size(cls):
        """Reset the grid size to the default of 3 rows and 3 columns."""
        cls.num_rows = 3
        cls.num_columns = 3

    # endregion Classmethod

    # region Public

    def grid(
        self,
        row: int = 0,
        column: int = 0,
        rowspan: int = 1,
        columnspan: int = 1,
        ipadx: ScreenUnits = 0,
        ipady: ScreenUnits = 0,
        sticky: Literal["n", "s", "w", "e"] = None,
        padx: Union[ScreenUnits, tuple[ScreenUnits, ScreenUnits]] = 0,
        pady: Union[ScreenUnits, tuple[ScreenUnits, ScreenUnits]] = 0,
        **kwargs,
    ):
        """Position a widget in the parent widget in a grid.

        Keyword Args:
            column (int): Cell column (starting with 0).
            columnspan (int): Widget spans several columns.
            ipadx (int): Internal padding in x direction.
            ipady (int): Internal padding in y direction.
            padx (int): Padding in x direction.
            pady (int): Padding in y direction.
            row (int): Cell row (starting with 0).
            rowspan (int): Widget spans several rows.
            sticky (str): Sides to stick to if cell is larger (NSEW).

        """
        # NOTE: This method assumes the widget has _rect and _master attributes.

        self._row = row
        self._column = column
        self._rowspan = rowspan
        self._columnspan = columnspan
        self._ipadx = ipadx
        self._ipady = ipady
        self._sticky = sticky
        self._padx = padx
        self._pady = pady

        master = getattr(self, "_master", None)
        rect = getattr(self, "_rect", None)
        if master is None or rect is None:
            return

        cell_width = master.get_width() // Grid.num_columns
        cell_height = master.get_height() // Grid.num_rows

        rect.x = self._column * cell_width
        rect.y = self._row * cell_height
        rect.width = cell_width * self._columnspan
        rect.height = cell_height * self._rowspan

        # Internal and external padding
        rect.width += 2 * (self._ipadx or 0)
        rect.height += 2 * (self._ipady or 0)
        rect.width += 2 * (self._padx if isinstance(self._padx, (int, float)) else sum(self._padx))
        rect.height += 2 * (self._pady if isinstance(self._pady, (int, float)) else sum(self._pady))

        # Sticky (align inside cell)
        if self._sticky == "n":
            rect.y = self._row * cell_height
        elif self._sticky == "s":
            rect.y = (self._row + 1) * cell_height - rect.height
        elif self._sticky == "e":
            rect.x = (self._column + 1) * cell_width - rect.width
        elif self._sticky == "w":
            rect.x = self._column * cell_width

    def grid_info(self):
        """Return a dictionary of the current grid options for this widget."""
        return {
            "column": self._column,
            "columnspan": self._columnspan,
            "row": self._row,
            "rowspan": self._rowspan,
            "ipadx": self._ipadx,
            "ipady": self._ipady,
            "padx": self._padx,
            "pady": self._pady,
            "sticky": self._sticky,
        }

    info = grid_info

    # endregion Public


class Place:
    """Geometry manager Place.

    Provides absolute or relative placement for widgets, similar to Tkinter's place manager.
    Widgets can be positioned by absolute coordinates or relative to the parent widget's size.

    Attributes:
        _x (int): Absolute x position.
        _y (int): Absolute y position.
        _relx (float): Relative x position (0.0 to 1.0).
        _rely (float): Relative y position (0.0 to 1.0).
        _anchor (str): Anchor position.
        _relwidth (float): Relative width (0.0 to 1.0).
        _relheight (float): Relative height (0.0 to 1.0).
        _bordermode (str): Border mode ('inside' or 'outside').
    """

    def __init__(self):
        """Initialize place options to None."""
        self._x: ScreenUnits = 0
        self._y: ScreenUnits = 0
        self._anchor: Anchor = None
        self._relx: Union[int, float] = 0
        self._rely: Union[int, float] = 0
        self._relwidth: Union[int, float] = 0
        self._relheight: Union[int, float] = 0
        self._bordermode: Literal["inside", "outside", "ignore"] = None

    # region Properties

    @property
    def x(self):
        """Absolute x position of the widget."""
        return self._x

    @x.setter
    def x(self, value: int):
        self._x = value

    @property
    def y(self):
        """Absolute y position of the widget."""
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = value

    @property
    def relx(self):
        """Relative x position of the widget (0.0 to 1.0)."""
        return self._relx

    @relx.setter
    def relx(self, value: float):
        if not (0.0 <= value <= 1.0):
            raise ValueError("relx must be between 0.0 and 1.0")
        self._relx = value

    @property
    def rely(self):
        """Relative y position of the widget (0.0 to 1.0)."""
        return self._rely

    @rely.setter
    def rely(self, value: float):
        if not (0.0 <= value <= 1.0):
            raise ValueError("rely must be between 0.0 and 1.0")
        self._rely = value

    @property
    def anchor(self):
        """Anchor position of the widget."""
        return self._anchor

    @anchor.setter
    def anchor(self, value: str):
        self._anchor = value

    @property
    def relwidth(self):
        """Relative width of the widget (0.0 to 1.0)."""
        return self._relwidth

    @relwidth.setter
    def relwidth(self, value: float):
        if not (0.0 <= value <= 1.0):
            raise ValueError("relwidth must be between 0.0 and 1.0")
        self._relwidth = value

    @property
    def relheight(self):
        """Relative height of the widget (0.0 to 1.0)."""
        return self._relheight

    @relheight.setter
    def relheight(self, value: float):
        if not (0.0 <= value <= 1.0):
            raise ValueError("relheight must be between 0.0 and 1.0")
        self._relheight = value

    @property
    def bordermode(self):
        """Border mode of the widget ('inside' or 'outside')."""
        return self._bordermode

    @bordermode.setter
    def bordermode(self, value: str):
        if value not in ("inside", "outside"):
            raise ValueError("bordermode must be 'inside' or 'outside'")
        self._bordermode = value

    # endregion Properties

    # region Public

    def place(
        self,
        x: ScreenUnits = 0,
        y: ScreenUnits = 0,
        anchor: Anchor = None,
        relx: Union[int, float] = 0,
        rely: Union[int, float] = 0,
        relwidth: Union[int, float] = 0,
        relheight: Union[int, float] = 0,
        width: Optional[ScreenUnits] = None,
        height: Optional[ScreenUnits] = None,
        bordermode: Literal["inside", "outside", "ignore"] = None,
        **kwargs,
    ):
        """Place a widget in the parent widget.

        Keyword Args:
            x (int): Absolute x position.
            y (int): Absolute y position.
            relx (float): Relative x position (0.0 to 1.0).
            rely (float): Relative y position (0.0 to 1.0).
            anchor (str): Anchor position.
            width (int): Absolute width.
            height (int): Absolute height.
            relwidth (float): Relative width (0.0 to 1.0).
            relheight (float): Relative height (0.0 to 1.0).
            bordermode (str): 'inside' or 'outside'.

        """
        # NOTE: This method assumes the widget has _rect and _master attributes.

        self._x = x
        self._y = y
        self._anchor = anchor
        self._relx = relx
        self._rely = rely
        self._relwidth = relwidth
        self._relheight = relheight
        self._bordermode = bordermode

        master = getattr(self, "_master", None)
        rect = getattr(self, "_rect", None)
        if master is None or rect is None:
            return

        # Calculate absolute position
        rect.x = int(x + (master.get_width() * relx))
        rect.y = int(y + (master.get_height() * rely))

        # Set width/height
        if width is not None:
            rect.width = width
        elif relwidth:
            rect.width = int(master.get_width() * relwidth)
        if height is not None:
            rect.height = height
        elif relheight:
            rect.height = int(master.get_height() * relheight)

        # Anchor adjustment
        if anchor == "center":
            rect.center = (rect.x, rect.y)
        elif anchor == "n":
            rect.midtop = (rect.x, rect.y)
        elif anchor == "s":
            rect.midbottom = (rect.x, rect.y)
        elif anchor == "e":
            rect.midright = (rect.x, rect.y)
        elif anchor == "w":
            rect.midleft = (rect.x, rect.y)
        elif anchor == "ne":
            rect.topright = (rect.x, rect.y)
        elif anchor == "nw":
            rect.topleft = (rect.x, rect.y)
        elif anchor == "se":
            rect.bottomright = (rect.x, rect.y)
        elif anchor == "sw":
            rect.bottomleft = (rect.x, rect.y)

    def place_info(self):
        """Return a dictionary of the current placing options for this widget."""
        return {
            "x": self._x,
            "y": self._y,
            "relx": self._relx,
            "rely": self._rely,
            "anchor": self._anchor,
            "relwidth": self._relwidth,
            "relheight": self._relheight,
            "width": self._rect.width,
            "height": self._rect.height,
            "bordermode": self._bordermode,
        }

    info = place_info

    # endregion Public
