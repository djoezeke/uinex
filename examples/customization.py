"""Runtime customization demo for Uinex widgets.

Run with:
    python -m examples.customization
"""

import pygame

from uinex import Button
from uinex import Label
from uinex import WidgetManager

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((620, 360))
    pygame.display.set_caption("Uinex Customization Demo")
    clock = pygame.time.Clock()

    manager = WidgetManager()

    title = Label(master=screen, text="Runtime customization", width=360, height=36)
    title.place(x=130, y=16)
    title.configure(background=(24, 28, 42), text_color=(235, 235, 250))
    manager.register(title)

    dynamic_button = Button(master=screen, text="Customize me", width=180, height=46)
    dynamic_button.place(x=220, y=126)
    dynamic_button.set_style(background=(75, 111, 255), hover_color=(61, 91, 214), border_color=(30, 48, 120))
    dynamic_button.set_opacity(245)
    manager.register(dynamic_button)

    hint = Label(
        master=screen,
        text="SPACE: randomize style   R: reset style",
        width=420,
        height=30,
        background=(16, 20, 32),
    )
    hint.place(x=100, y=290)
    manager.register(hint)

    running = True
    while running:
        dt = clock.tick(60) / 1000
        events = pygame.event.get()

        unconsumed = manager.process_events(events, dt=dt)
        for event in unconsumed:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    color = (
                        (pygame.time.get_ticks() // 3) % 255,
                        (pygame.time.get_ticks() // 7) % 255,
                        (pygame.time.get_ticks() // 11) % 255,
                    )
                    dynamic_button.set_style(background=color)
                elif event.key == pygame.K_r:
                    dynamic_button.reset_style()

        screen.fill((10, 14, 22))
        manager.draw_all(screen)
        pygame.display.flip()

    pygame.quit()
