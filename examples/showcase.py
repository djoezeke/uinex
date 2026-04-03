"""Uinex Widget Showcase

Demonstrates all major Uinex widgets and the non-intrusive event handling
system in a single, self-contained Pygame application.

The showcase includes:
    - Label
    - Button (with command binding)
    - Entry (text input)
    - Separator
    - Scale (horizontal slider)
    - Progressbar
    - CheckButton / RadioButton
    - Tooltip (attached to button)
    - Dialog (triggered by a button)
    - UIEventDispatcher / WidgetManager integration

Run with::

    python -m examples.showcase
    # or
    python examples/showcase.py

The game's own events (QUIT) are handled only after the UI manager returns
them as *unconsumed*, demonstrating zero interference between UI and game.

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & Uinex Contributors
License: MIT
"""

import pygame

import uinex
from uinex import Button
from uinex import CheckButton
from uinex import Dialog
from uinex import Entry
from uinex import Label
from uinex import Progressbar
from uinex import RadioButton
from uinex import Scale
from uinex import Separator
from uinex import Tooltip
from uinex import WidgetManager

# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

SCREEN_W, SCREEN_H = 680, 520
BG_COLOR = (18, 18, 28)
TITLE_COLOR = (200, 200, 220)
PANEL_COLOR = (28, 28, 42)
ACCENT = (0, 120, 215)

