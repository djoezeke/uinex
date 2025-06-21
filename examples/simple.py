"""PygameUI Simple Widgets Demo"""

import pygame
from pygameui import Label, Button, Separator

# --------------------------------------------------------------------
# PygameUI Simple Widget Demonstration.

if __name__ == "__main__":

    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((560, 480))
    pygame.display.set_caption("Simple Demo | PygameUI")
    # pygame.display.set_icon()

    BACKGROUND = (0, 233, 45)
    ACCENT = (58, 141, 255)

    label = Label(master=screen, text="My Label", width=500, background=BACKGROUND)
    label.place(x=30, y=10)

    separator = Separator(master=screen, length=500, color=ACCENT)
    separator.place(y=400, x=30)

    button = Button(master=screen, length=100, background=ACCENT)
    button.place(y=100, x=230)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            separator.handle(event)
            button.handle(event)
            label.handle(event)

        separator.update()
        button.update()
        label.update()

        screen.fill(pygame.Color("#ffffff"))

        separator.draw()
        button.draw()
        label.draw()

        pygame.display.flip()
    pygame.quit()
