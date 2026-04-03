"""Extended widget tests covering Button, Label, Entry, Tooltip, Dialog, Scale, Progressbar."""

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
# Button tests
# ---------------------------------------------------------------------------


class TestButton:
    def test_creation_defaults(self, screen):
        from uinex import Button

        btn = Button(master=screen)
        assert btn.width == 100
        assert btn.height == 40
        assert btn.text == "Button"
        assert not btn.disabled
        assert btn.state == "normal"

    def test_disable_enable(self, screen):
        from uinex import Button

        btn = Button(master=screen, text="X")
        btn.disable()
        assert btn.disabled
        assert btn.state == "disabled"
        btn.enable()
        assert not btn.disabled
        assert btn.state == "normal"

    def test_command_binding(self, screen):
        from uinex import Button

        called = []
        btn = Button(master=screen, text="X", command=lambda: called.append(1))
        btn.place(x=10, y=10)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (30, 20)})
        btn.handle(event)
        assert len(called) == 1

    def test_set_text(self, screen):
        from uinex import Button

        btn = Button(master=screen)
        btn.text = "New Text"
        assert btn.text == "New Text"

    def test_draw_does_not_raise(self, screen):
        from uinex import Button

        btn = Button(master=screen, text="Draw Test")
        btn.place(x=50, y=50)
        screen.fill((20, 20, 30))
        btn.update(delta=0.016)
        btn.draw(surface=screen)

    def test_configure_get_text(self, screen):
        from uinex import Button

        btn = Button(master=screen, text="Configure")
        assert btn.configure("text") == "Configure"

    def test_configure_set_text(self, screen):
        from uinex import Button

        btn = Button(master=screen, text="Before")
        btn.configure(text="After")
        assert btn.configure("text") == "After"

    def test_tooltip_set(self, screen):
        from uinex import Button

        btn = Button(master=screen, text="Tooltip")
        btn.set_tooltip("My Tooltip")
        assert btn._tooltip == "My Tooltip"

    def test_bind_unbind(self, screen):
        from uinex import Button

        results = []
        btn = Button(master=screen)
        btn.bind(pygame.MOUSEBUTTONDOWN, lambda: results.append(1))
        btn.place(x=10, y=10)
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (30, 20)})
        btn.handle(event)
        assert results == [1]

        btn.unbind(pygame.MOUSEBUTTONDOWN)
        btn.handle(event)
        assert results == [1]  # no additional call


# ---------------------------------------------------------------------------
# Label tests
# ---------------------------------------------------------------------------


class TestLabel:
    def test_creation(self, screen):
        from uinex import Label

        lbl = Label(master=screen, text="Hello")
        assert lbl.text == "Hello"

    def test_set_get_text(self, screen):
        from uinex import Label

        lbl = Label(master=screen, text="A")
        lbl.set_text("B")
        assert lbl.get_text() == "B"

    def test_draw_to_surface(self, screen):
        from uinex import Label

        lbl = Label(master=screen, text="Draw")
        lbl.place(x=10, y=10)
        screen.fill((10, 10, 10))
        lbl.update(delta=0.016)
        lbl.draw(surface=screen)  # should not raise

    def test_hide_show(self, screen):
        from uinex import Label

        lbl = Label(master=screen, text="Vis")
        lbl.hide()
        assert not lbl.visible
        lbl.show()
        assert lbl.visible


# ---------------------------------------------------------------------------
# Entry tests
# ---------------------------------------------------------------------------


class TestEntry:
    def test_creation(self, screen):
        from uinex import Entry

        e = Entry(master=screen, placeholder="Type here")
        assert e.get() == ""

    def test_set_get(self, screen):
        from uinex import Entry

        e = Entry(master=screen)
        e.set("hello")
        assert e.get() == "hello"

    def test_focus_blur(self, screen):
        from uinex import Entry

        e = Entry(master=screen)
        e.place(x=10, y=10)
        e.focus()
        assert e.is_focused()
        e.blur()
        assert not e.is_focused()

    def test_keyboard_input(self, screen):
        from uinex import Entry

        e = Entry(master=screen)
        e.place(x=10, y=10)
        e.focus()

        # Simulate typing 'hi'
        for char in "hi":
            event = pygame.event.Event(
                pygame.KEYDOWN,
                {"key": ord(char), "unicode": char, "mod": 0, "scancode": 0},
            )
            e.handle(event)
        assert e.get() == "hi"

    def test_backspace(self, screen):
        from uinex import Entry

        e = Entry(master=screen, text="abc")
        e.place(x=10, y=10)
        e.focus()
        e._cursor_pos = 3
        event = pygame.event.Event(
            pygame.KEYDOWN,
            {"key": pygame.K_BACKSPACE, "unicode": "", "mod": 0, "scancode": 0},
        )
        e.handle(event)
        assert e.get() == "ab"

    def test_disable_prevents_input(self, screen):
        from uinex import Entry

        e = Entry(master=screen, text="abc")
        e.place(x=10, y=10)
        e.disable()
        # Even if focused status is forced, disabled entry ignores input
        e._focused = True
        event = pygame.event.Event(
            pygame.KEYDOWN,
            {"key": ord("x"), "unicode": "x", "mod": 0, "scancode": 0},
        )
        e.handle(event)
        # Disabled widget should return False from handle
        assert e.handle(event) is False

    def test_on_change_callback(self, screen):
        from uinex import Entry

        changes = []
        e = Entry(master=screen, on_change=lambda t: changes.append(t))
        e.set("test")
        assert "test" in changes

    def test_draw_does_not_raise(self, screen):
        from uinex import Entry

        e = Entry(master=screen, placeholder="Enter text")
        e.place(x=10, y=10)
        screen.fill((20, 20, 30))
        e.update(delta=0.016)
        e.draw(surface=screen)


