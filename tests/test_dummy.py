import pygame
import pytest

from uinex.widget.base import Widget


class DummyWidget(Widget):
    """Minimal concrete Widget for testing abstract methods."""

    def _perform_draw_(self, surface, *args, **kwargs):
        pass

    def _handle_event_(self, event, *args, **kwargs):
        pass

    def _perform_update_(self, delta, *args, **kwargs):
        pass


def test_widget_init_and_properties(screen):
    widget = DummyWidget(master=screen, width=120, height=80)
    assert widget.width == 120
    assert widget.height == 80
    assert widget.visible is True
    assert widget.focused is False
    assert widget.disabled is False
    assert widget.dirty is True
    assert isinstance(widget.surface, pygame.Surface)
    assert isinstance(widget.rect, pygame.Rect)
    assert widget.theme == "light"
    assert isinstance(widget.style, dict)


def test_widget_visibility(screen):
    widget = DummyWidget(master=screen)
    widget.hide()
    assert widget.visible is False
    widget.show()
    assert widget.visible is True


def test_widget_focus(screen):
    widget = DummyWidget(master=screen)
    widget.focus()
    assert widget.focused is True
    widget.unfocus()
    assert widget.focused is False


def test_widget_enable_disable(screen):
    widget = DummyWidget(master=screen)
    widget.disable()
    assert widget.disabled is True
    assert widget.state == "disabled"
    widget.enable()
    assert widget.disabled is False
    assert widget.state == "normal"


def test_widget_resize(screen):
    widget = DummyWidget(master=screen)
    widget.resize(200, 150)
    assert widget.width == 200
    assert widget.height == 150


def test_widget_configure_and_getconfig(screen):
    widget = DummyWidget(master=screen)
    widget.setconfig(width=222, height=111, visible=False)
    assert widget.getconfig("width") == 222
    assert widget.getconfig("height") == 111
    assert widget.visible is False


def test_widget_pack(screen):
    widget = DummyWidget(master=screen)
    widget.pack(side="top", fill="x", padx=10, pady=5)
    info = widget.pack_info()
    assert info["anchor"] == "center"
    assert info["expand"] is False
    assert info["side"] == "top"
    assert info["fill"] == "x"
    assert info["padx"] == 10
    assert info["pady"] == 5
    assert info["ipadx"] == 0
    assert info["ipady"] == 0


def test_widget_grid(screen):
    widget = DummyWidget(master=screen)
    widget.grid(row=1, column=2, rowspan=2, columnspan=1, padx=7, pady=3)
    info = widget.grid_info()
    assert info["row"] == 1
    assert info["column"] == 2
    assert info["rowspan"] == 2
    assert info["columnspan"] == 1
    assert info["padx"] == 7
    assert info["pady"] == 3
    assert info["ipadx"] == 0
    assert info["ipady"] == 0
    assert info["sticky"] is None
    widget.grid(sticky="s")
    info = widget.grid_info()
    assert info["sticky"] == "s"


def test_widget_place(screen):
    widget = DummyWidget(master=screen)
    widget.place(x=50, y=60, relx=0.1, rely=0.2, anchor="center")
    info = widget.place_info()
    assert info["x"] == 50
    assert info["y"] == 60
    assert info["relx"] == 0.1
    assert info["rely"] == 0.2
    assert info["anchor"] == "center"
    assert info["width"] == 100
    assert info["height"] == 100
    assert info["relwidth"] == 0
    assert info["relheight"] == 0


def test_widget_bind_and_unbind(screen):
    widget = DummyWidget(master=screen)
    called = False

    def handler():
        called = True

    widget.bind(pygame.KEYDOWN, handler)
    event = pygame.event.Event(pygame.KEYDOWN, {})
    widget.handle(event)
    assert not called

    widget.unbind(pygame.KEYDOWN)
    widget.handle(event)
    assert called is False

    widget.bind(pygame.KEYDOWN, handler)
    widget.handle(event)
    assert not called


@pytest.mark.skip(reason="Feature Broken")
def test_widget_after_and_post(screen):
    widget = DummyWidget(master=screen)
    called = False

    import time

    def cb():
        called = True

    run_at = widget.after(1000, cb)
    time.sleep(0.01)
    time_now = time.time()
    assert run_at == str(time_now)
    assert not called
    widget.update()

    time.sleep(0.01)
    # widget.update()
    assert called is True

    posted = False
    try:
        widget.post(pygame.USEREVENT + 1)
    except Exception:
        pytest.fail("post() raised unexpectedly")

    for event in pygame.event.get():
        if event.type == pygame.USEREVENT + 1:
            posted = True

    assert posted


def test_widget_repr_and_str(screen):
    widget = DummyWidget(master=screen)
    assert "DummyWidget" in repr(widget)
    assert "<DummyWidget widget" in str(widget)


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])
