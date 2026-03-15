from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import timedelta

__all__ = ["parse", "format", "Duration"]

_UNIT_MAP: dict[str, float] = {
    "w": 604800,
    "week": 604800,
    "weeks": 604800,
    "d": 86400,
    "day": 86400,
    "days": 86400,
    "h": 3600,
    "hr": 3600,
    "hrs": 3600,
    "hour": 3600,
    "hours": 3600,
    "m": 60,
    "min": 60,
    "mins": 60,
    "minute": 60,
    "minutes": 60,
    "s": 1,
    "sec": 1,
    "secs": 1,
    "second": 1,
    "seconds": 1,
    "ms": 0.001,
    "millisecond": 0.001,
    "milliseconds": 0.001,
}

_PARSE_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*([a-zA-Z]+)",
)


def parse(s: str) -> float:
    """Parse a human-readable duration string to seconds.

    Supported formats include "2h30m", "2 hours 30 minutes", "2.5h",
    "150m", "500ms", "1w 2d", "1 day, 3 hours".

    Args:
        s: The duration string to parse.

    Returns:
        The duration in seconds as a float.

    Raises:
        ValueError: If the string cannot be parsed or contains unknown units.
    """
    s = s.strip()
    if not s:
        raise ValueError("Empty duration string")

    matches = _PARSE_PATTERN.findall(s)
    if not matches:
        raise ValueError(f"Cannot parse duration string: {s!r}")

    total = 0.0
    for value_str, unit_str in matches:
        unit_lower = unit_str.lower()
        if unit_lower not in _UNIT_MAP:
            raise ValueError(f"Unknown duration unit: {unit_str!r}")
        total += float(value_str) * _UNIT_MAP[unit_lower]

    return round(total, 3)


def format(seconds: float, *, style: str = "short") -> str:
    """Format seconds to a human-readable duration string.

    Args:
        seconds: The duration in seconds.
        style: Output style. One of "short", "long", "colon", or "iso".

    Returns:
        A formatted duration string.

    Raises:
        ValueError: If an unknown style is provided.
    """
    if style == "short":
        return _format_short(seconds)
    elif style == "long":
        return _format_long(seconds)
    elif style == "colon":
        return _format_colon(seconds)
    elif style == "iso":
        return _format_iso(seconds)
    else:
        raise ValueError(f"Unknown format style: {style!r}")


def _decompose(seconds: float) -> tuple[int, int, int, int, float, int]:
    """Decompose seconds into weeks, days, hours, minutes, seconds, milliseconds."""
    total_ms = round(seconds * 1000)
    ms = int(total_ms % 1000)
    total_s = int(total_ms // 1000)

    w = total_s // 604800
    total_s %= 604800
    d = total_s // 86400
    total_s %= 86400
    h = total_s // 3600
    total_s %= 3600
    m = total_s // 60
    s = total_s % 60

    return w, d, h, m, s, ms


def _format_short(seconds: float) -> str:
    w, d, h, m, s, ms = _decompose(seconds)
    parts: list[str] = []
    if w:
        parts.append(f"{w}w")
    if d:
        parts.append(f"{d}d")
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}m")
    if s:
        parts.append(f"{s}s")
    if ms:
        parts.append(f"{ms}ms")
    return " ".join(parts) if parts else "0s"


def _format_long(seconds: float) -> str:
    w, d, h, m, s, ms = _decompose(seconds)
    parts: list[str] = []
    if w:
        parts.append(f"{w} {'week' if w == 1 else 'weeks'}")
    if d:
        parts.append(f"{d} {'day' if d == 1 else 'days'}")
    if h:
        parts.append(f"{h} {'hour' if h == 1 else 'hours'}")
    if m:
        parts.append(f"{m} {'minute' if m == 1 else 'minutes'}")
    if s:
        parts.append(f"{s} {'second' if s == 1 else 'seconds'}")
    if ms:
        parts.append(f"{ms} {'millisecond' if ms == 1 else 'milliseconds'}")
    return ", ".join(parts) if parts else "0 seconds"


def _format_colon(seconds: float) -> str:
    _, _, h_total, _, _, _ = _decompose(seconds)
    total_ms = round(seconds * 1000)
    ms = int(total_ms % 1000)
    total_s = int(total_ms // 1000)
    h = total_s // 3600
    total_s %= 3600
    m = total_s // 60
    s = total_s % 60
    base = f"{h}:{m:02d}:{s:02d}"
    if ms:
        base += f".{ms:03d}"
    return base


def _format_iso(seconds: float) -> str:
    w, d, h, m, s, ms = _decompose(seconds)
    total_days = w * 7 + d
    parts = ["P"]
    if total_days:
        parts.append(f"{total_days}D")

    time_parts: list[str] = []
    if h:
        time_parts.append(f"{h}H")
    if m:
        time_parts.append(f"{m}M")
    if s or ms:
        if ms:
            sec_val = s + ms / 1000
            time_parts.append(f"{sec_val:g}S")
        else:
            time_parts.append(f"{s}S")

    if time_parts:
        parts.append("T")
        parts.extend(time_parts)

    result = "".join(parts)
    return result if result != "P" else "PT0S"


@dataclass
class Duration:
    """Represents a decomposed duration with individual time components.

    Attributes:
        weeks: Number of weeks.
        days: Number of days (0-6).
        hours: Number of hours (0-23).
        minutes: Number of minutes (0-59).
        seconds: Number of seconds (0-59).
        milliseconds: Number of milliseconds (0-999).
    """

    weeks: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    milliseconds: int = 0

    def total_seconds(self) -> float:
        """Return the total duration in seconds."""
        total = (
            self.weeks * 604800
            + self.days * 86400
            + self.hours * 3600
            + self.minutes * 60
            + self.seconds
            + self.milliseconds / 1000
        )
        return round(total, 3)

    def to_timedelta(self) -> timedelta:
        """Convert to a datetime.timedelta object."""
        return timedelta(seconds=self.total_seconds())

    @classmethod
    def from_seconds(cls, s: float) -> Duration:
        """Create a Duration from a number of seconds.

        Args:
            s: Total seconds.

        Returns:
            A Duration instance with decomposed components.
        """
        w, d, h, m, sec, ms = _decompose(s)
        return cls(weeks=w, days=d, hours=h, minutes=m, seconds=sec, milliseconds=ms)

    def __add__(self, other: Duration) -> Duration:
        if not isinstance(other, Duration):
            return NotImplemented
        total = self.total_seconds() + other.total_seconds()
        return Duration.from_seconds(total)

    def __mul__(self, factor: int | float) -> Duration:
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return Duration.from_seconds(self.total_seconds() * factor)

    def __rmul__(self, factor: int | float) -> Duration:
        return self.__mul__(factor)

    def __str__(self) -> str:
        return _format_short(self.total_seconds())
