"""PygameUI main module.

Usage:
    python -m pygameui

    Author: Sackey Ezekiel Etrue ![djoezeke](https://github.com/djoezeke) & PygameUI Framework Contributors
    License: MIT
"""

import sys
import pygame

# Initialized Pygame.
pygame.init()
# Initialized Pygame font.
pygame.font.init()

# Check if the script is run as a module
if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m pygameui"

window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PygameUI Main Module")
# Ensure Pygame display is initialized


def main():
    """Main function to run the PygameUI application."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the screen with a color
        window.fill((50, 50, 50))

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
