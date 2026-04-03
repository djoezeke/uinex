"""Tests for the Uinex event system (UIEventDispatcher and WidgetManager.process_events)."""

import os

import pygame
import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


@pytest.fixture(scope="module")
def pygame_init():
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def screen(pygame_init):
    screen = pygame.display.set_mode((800, 600))
    yield screen
    pygame.display.quit()


# ---------------------------------------------------------------------------
# UIEventDispatcher tests
# ---------------------------------------------------------------------------


class TestUIEventDispatcher:
    def test_register_and_len(self, screen):
        from uinex import Button
        from uinex.core.events import UIEventDispatcher

        dispatcher = UIEventDispatcher()
        btn = Button(master=screen, text="A")
        btn.place(x=10, y=10)
        dispatcher.register(btn)
        assert len(dispatcher) == 1

    def test_register_duplicate_ignored(self, screen):
        from uinex import Button
        from uinex.core.events import UIEventDispatcher

        dispatcher = UIEventDispatcher()
        btn = Button(master=screen, text="A")
        btn.place(x=10, y=10)
        dispatcher.register(btn)
        dispatcher.register(btn)  # second time should be ignored
        assert len(dispatcher) == 1

    def test_unregister(self, screen):
        from uinex import Button
        from uinex.core.events import UIEventDispatcher

        dispatcher = UIEventDispatcher()
        btn = Button(master=screen, text="A")
        btn.place(x=10, y=10)
        dispatcher.register(btn)
        dispatcher.unregister(btn)
        assert len(dispatcher) == 0

    def test_unconsumed_quit_event_returned(self, screen):
        from uinex import Label
        from uinex.core.events import UIEventDispatcher

        dispatcher = UIEventDispatcher()
        lbl = Label(master=screen, text="Hello")
        lbl.place(x=400, y=400)  # Far from any event pos
        dispatcher.register(lbl)

        quit_event = pygame.event.Event(pygame.QUIT)
        unconsumed = dispatcher.process([quit_event])
        assert any(e.type == pygame.QUIT for e in unconsumed), "QUIT event should be unconsumed"

    def test_clear(self, screen):
        from uinex import Button
        from uinex import Label
        from uinex.core.events import UIEventDispatcher

        dispatcher = UIEventDispatcher()
        dispatcher.register(Button(master=screen, text="A"))
        dispatcher.register(Label(master=screen, text="B"))
        assert len(dispatcher) == 2
        dispatcher.clear()
        assert len(dispatcher) == 0

    def test_contains(self, screen):
        from uinex import Button
        from uinex.core.events import UIEventDispatcher

        dispatcher = UIEventDispatcher()
        btn = Button(master=screen, text="A")
        dispatcher.register(btn)
        assert btn in dispatcher

    def test_process_calls_update(self, screen):
        """process() must call update() on each widget."""
        from uinex import Label
        from uinex.core.events import UIEventDispatcher

        dispatcher = UIEventDispatcher()
        lbl = Label(master=screen, text="Test")
        lbl.place(x=10, y=10)
        dispatcher.register(lbl)
        # Should not raise
        dispatcher.process([], dt=0.016)


# ---------------------------------------------------------------------------
# WidgetManager.process_events tests
# ---------------------------------------------------------------------------


class TestWidgetManager:
    def test_process_events_returns_unconsumed(self, screen):
        from uinex import Label
        from uinex.widget.manager import WidgetManager

        mgr = WidgetManager()
        lbl = Label(master=screen, text="Hello")
        lbl.place(x=400, y=400)
        mgr.register(lbl)

        quit_event = pygame.event.Event(pygame.QUIT)
        unconsumed = mgr.process_events([quit_event], dt=0.016)
        assert any(e.type == pygame.QUIT for e in unconsumed)

    def test_process_events_modal_dialog_consumes_all(self, screen):
        from uinex.widget.dialog import Dialog
        from uinex.widget.manager import WidgetManager

        mgr = WidgetManager()
        dlg = Dialog(master=screen, title="T", message="M", buttons=["OK"])
        mgr.register(dlg, layer=WidgetManager.OVERLAY_LAYER)
        dlg.show()

        events = [
            pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (10, 10)}),
            pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE, "unicode": " ", "mod": 0, "scancode": 0}),
        ]
        unconsumed = mgr.process_events(events, dt=0.0)
        assert len(unconsumed) == 0, "Dialog should consume all events while open"

    def test_draw_all_does_not_raise(self, screen):
        from uinex import Button
        from uinex import Label
        from uinex.widget.manager import WidgetManager

        mgr = WidgetManager()
        btn = Button(master=screen, text="OK")
        btn.place(x=10, y=10)
        lbl = Label(master=screen, text="Label")
        lbl.place(x=10, y=60)
        mgr.register(btn)
        mgr.register(lbl)
        screen.fill((20, 20, 30))
        mgr.draw_all(screen)  # Should not raise

    def test_higher_layer_drawn_last(self, screen):
        """Verify layer ordering: higher layer widgets are registered on top."""
        from uinex import Button
        from uinex import Label
        from uinex.widget.manager import WidgetManager

        mgr = WidgetManager()
        btn = Button(master=screen, text="Base")
        btn.place(x=10, y=10)
        lbl = Label(master=screen, text="Overlay")
        lbl.place(x=10, y=10)
        mgr.register(btn, layer=0)
        mgr.register(lbl, layer=WidgetManager.OVERLAY_LAYER)

        assert len(mgr) == 2

    def test_update_all_does_not_raise(self, screen):
        from uinex import Label
        from uinex.widget.manager import WidgetManager

        mgr = WidgetManager()
        lbl = Label(master=screen, text="Hi")
        lbl.place(x=10, y=10)
        mgr.register(lbl)
        mgr.update_all(dt=0.016)  # Should not raise

    def test_handle_returns_bool(self, screen):
        from uinex import Button

        btn = Button(master=screen, text="Click me")
        btn.place(x=10, y=10)
        event = pygame.event.Event(pygame.QUIT)
        result = btn.handle(event)
        assert isinstance(result, bool)


# ---------------------------------------------------------------------------
# Widget.handle() consumption flag
# ---------------------------------------------------------------------------


class TestHandleConsumption:
    def test_disabled_widget_does_not_consume(self, screen):
        from uinex import Button

        btn = Button(master=screen, text="Disabled")
        btn.place(x=10, y=10)
        btn.disable()
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (20, 20)})
        assert btn.handle(event) is False

    def test_bound_event_consumed(self, screen):
        from uinex import Button

        results = []
        btn = Button(master=screen, text="Bind")
        btn.place(x=10, y=10)
        btn.bind(pygame.KEYDOWN, lambda: results.append(True))
        btn.focus()
        event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a, "unicode": "a", "mod": 0, "scancode": 0})
        consumed = btn.handle(event)
        assert consumed is True
        assert len(results) == 1
