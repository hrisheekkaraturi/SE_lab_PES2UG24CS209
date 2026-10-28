"""Line/code coverage tests for hotel_booking.py.

Run from this directory:
    coverage erase
    coverage run --source=hotel_booking -m pytest CodeCoverageTest_209_application.py
    coverage report -m
"""
import pytest
from hotel_booking import booking_cost, cancellation_refund, room_upgrade


def test_booking_invalid_room():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("penthouse", 2, 2, True)


def test_booking_invalid_nights():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 2, True)


def test_booking_peak_extra_guests_week_discount():
    # Exercises peak pricing, extra-guest charge, and long-stay discount.
    assert booking_cost("deluxe", 7, 3, True) == 7 * (3500 + 3500 // 4) + 7 * 500 - (7 * (3500 + 3500 // 4) + 7 * 500) // 10


def test_cancellation_full_refund_member():
    # Full-refund return line and membership branch.
    assert cancellation_refund(1000, 10, True) == 1000


def test_cancellation_half_refund_member():
    assert cancellation_refund(1000, 3, True) == 750


def test_cancellation_zero_refund_nonmember():
    assert cancellation_refund(1000, 1, False) == 0


def test_upgrade_no_rooms():
    assert room_upgrade("standard", True, 0) == "standard"


def test_upgrade_standard_member():
    assert room_upgrade("standard", True, 1) == "deluxe"


def test_upgrade_deluxe_member():
    assert room_upgrade("deluxe", True, 1) == "suite"


def test_upgrade_nonmember_fallback():
    assert room_upgrade("standard", False, 1) == "standard"
