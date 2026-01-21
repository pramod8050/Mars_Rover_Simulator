import pytest
from rover import Robot


def test_ignore_move_before_place():
    r = Robot()
    assert r.move() is False
    assert r.report() is None


def test_place_valid_position():
    r = Robot()
    assert r.place(1, 1, "NORTH") is True
    assert r.report() == "1,1,NORTH"


def test_place_invalid_position_is_ignored():
    r = Robot()
    assert r.place(6, 6, "NORTH") is False
    assert r.report() is None  # still not placed


def test_move_north():
    r = Robot()
    r.place(0, 0, "NORTH")
    assert r.move() is True
    assert r.report() == "0,1,NORTH"


def test_boundary_move_blocked():
    r = Robot()
    r.place(0, 0, "SOUTH")
    assert r.move() is False  # would fall off
    assert r.report() == "0,0,SOUTH"


def test_left_rotation():
    r = Robot()
    r.place(0, 0, "NORTH")
    assert r.left() is True
    assert r.report() == "0,0,WEST"


def test_right_rotation():
    r = Robot()
    r.place(0, 0, "NORTH")
    assert r.right() is True
    assert r.report() == "0,0,EAST"


def test_multiple_place_resets_state():
    r = Robot()
    r.place(0, 0, "NORTH")
    r.move()
    assert r.report() == "0,1,NORTH"

    # Re-place should reset robot state
    assert r.place(4, 4, "WEST") is True
    assert r.report() == "4,4,WEST"


def test_example_scenario_from_spec():
    r = Robot()
    r.place(1, 2, "EAST")
    r.move()
    r.move()
    r.left()
    r.move()
    assert r.report() == "3,3,NORTH"
