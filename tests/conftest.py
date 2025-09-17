import pygame
import pytest


def pytest_report_header(config):
    if config.get_verbosity() > 0:
        return ["info1: did you know that this is a fun project", "did you?"]
    else:
        return "project deps: pygame"


def pytest_addoption(parser):
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--runslow"):
        return
    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture(scope="module")
def pygame_init():
    """Initialize Pygame for testing."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


@pytest.fixture
def screen(pygame_init):
    """Create a Pygame screen for testing."""
    screen = pygame.display.set_mode((800, 600))
    yield screen
    pygame.display.quit()
