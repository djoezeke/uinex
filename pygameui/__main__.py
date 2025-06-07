"""PygameUI Main Module

This is the entry point for running PygameUI as a module.

Usage:
    python -m pygameui

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & PygameUI Contributors
License: MIT
"""

import sys
import pygame


# # In Button.__init__:
# theme = ThemeManager.theme.get("Button", {})
# self.background = background or theme.get("background", (58, 141, 255))
# self.foreground = foreground or theme.get("foreground", (245, 247, 250))
# self.border_radius = border_radius if border_radius is not None else theme.get("border_radius", 8)
# # ...and so on for other style properties


def initialize_pygame():
    """
    Initialize Pygame and its font module.
    """
    pygame.init()
    pygame.font.init()


def create_window(width: int = 800, height: int = 600) -> pygame.Surface:
    """
    Create and return the main application window.

    Args:
        width (int): Width of the window.
        height (int): Height of the window.

    Returns:
        pygame.Surface: The created window surface.
    """
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PygameUI Main Module")
    return window


def main():
    """
    Main function to run the PygameUI application.

    Handles the main event loop and window updates.
    """
    initialize_pygame()

    # If run as a module, adjust sys.argv[0] for clarity in error messages.
    if sys.argv[0].endswith("__main__.py"):
        sys.argv[0] = "python -m pygameui"

    window = create_window()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a background color
        window.fill((50, 50, 50))

        # TODO: Add UI widgets or demo content here

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
