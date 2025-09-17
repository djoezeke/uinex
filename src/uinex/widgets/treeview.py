"""PygameUI TreeView Widget

A TreeView is a widget that displays a hierarchical tree of items, allowing users to expand/collapse nodes
and select items. It is commonly used for file browsers, project explorers, and structured data navigation.

Features:
    - Hierarchical display of items (nodes and leaves)
    - Expand/collapse nodes with mouse click
    - Single or multiple selection support
    - Customizable icons, fonts, and colors
    - Callback for selection and expansion changes

Example:
    tree = TreeView(master, width=200, height=300)
    tree.add_node("Root")
    tree.add_node("Child", parent="Root")
    tree.on_select = lambda node: print("Selected:", node)

Author: Your Name & PygameUI Contributors
License: MIT
"""

import pygame
from uinex.core.widget import Widget
from uinex.core.themes import ThemeManager

__all__ = ["TreeView"]


class TreeNode:
    """
    Represents a node in the TreeView.

    Args:
        label (str): The display label for the node.
        parent (TreeNode, optional): Parent node.
        data (any, optional): Custom data associated with the node.
        expanded (bool, optional): Whether the node is expanded.
        children (list, optional): List of child nodes.

    Attributes:
        label (str): Node label.
        parent (TreeNode): Parent node.
        data (any): Custom data.
        expanded (bool): Node expansion state.
        children (list): Child nodes.
        selected (bool): Selection state.
    """

    def __init__(self, label, parent=None, data=None, expanded=False):
        self.label = label
        self.parent = parent
        self.data = data
        self.expanded = expanded
        self.children = []
        self.selected = False

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def is_leaf(self):
        return not self.children

    def is_root(self):
        return self.parent is None

    def get_level(self):
        level = 0
        node = self.parent
        while node:
            level += 1
            node = node.parent
        return level


class TreeView(Widget):
    """
    A widget for displaying and interacting with hierarchical tree data.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        width (int): Width of the treeview.
        height (int): Height of the treeview.
        font (pygame.font.Font, optional): Font for node labels.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        node_height (int, optional): Height of each node row.
        indent (int, optional): Indentation per tree level.
        on_select (callable, optional): Callback when a node is selected.
        on_expand (callable, optional): Callback when a node is expanded/collapsed.
        **kwargs: Additional widget options.

    Attributes:
        root_nodes (list): Top-level nodes.
        selected_node (TreeNode): Currently selected node.
        on_select (callable): Selection callback.
        on_expand (callable): Expansion callback.
    """

    def __init__(
        self,
        master,
        width=200,
        height=300,
        font=None,
        foreground=(0, 0, 0),
        background=(255, 255, 255),
        node_height=24,
        indent=20,
        on_select=None,
        on_expand=None,
        **kwargs,
    ):
        self.font = font or pygame.font.SysFont(None, 20)
        self.foreground = foreground
        self.background = background
        self.node_height = node_height
        self.indent = indent
        self.on_select = on_select
        self.on_expand = on_expand

        self.root_nodes = []
        self.selected_node = None

        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

    def add_node(self, label, parent=None, data=None, expanded=False):
        """
        Add a node to the tree.

        Args:
            label (str): Node label.
            parent (str or TreeNode, optional): Parent node or label.
            data (any, optional): Custom data.
            expanded (bool, optional): Initial expansion state.

        Returns:
            TreeNode: The created node.
        """
        if parent is None:
            node = TreeNode(label, data=data, expanded=expanded)
            self.root_nodes.append(node)
        else:
            if isinstance(parent, str):
                parent_node = self.find_node(parent)
            else:
                parent_node = parent
            node = TreeNode(label, parent=parent_node, data=data, expanded=expanded)
            parent_node.add_child(node)
        self._dirty = True
        return node

    def find_node(self, label):
        """Find a node by label (DFS)."""

        def dfs(nodes):
            for node in nodes:
                if node.label == label:
                    return node
                found = dfs(node.children)
                if found:
                    return found
            return None

        return dfs(self.root_nodes)

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the tree view and its nodes."""
        surface.fill(self.background)
        y = 0
        for node in self._visible_nodes():
            x = node.get_level() * self.indent
            # Draw expand/collapse icon if node has children
            if node.children:
                icon_rect = pygame.Rect(x + 2, y + self.node_height // 2 - 6, 12, 12)
                pygame.draw.rect(surface, (180, 180, 180), icon_rect, 1)
                if node.expanded:
                    pygame.draw.line(
                        surface, (80, 80, 80), icon_rect.midleft, icon_rect.midright, 2
                    )
                else:
                    pygame.draw.line(
                        surface, (80, 80, 80), icon_rect.midleft, icon_rect.midright, 2
                    )
                    pygame.draw.line(
                        surface, (80, 80, 80), icon_rect.midtop, icon_rect.midbottom, 2
                    )
            else:
                icon_rect = None

            # Highlight selected node
            if node.selected:
                pygame.draw.rect(
                    surface,
                    (200, 220, 255),
                    pygame.Rect(x, y, self._rect.width, self.node_height),
                )

            # Draw node label
            label_surf = self.font.render(str(node.label), True, self.foreground)
            surface.blit(
                label_surf,
                (x + 20, y + (self.node_height - label_surf.get_height()) // 2),
            )
            node._draw_rect = pygame.Rect(x, y, self._rect.width, self.node_height)
            node._icon_rect = icon_rect
            y += self.node_height

    def _visible_nodes(self):
        """Yield nodes in visible order (expanded nodes only)."""

        def walk(nodes):
            for node in nodes:
                yield node
                if node.expanded:
                    yield from walk(node.children)

        return walk(self.root_nodes)

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse events for selection and expand/collapse."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_y = event.pos[1] - self._rect.y
            idx = mouse_y // self.node_height
            nodes = list(self._visible_nodes())
            if 0 <= idx < len(nodes):
                node = nodes[idx]
                # Check if click was on expand/collapse icon
                if node._icon_rect and node._icon_rect.collidepoint(
                    event.pos[0] - self._rect.x, mouse_y
                ):
                    node.expanded = not node.expanded
                    if self.on_expand:
                        self.on_expand(node)
                else:
                    # Select node
                    if self.selected_node:
                        self.selected_node.selected = False
                    node.selected = True
                    self.selected_node = node
                    if self.on_select:
                        self.on_select(node)
                self._dirty = True

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for TreeView (not used)."""
        pass
