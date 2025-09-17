import pygame
import pytest

from uinex.widgets.scale import Scale


def test_scale_creation(screen):
    scale = Scale(screen, from_=0, to=100, value=50)
    assert isinstance(scale, Scale)
    assert scale.get_value() == 50


def test_scale_set_value(screen):
    scale = Scale(screen, from_=0, to=100)
    scale.set_value(75)
    assert scale.get_value() == 75


def test_scale_set_range(screen):
    scale = Scale(screen, from_=0, to=100, value=50)
    scale.set_range(10, 90)
    assert scale.from_ == 10
    assert scale.to == 90
    assert 10 <= scale.get_value() <= 90


def test_scale_set_step(screen):
    scale = Scale(screen, from_=0, to=100, step=5)
    scale.set_step(10)
    assert scale.step == 10


def test_scale_set_orientation(screen):
    scale = Scale(screen, orientation="horizontal")
    scale.set_orientation("vertical")
    assert scale.orientation == "vertical"


def test_scale_reset(screen):
    scale = Scale(screen, from_=5, to=15, value=10)
    scale.reset()
    assert scale.get_value() == 5


def test_scale_draw(screen):
    scale = Scale(screen, from_=0, to=100, value=50)
    scale.draw()
    pygame.display.flip()


def test_scale_configure(screen):
    scale = Scale(screen, from_=0, to=100, value=50)
    scale.configure(value=80)
    assert scale.get_value() == 80
    assert scale.configure("from_") == 0
    assert scale.configure("to") == 100
    assert scale.configure("step") == 1
    assert scale.configure("orientation") == "horizontal"


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])
