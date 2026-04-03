"""UI samples board for quick feature display.

Run with:
    uv run python -m examples.ui_samples
"""

import pygame

from uinex import Button
from uinex import Entry
from uinex import Label
from uinex import Progressbar
from uinex import Scale
from uinex import Separator
from uinex import WidgetManager

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((820, 500))
    pygame.display.set_caption("Uinex UI Samples")
    clock = pygame.time.Clock()

    manager = WidgetManager()

    title = Label(master=screen, text="Uinex UI Samples", width=260, height=34)
    title.place(x=280, y=18)
    manager.register(title)

    sep = Separator(master=screen, length=780, color=(82, 90, 120))
    sep.place(x=20, y=60)
    manager.register(sep)

    left_title = Label(master=screen, text="Inputs", width=120, height=28)
    left_title.place(x=40, y=90)
    manager.register(left_title)

    typed = [""]
    typed_lbl = Label(master=screen, text="Typed: ", width=280, height=30)
    typed_lbl.place(x=40, y=190)
    manager.register(typed_lbl)

    entry = Entry(
        master=screen,
        width=300,
        placeholder="Type here",
        on_change=lambda value: typed.__setitem__(0, value),
    )
    entry.place(x=40, y=130)
    manager.register(entry)

    slider_lbl = Label(master=screen, text="Scale: 40", width=150, height=30)
    slider_lbl.place(x=40, y=270)
    manager.register(slider_lbl)

    progress = Progressbar(master=screen, length=300, thickness=22, value=40)
    progress.place(x=40, y=320)
    manager.register(progress)

    slider = Scale(
        master=screen,
        from_=0,
        to=100,
        value=40,
        width=300,
        height=30,
        on_change=lambda value: (
            slider_lbl.__setattr__("text", f"Scale: {int(value)}"),
            progress.configure(value=int(value)),
        ),
    )
    slider.place(x=40, y=230)
    manager.register(slider)

    right_title = Label(master=screen, text="Buttons", width=120, height=28)
    right_title.place(x=470, y=90)
    manager.register(right_title)

    counter = [0]
    count_lbl = Label(master=screen, text="Clicks: 0", width=170, height=30)
    count_lbl.place(x=470, y=240)
    manager.register(count_lbl)

    def on_click() -> None:
        counter[0] += 1
        count_lbl.text = f"Clicks: {counter[0]}"

    button = Button(master=screen, text="Primary Action", width=220, height=44, command=on_click)
    button.place(x=470, y=140)
    manager.register(button)

    dim_button = Button(master=screen, text="Half opacity", width=220, height=44)
    dim_button.set_opacity(130)
    dim_button.place(x=470, y=190)
    manager.register(dim_button)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        events = pygame.event.get()

        unconsumed = manager.process_events(events, dt=dt)
        for event in unconsumed:
            if event.type == pygame.QUIT:
                running = False

        typed_lbl.text = f"Typed: {typed[0]}"

        screen.fill((14, 16, 24))
        manager.draw_all(screen)
        pygame.display.flip()

    pygame.quit()
