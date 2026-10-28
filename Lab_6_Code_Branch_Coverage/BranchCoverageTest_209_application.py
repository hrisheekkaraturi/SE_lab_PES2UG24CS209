"""Branch coverage tests for hotel_booking.py.

Run from this directory:
    coverage erase
    coverage run --branch --source=hotel_booking -m pytest BranchCoverageTest_209_application.py
    coverage report -m
"""
import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


@pytest.mark.parametrize(
    "room,nights,guests,peak,expected",
    [
        ("standard", 1, 2, False, 2000),       # non-peak; no extra guest; short stay
        ("standard", 1, 3, True, 3000),        # peak; extra guest; short stay
        ("standard", 7, 2, False, 12600),      # long-stay discount
        ("deluxe", 2, 2, False, 7000),
        ("suite", 1, 4, False, 7000),
    ],
)
def test_booking_valid_combinations(room, nights, guests, peak, expected):
    assert booking_cost(room, nights, guests, peak) == expected


@pytest.mark.parametrize("room,nights", [("unknown", 1), ("standard", 0), ("standard", -1)])
def test_booking_invalid_inputs(room, nights):
    expected_message = "unknown room" if room == "unknown" else "invalid nights"
    with pytest.raises(ValueError, match=expected_message):
        booking_cost(room, nights, 2, False)


@pytest.mark.parametrize(
    "days_before,is_member,expected",
    [
        (7, False, 1000),  # first if true
        (10, True, 1000),  # full refund returns before membership adjustment
        (2, False, 500),   # elif true
        (3, True, 750),    # elif and membership true
        (1, False, 0),     # else and membership false
        (0, True, 250),    # else and membership true
    ],
)
def test_cancellation_branches(days_before, is_member, expected):
    assert cancellation_refund(1000, days_before, is_member) == expected


@pytest.mark.parametrize(
    "room,is_member,rooms_free,expected",
    [
        ("standard", True, 0, "standard"),  # no free rooms
        ("standard", True, 1, "deluxe"),    # standard member upgrade
        ("deluxe", True, 1, "suite"),       # deluxe member upgrade
        ("suite", True, 1, "suite"),        # other room fallback
        ("standard", False, 1, "standard"), # nonmember fallback
        ("deluxe", False, 1, "deluxe"),    # nonmember deluxe fallback
    ],
)
def test_room_upgrade_branches(room, is_member, rooms_free, expected):
    assert room_upgrade(room, is_member, rooms_free) == expected
