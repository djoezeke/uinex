"""PygameUI Geometry Managers

This module provides geometry manager base classes for widget layout in PygameUI.
Supported managers:
    - Pack:   Simple side-based packing (like Tkinter's pack)
    - Grid:   Table/grid-based placement (like Tkinter's grid)
    - Place:  Absolute or relative placement (like Tkinter's place)

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & PygameUI Framework Contributors
License: MIT
"""

__all__ = ["Pack", "Grid", "Place"]


class Pack:
    """Geometry manager Pack.

    Provides side-based packing for widgets, similar to Tkinter's pack manager.
    Widgets can be packed to the top, bottom, left, or right of their parent,
    with options for padding, filling, and expansion.

    Attributes:
        _anchor (str): Anchor position (e.g., 'n', 's', 'e', 'w', 'center').
        _expand (bool): Whether widget expands when parent grows.
        _fill (str): Fill direction ('none', 'x', 'y', 'both').
        _side (str): Side of parent to pack to ('top', 'bottom', 'left', 'right').
        _ipadx (int): Internal padding (x).
        _ipady (int): Internal padding (y).
        _padx (int): External padding (x).
        _pady (int): External padding (y).
    """

    def __init__(self):
        """Initialize packing options to None."""
        self._anchor: str = None
        self._expand: bool = None
        self._fill: str = None
        self._side: str = None
        self._ipadx: int = None
        self._ipady: int = None
        self._padx: int = None
        self._pady: int = None

    # region Properties
    @property
    def anchor(self):
        """Anchor position of the widget (e.g., 'n', 's', 'e', 'w', 'center')."""
        return self._anchor

    @anchor.setter
    def anchor(self, value: str):
        if value not in ("n", "s", "e", "w", "ne", "nw", "se", "sw", "center"):
            raise ValueError("Anchor must be one of NSEW or a combination thereof")
        self._anchor = value

    @property
    def expand(self):
        """Whether the widget should expand when the parent grows."""
        return self._expand

    @expand.setter
    def expand(self, value: bool):
        if not isinstance(value, bool):
            raise ValueError("Expand must be a boolean value")
        self._expand = value

    @property
    def fill(self):
        """How the widget should fill the available space ('none', 'x', 'y', 'both')."""
        return self._fill

    @fill.setter
    def fill(self, value: str):
        if value not in ("none", "x", "y", "both"):
            raise ValueError("Fill must be 'none', 'x', 'y', or 'both'")
        self._fill = value

    @property
    def side(self):
        """Side of the parent widget where the widget should be placed."""
        return self._side

    @side.setter
    def side(self, value: str):
        if value not in ("top", "bottom", "left", "right"):
            raise ValueError("Side must be 'top', 'bottom', 'left', or 'right'")
        self._side = value

    @property
    def ipadx(self):
        """Internal padding in the x direction."""
        return self._ipadx

    @ipadx.setter
    def ipadx(self, value: int):
        if value < 0:
            raise ValueError(
                "Internal padding in x direction must be a non-negative integer"
            )
        self._ipadx = value

    @property
    def ipady(self):
        """Internal padding in the y direction."""
        return self._ipady

    @ipady.setter
    def ipady(self, value: int):
        if value < 0:
            raise ValueError(
                "Internal padding in y direction must be a non-negative integer"
            )
        self._ipady = value

    @property
    def padx(self):
        """External padding in the x direction."""
        return self._padx

    @padx.setter
    def padx(self, value: int):
        if value < 0:
            raise ValueError("Padding in x direction must be a non-negative integer")
        self._padx = value

    @property
    def pady(self):
        """External padding in the y direction."""
        return self._pady

    @pady.setter
    def pady(self, value: int):
        if value < 0:
            raise ValueError("Padding in y direction must be a non-negative integer")
        self._pady = value

    # endregion Properties

    # region Public

    def pack(self, **kwargs):
        """Pack a widget in the parent widget.

        Keyword Args:
            anchor (str): Position widget according to given direction.
            expand (bool): Expand widget if parent size grows.
            fill (str): Fill widget if widget grows ('none', 'x', 'y', 'both').
            ipadx (int): Internal padding in x direction.
            ipady (int): Internal padding in y direction.
            padx (int): Padding in x direction.
            pady (int): Padding in y direction.
            side (str): Where to add this widget ('top', 'bottom', 'left', 'right').
        """
        self._anchor = kwargs.pop("anchor", self._anchor)
        self._expand = kwargs.pop("expand", self._expand)
        self._fill = kwargs.pop("fill", self._fill)
        self._side = kwargs.pop("side", self._side)
        self._ipadx = kwargs.pop("ipadx", self._ipadx)
        self._ipady = kwargs.pop("ipady", self._ipady)
        self._padx = kwargs.pop("padx", self._padx)
        self._pady = kwargs.pop("pady", self._pady)

        if kwargs:
            raise TypeError(
                f"pack() got an unexpected keyword argument: {list(kwargs.keys())[0]}"
            )
        self._pack_()

    def pack_info(self):
        """Return a dictionary of the current packing options for this widget."""
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

    # region Private

    def _pack_(self):
        """Calculate the position and size of the widget based on packing options.

        NOTE: This method assumes the widget has _rect and _master attributes.
        """
        if self._side is None:
            self._side = "top"

        # Positioning based on side
        if self._side == "top":
            self._rect.y = 0
        elif self._side == "bottom":
            self._rect.y = self._master.get_height() - self._rect.height
        elif self._side == "left":
            self._rect.x = 0
        elif self._side == "right":
            self._rect.x = self._master.get_width() - self._rect.width

        # Fill options
        if self._fill == "x":
            self._rect.width = self._master.get_width()
        elif self._fill == "y":
            self._rect.height = self._master.get_height()
        elif self._fill == "both":
            self._rect.width = self._master.get_width()
            self._rect.height = self._master.get_height()

        # Expand options
        if self._expand:
            if self._side in ["top", "bottom"]:
                self._rect.width = self._master.get_width()
            elif self._side in ["left", "right"]:
                self._rect.height = self._master.get_height()

        # Padding adjustments
        if self._ipadx is not None:
            self._rect.width += self._ipadx * 2
        if self._ipady is not None:
            self._rect.height += self._ipady * 2
        if self._padx is not None:
            self._rect.width += self._padx * 2
        if self._pady is not None:
            self._rect.height += self._pady * 2

    # endregion Private


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
        self._column: int = None
        self._columnspan: int = None
        self._row: int = None
        self._rowspan: int = None
        self._ipadx: int = None
        self._ipady: int = None
        self._padx: int = None
        self._pady: int = None

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
            raise ValueError(
                "Internal padding in x direction must be a non-negative integer"
            )
        self._ipadx = value

    @property
    def ipady(self):
        """Internal padding in y direction."""
        return self._ipady

    @ipady.setter
    def ipady(self, value: int):
        if value < 0:
            raise ValueError(
                "Internal padding in y direction must be a non-negative integer"
            )
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

    def grid(self, **kwargs):
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
        self._column = kwargs.pop("column", self._column)
        self._columnspan = kwargs.pop(
            "columnspan", 1 if self._column is not None else 1
        )
        self._row = kwargs.pop("row", self._row)
        self._rowspan = kwargs.pop("rowspan", 1 if self._row is not None else 1)
        self._ipadx = kwargs.pop("ipadx", self._ipadx)
        self._ipady = kwargs.pop("ipady", self._ipady)
        self._padx = kwargs.pop("padx", self._padx)
        self._pady = kwargs.pop("pady", self._pady)

        if kwargs:
            raise TypeError(
                f"grid() got an unexpected keyword argument: {list(kwargs.keys())[0]}"
            )
        self._grid_()

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
        }

    # endregion Public

    # region Private

    def _grid_(self):
        """Calculate the position and size of the widget in the grid.

        NOTE: This method assumes the widget has _rect and _master attributes.
        """
        cell_width = self._master.get_width() // Grid.num_columns
        cell_height = self._master.get_height() // Grid.num_rows

        if self._column is not None:
            self._rect.x = self._column * cell_width
        if self._row is not None:
            self._rect.y = self._row * cell_height
        if self._rowspan is not None:
            self._rect.height = cell_height * self._rowspan
        if self._columnspan is not None:
            self._rect.width = cell_width * self._columnspan

        # Padding adjustments
        if self._ipadx is not None:
            self._rect.width += self._ipadx * 2
        if self._ipady is not None:
            self._rect.height += self._ipady * 2
        if self._padx is not None:
            self._rect.width += self._padx * 2
        if self._pady is not None:
            self._rect.height += self._pady * 2

    # endregion Private


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
        self._x: int = None
        self._y: int = None
        self._relx: float = None
        self._rely: float = None
        self._anchor: str = None
        self._relwidth: float = None
        self._relheight: float = None
        self._bordermode: str = None

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

    def place(self, **kwargs):
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
        self._x = kwargs.pop("x", self._x)
        self._y = kwargs.pop("y", self._y)
        self._relx = kwargs.pop("relx", self._relx)
        self._rely = kwargs.pop("rely", self._rely)
        self._anchor = kwargs.pop("anchor", self._anchor)
        self._relwidth = kwargs.pop("relwidth", self._relwidth)
        self._relheight = kwargs.pop("relheight", self._relheight)
        self._bordermode = kwargs.pop("bordermode", self._bordermode)

        if kwargs:
            raise TypeError(
                f"place() got an unexpected keyword argument: {list(kwargs.keys())[0]}"
            )
        self._place_()

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
            "bordermode": self._bordermode,
        }

    info = place_info

    # endregion Public

    # region Private

    def _place_(self):
        """Calculate the position and size of the widget.

        NOTE: This method assumes the widget has _rect and _master attributes.
        """
        if self._x is not None:
            self._rect.x = self._x
        if self._relx is not None:
            self._rect.x = int(self._master.get_width() * self._relx)

        if self._y is not None:
            self._rect.y = self._y
        if self._rely is not None:
            self._rect.y = int(self._master.get_height() * self._rely)

        if hasattr(self, "_width") and self._width is not None:
            self._rect.width = self._width
        if self._relwidth is not None:
            self._rect.width = int(self._master.get_width() * self._relwidth)

        if hasattr(self, "_height") and self._height is not None:
            self._rect.height = self._height
        if self._relheight is not None:
            self._rect.height = int(self._master.get_height() * self._relheight)

    # endregion Private