FPS = 60


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption(f"Uinex Showcase  v{uinex.__version__}")
    clock = pygame.time.Clock()

    # ── Widget manager ─────────────────────────────────────────────────────
    manager = WidgetManager()

    # ── Helpers ───────────────────────────────────────────────────────────
    state_text = ["Progress: 0 %"]
    dialog_result = ["—"]

    # ── Title label ───────────────────────────────────────────────────────
    title = Label(
        master=screen,
        text="Uinex Widget Showcase",
        width=400,
        height=36,
        foreground=TITLE_COLOR,
        background=BG_COLOR,
    )
    title.place(x=140, y=12)
    manager.register(title)

    # ── Separator below title ─────────────────────────────────────────────
    sep_top = Separator(master=screen, length=640, color=(60, 60, 90))
    sep_top.place(x=20, y=55)
    manager.register(sep_top)

    # ── Button ────────────────────────────────────────────────────────────
    btn_label = Label(master=screen, text="Button:", width=100, height=30, background=BG_COLOR)
    btn_label.place(x=20, y=75)
    manager.register(btn_label)

    click_counter = [0]

    def on_click():
        click_counter[0] += 1
        click_lbl.text = f"Clicked {click_counter[0]}x"

    btn = Button(master=screen, text="Click me", width=140, height=34, command=on_click)
    btn.place(x=130, y=72)
    manager.register(btn)

    click_lbl = Label(master=screen, text="Clicked 0x", width=150, height=30, background=BG_COLOR)
    click_lbl.place(x=285, y=75)
    manager.register(click_lbl)

    # Tooltip on button
    btn_tip = Tooltip(master=screen, text="Left-click to increment the counter", target=btn)
    manager.register(btn_tip, layer=WidgetManager.OVERLAY_LAYER)

    # ── Entry ─────────────────────────────────────────────────────────────
    entry_label = Label(master=screen, text="Entry:", width=100, height=30, background=BG_COLOR)
    entry_label.place(x=20, y=120)
    manager.register(entry_label)

    typed_lbl = Label(master=screen, text="You typed: ", width=260, height=30, background=BG_COLOR)
    typed_lbl.place(x=340, y=120)
    manager.register(typed_lbl)

    entry = Entry(
        master=screen,
        width=200,
        placeholder="Type something…",
        on_change=lambda t: typed_lbl.__setattr__("_text", f"You typed: {t}"),
    )
    entry.place(x=130, y=118)
    manager.register(entry)

    # ── Scale ─────────────────────────────────────────────────────────────
    scale_label = Label(master=screen, text="Scale:", width=100, height=30, background=BG_COLOR)
    scale_label.place(x=20, y=170)
    manager.register(scale_label)

    scale_val_lbl = Label(master=screen, text="Value: 50", width=120, height=30, background=BG_COLOR)
    scale_val_lbl.place(x=370, y=170)
    manager.register(scale_val_lbl)

    scale = Scale(
        master=screen,
        from_=0,
        to=100,
        value=50,
        width=220,
        height=30,
        on_change=lambda v: scale_val_lbl.__setattr__("_text", f"Value: {int(v)}"),
    )
    scale.place(x=130, y=168)
    manager.register(scale)

    # ── Progressbar ───────────────────────────────────────────────────────
    pb_label = Label(master=screen, text="Progress:", width=100, height=30, background=BG_COLOR)
    pb_label.place(x=20, y=220)
    manager.register(pb_label)

    pb = Progressbar(master=screen, length=220, thickness=22, value=30, orientation="horizontal")
    pb.place(x=130, y=218)
    manager.register(pb)

    pb_state_lbl = Label(
        master=screen, text=state_text[0], width=140, height=30, background=BG_COLOR
    )
    pb_state_lbl.place(x=370, y=220)
    manager.register(pb_state_lbl)

    def set_progress_25():
        pb.configure(value=25)
        state_text[0] = "Progress: 25 %"
        pb_state_lbl._text = state_text[0]

    def set_progress_75():
        pb.configure(value=75)
        state_text[0] = "Progress: 75 %"
        pb_state_lbl._text = state_text[0]

    btn_25 = Button(master=screen, text="25%", width=55, height=28, command=set_progress_25)
    btn_25.place(x=130, y=254)
    manager.register(btn_25)

    btn_75 = Button(master=screen, text="75%", width=55, height=28, command=set_progress_75)
    btn_75.place(x=200, y=254)
    manager.register(btn_75)

    # ── CheckButton ───────────────────────────────────────────────────────
    chk_label = Label(master=screen, text="Check:", width=100, height=30, background=BG_COLOR)
    chk_label.place(x=20, y=300)
    manager.register(chk_label)

    chk = CheckButton(master=screen, text="Enable feature", width=160, height=28)
    chk.place(x=130, y=298)
    manager.register(chk)

    # ── RadioButton ───────────────────────────────────────────────────────
    radio_label = Label(master=screen, text="Radio:", width=100, height=30, background=BG_COLOR)
    radio_label.place(x=20, y=340)
    manager.register(radio_label)

    for i, opt in enumerate(["Option A", "Option B", "Option C"]):
        rb = RadioButton(master=screen, text=opt, width=130, height=28)
        rb.place(x=130 + i * 145, y=338)
        manager.register(rb)

    # ── Separator ─────────────────────────────────────────────────────────
    sep_mid = Separator(master=screen, length=640, color=(60, 60, 90))
    sep_mid.place(x=20, y=380)
    manager.register(sep_mid)

    # ── Dialog trigger ────────────────────────────────────────────────────
    dlg_result_lbl = Label(
        master=screen, text=f"Last dialog result: {dialog_result[0]}", width=340, height=30,
        background=BG_COLOR,
    )
    dlg_result_lbl.place(x=20, y=400)
    manager.register(dlg_result_lbl)

    dialog = Dialog(
        master=screen,
        title="Confirm Action",
        message="Do you want to proceed with this action?",
        buttons=["Yes", "No"],
        on_close=lambda r: (
            dialog_result.__setitem__(0, r or "dismissed"),
            dlg_result_lbl.__setattr__("_text", f"Last dialog result: {r or 'dismissed'}"),
        ),
    )
    manager.register(dialog, layer=WidgetManager.OVERLAY_LAYER)

    def show_dialog():
        dialog.show()

    btn_dlg = Button(master=screen, text="Open Dialog", width=140, height=34, command=show_dialog)
    btn_dlg.place(x=20, y=440)
    manager.register(btn_dlg)

    # ── Version / quit label ──────────────────────────────────────────────
    ver_lbl = Label(
        master=screen,
        text=f"Uinex v{uinex.__version__}  |  Press ESC to quit",
        width=400,
        height=24,
        background=BG_COLOR,
        foreground=(100, 100, 130),
    )
    ver_lbl.place(x=140, y=490)
    manager.register(ver_lbl)

    # ─────────────────────────────────────────────────────────────────────
    # Main loop
    # ─────────────────────────────────────────────────────────────────────
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        events = pygame.event.get()

        # process_events returns only events NOT consumed by any widget.
        # These are safe to use in game logic without risking double-handling.
        unconsumed = manager.process_events(events, dt=dt)

        for event in unconsumed:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Draw
        screen.fill(BG_COLOR)
        manager.draw_all(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
