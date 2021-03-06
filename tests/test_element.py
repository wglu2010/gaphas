import pytest
from os import getenv

from gaphas.canvas import Canvas
from gaphas.examples import Box
from gaphas.item import NW, NE, SE, SW


class CanvasBox:
    def __init__(self):
        self.canvas = Canvas()
        self.box = Box()
        self.handles = self.box.handles()


@pytest.fixture()
def cb():
    return CanvasBox()


def test_creation_with_size(cb):
    """Test if initial size holds when added to a canvas.

    """
    cb.box.width = 150
    cb.box.height = 153

    assert cb.box.width == 150, cb.box.width
    assert cb.box.height == 153, cb.box.height
    assert cb.box.handles()[SE].pos.x == 150, cb.box.handles()[SE].pos.x
    assert cb.box.handles()[SE].pos.y == 153, cb.box.handles()[SE].pos.y

    cb.canvas.add(cb.box)

    assert cb.box.width == 150, cb.box.width
    assert cb.box.height == 153, cb.box.height
    assert cb.box.handles()[SE].pos.x == 150, cb.box.handles()[SE].pos.x
    assert cb.box.handles()[SE].pos.y == 153, cb.box.handles()[SE].pos.y


def test_resize_se(cb):
    """Test resizing of element by dragging its SE handle.

    """
    cb.canvas.add(cb.box)

    h_nw, h_ne, h_se, h_sw = cb.handles
    assert h_nw is cb.handles[NW]
    assert h_ne is cb.handles[NE]
    assert h_sw is cb.handles[SW]
    assert h_se is cb.handles[SE]

    count = getenv("GAPHAS_TEST_COUNT")
    if count:
        count = int(count)
    else:
        count = 1

    for i in range(count):
        h_se.pos.x += 100  # h.se.{x,y} = 10, now
        h_se.pos.y += 100
        cb.box.request_update()
        cb.canvas.update()

    assert 110 * count == h_se.pos.x  # h_se changed above, should remain the same
    assert 110 * count == float(h_se.pos.y)

    assert 110 * count == float(h_ne.pos.x)
    assert 110 * count == float(h_sw.pos.y)


def test_minimal_se(cb):
    """Test resizing of element by dragging its SE handle.

    """
    cb.canvas.add(cb.box)

    h_nw, h_ne, h_se, h_sw = cb.handles
    assert h_nw is cb.handles[NW]
    assert h_ne is cb.handles[NE]
    assert h_sw is cb.handles[SW]
    assert h_se is cb.handles[SE]

    h_se.pos.x -= 20  # h.se.{x,y} == -10
    h_se.pos.y -= 20
    assert h_se.pos.x == h_se.pos.y == -10

    cb.box.request_update()
    cb.canvas.update()

    assert 10 == h_se.pos.x  # h_se changed above, should be 10
    assert 10 == h_se.pos.y

    assert 10 == h_ne.pos.x
    assert 10 == h_sw.pos.y
