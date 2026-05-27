"""Tests for Duration.from_timedelta."""

from __future__ import annotations

from datetime import timedelta

from philiprehberger_duration import Duration


def test_from_timedelta_basic() -> None:
    td = timedelta(hours=1, minutes=30)
    d = Duration.from_timedelta(td)
    assert d.total_seconds() == 5400


def test_roundtrip_to_timedelta() -> None:
    original = Duration(hours=1, minutes=30, seconds=15, milliseconds=500)
    td = original.to_timedelta()
    roundtrip = Duration.from_timedelta(td)
    assert original == roundtrip


def test_from_timedelta_zero() -> None:
    d = Duration.from_timedelta(timedelta(0))
    assert d.total_seconds() == 0


def test_from_timedelta_negative() -> None:
    td = timedelta(seconds=-60)
    d = Duration.from_timedelta(td)
    assert d.total_seconds() == -60


def test_from_timedelta_microseconds() -> None:
    td = timedelta(microseconds=500)
    d = Duration.from_timedelta(td)
    assert d.total_seconds() == 0.0005
