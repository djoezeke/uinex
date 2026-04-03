"""Theming demo for Uinex.

Run with:
    uv run python -m examples.theming
"""

import pygame

import uinex
from uinex import Button
from uinex import Label
from uinex import ThemeManager
from uinex import WidgetManager

LIGHT_PATCH = {
    "Widget": {"background": (238, 241, 248)},
    "Label": {"background": (238, 241, 248), "text_color": (29, 34, 49)},
    "Button": {
        "background": (70, 120, 255),
        "hover_color": (56, 99, 218),
        "border_color": (39, 78, 179),
        "text_color": (255, 255, 255),
    },
}

DARK_PATCH = {
    "Widget": {"background": (20, 24, 34)},
    "Label": {"background": (20, 24, 34), "text_color": (224, 229, 245)},
    "Button": {
        "background": (101, 72, 255),
        "hover_color": (83, 57, 217),
        "border_color": (57, 37, 165),
        "text_color": (255, 255, 255),
    },
}


def apply_theme_patch(theme_patch: dict) -> None:
    ThemeManager.reset_theme()
    ThemeManager.update_theme(theme_patch)
    uinex.reload_theme_for_all_widgets()


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((660, 360))
    pygame.display.set_caption("Uinex Theming Demo")
    clock = pygame.time.Clock()

    manager = WidgetManager()

    apply_theme_patch(DARK_PATCH)

    title = Label(master=screen, text="Theme switching sample", width=360, height=36)
    title.place(x=160, y=30)
    manager.register(title)

    subtitle = Label(
        master=screen,
        text="Press 1 for DARK, 2 for LIGHT. Theme is applied to new widgets.",
        width=600,
        height=30,
    )
    subtitle.place(x=30, y=75)
    manager.register(subtitle)

    active_mode = ["DARK"]
    mode_label = Label(master=screen, text=f"Current theme: {active_mode[0]}", width=220, height=30)
    mode_label.place(x=220, y=250)
    manager.register(mode_label)

    toggle_button = Button(master=screen, text="I use current theme", width=220, height=46)
    toggle_button.place(x=220, y=150)
    manager.register(toggle_button)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        events = pygame.event.get()

        unconsumed = manager.process_events(events, dt=dt)
        for event in unconsumed:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    apply_theme_patch(DARK_PATCH)
                    active_mode[0] = "DARK"
                    mode_label.text = f"Current theme: {active_mode[0]}"
                    toggle_button.reset_style()
                elif event.key == pygame.K_2:
                    apply_theme_patch(LIGHT_PATCH)
                    active_mode[0] = "LIGHT"
                    mode_label.text = f"Current theme: {active_mode[0]}"
                    toggle_button.reset_style()

        screen.fill(ThemeManager.theme["Widget"]["background"])
        manager.draw_all(screen)
        pygame.display.flip()

    pygame.quit()