# ---------------------------------------------------------------------------
# Tooltip tests
# ---------------------------------------------------------------------------


class TestTooltip:
    def test_creation(self, screen):
        from uinex import Button
        from uinex.widget.tooltip import Tooltip

        btn = Button(master=screen, text="Hover me")
        btn.place(x=10, y=10)
        tip = Tooltip(master=screen, text="I am a tooltip", target=btn)
        assert tip._text == "I am a tooltip"
        assert tip._target is btn

    def test_hidden_by_default(self, screen):
        from uinex.widget.tooltip import Tooltip

        tip = Tooltip(master=screen, text="Tip")
        assert not tip.visible

    def test_set_text(self, screen):
        from uinex.widget.tooltip import Tooltip

        tip = Tooltip(master=screen, text="Old")
        tip.set_text("New")
        assert tip._text == "New"

    def test_attach(self, screen):
        from uinex import Button
        from uinex.widget.tooltip import Tooltip

        btn1 = Button(master=screen, text="A")
        btn1.place(x=10, y=10)
        btn2 = Button(master=screen, text="B")
        btn2.place(x=100, y=10)
        tip = Tooltip(master=screen, text="Tip", target=btn1)
        tip.attach(btn2)
        assert tip._target is btn2


# ---------------------------------------------------------------------------
# Dialog tests
# ---------------------------------------------------------------------------


class TestDialog:
    def test_creation(self, screen):
        from uinex.widget.dialog import Dialog

        dlg = Dialog(master=screen, title="Hello", message="World", buttons=["OK", "Cancel"])
        assert dlg._title == "Hello"
        assert dlg._message == "World"
        assert dlg._buttons == ["OK", "Cancel"]

    def test_hidden_by_default(self, screen):
        from uinex.widget.dialog import Dialog

        dlg = Dialog(master=screen, title="T", message="M")
        assert not dlg.visible

    def test_show_centres_dialog(self, screen):
        from uinex.widget.dialog import Dialog

        dlg = Dialog(master=screen, title="T", message="M", width=200, height=120)
        dlg.show()
        assert dlg.visible
        # Centre of dialog should be near centre of 800×600 display
        cx, cy = dlg._rect.center
        assert abs(cx - 400) < 5
        assert abs(cy - 300) < 5

    def test_close_invokes_callback(self, screen):
        from uinex.widget.dialog import Dialog

        results = []
        dlg = Dialog(
            master=screen,
            title="Confirm",
            message="Sure?",
            buttons=["Yes", "No"],
            on_close=lambda r: results.append(r),
        )
        dlg.show()
        dlg.close("Yes")
        assert results == ["Yes"]
        assert not dlg.visible

    def test_modal_consumes_all_events_when_open(self, screen):
        from uinex.widget.dialog import Dialog

        dlg = Dialog(master=screen, title="T", message="M")
        dlg.show()
        for event_type in [pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
            if event_type == pygame.MOUSEBUTTONDOWN:
                ev = pygame.event.Event(event_type, {"button": 1, "pos": (0, 0)})
            elif event_type == pygame.KEYDOWN:
                ev = pygame.event.Event(event_type, {"key": pygame.K_ESCAPE, "unicode": "", "mod": 0, "scancode": 0})
            else:
                ev = pygame.event.Event(event_type)
            assert dlg.handle(ev) is True

    def test_invisible_dialog_does_not_consume(self, screen):
        from uinex.widget.dialog import Dialog

        dlg = Dialog(master=screen, title="T", message="M")
        assert not dlg.visible
        ev = pygame.event.Event(pygame.QUIT)
        assert dlg.handle(ev) is False

    def test_draw_does_not_raise(self, screen):
        from uinex.widget.dialog import Dialog

        dlg = Dialog(master=screen, title="Title", message="Some message here")
        dlg.show()
        screen.fill((20, 20, 30))
        dlg.update(delta=0.016)
        dlg.draw(surface=screen)


# ---------------------------------------------------------------------------
# Theme tests
# ---------------------------------------------------------------------------


class TestThemeManager:
    def test_defaults_present(self):
        from uinex.theme.manager import ThemeManager

        assert "font" in ThemeManager.theme
        assert "family" in ThemeManager.theme["font"]
        assert "Button" in ThemeManager.theme
        assert "background" in ThemeManager.theme["Button"]

    def test_load_builtin_theme(self):
        from uinex.theme.manager import ThemeManager

        ThemeManager.load_theme("blue")
        assert "font" in ThemeManager.theme

    def test_invalid_theme_raises(self):
        from uinex.core.exceptions import ThemeError
        from uinex.theme.manager import ThemeManager

        with pytest.raises(ThemeError):
            ThemeManager.load_theme("/nonexistent/path/theme.json")
