import pygame
import pytest

from pygameui.widgets.progressbar import Progressbar
from pygameui.widgets.meter import Meter
from pygameui.widgets.floodgauge import Floodgauge


class TestProgressbar:
    def test_progressbar_creation(self, screen):
        pb = Progressbar(master=screen, length=150, thickness=20, value=30)
        assert isinstance(pb, Progressbar)
        assert pb.get() == 30

    def test_progressbar_set_and_get(self, screen):
        pb = Progressbar(master=screen, value=10)
        pb.set(55)
        assert pb.get() == 55

    def test_progressbar_min_max(self, screen):
        pb = Progressbar(master=screen, minimum=10, maximum=90, value=50)
        pb.set_min(20)
        assert pb._minimum == 20
        pb.set_max(80)
        assert pb._maximum == 80

    def test_progressbar_draw(self, screen):
        pb = Progressbar(master=screen, value=40)
        pb.draw()
        pygame.display.flip()

    def test_progressbar_step(self, screen):
        pb = Progressbar(master=screen, value=10)
        pb.step(15)
        assert pb.get() == 25

    def test_progressbar_orientation(self, screen):
        pb = Progressbar(master=screen, orientation="vertical")
        pb.set_orientation("horizontal")
        assert pb.orientation == "horizontal"


class TestMeter:
    def test_meter_creation(self, screen):
        m = Meter(master=screen, value=60, style="circular")
        assert isinstance(m, Meter)
        assert m.get() == 60

    def test_meter_draw_circular(self, screen):
        m = Meter(master=screen, value=80, style="circular")
        m.draw()
        pygame.display.flip()

    def test_meter_draw_horizontal(self, screen):
        m = Meter(master=screen, value=40, style="horizontal")
        m.draw()
        pygame.display.flip()

    def test_meter_step(self, screen):
        m = Meter(master=screen, value=10)
        m.step(20)
        assert m.get() == 30


class TestFloodgauge:
    def test_floodgauge_creation(self, screen):
        fg = Floodgauge(master=screen, value=25)
        assert isinstance(fg, Floodgauge)
        assert fg.get() == 25

    def test_floodgauge_draw(self, screen):
        fg = Floodgauge(master=screen, value=70)
        fg.draw()
        pygame.display.flip()

    def test_floodgauge_step(self, screen):
        fg = Floodgauge(master=screen, value=5)
        fg.step(10)
        assert fg.get() == 15


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])
