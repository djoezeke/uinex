import pygame
import pytest


@pytest.fixture(scope="module")
def pygame_init():
    """Initialize Pygame for testing."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def screen(pygame_init):
    """Create a Pygame screen for testing."""
    screen = pygame.display.set_mode((800, 600))
    yield screen
    pygame.display.quit()
