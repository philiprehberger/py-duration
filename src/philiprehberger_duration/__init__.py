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
    "us": 0.000001,
    "\u03bcs": 0.000001,
    "microsecond": 0.000001,
    "microseconds": 0.000001,
}

_PARSE_PATTERN = re.compile(
    r"(\d+(?:\.\d+)?)\s*([a-zA-Zμ]+)",
)

_ISO_PATTERN = re.compile(
    r"^P(?:(\d+)D)?(?:T(?:(\d+(?:\.\d+)?)H)?(?:(\d+(?:\.\d+)?)M)?(?:(\d+(?:\.\d+)?)S)?)?$",
)

_COLON_PATTERN = re.compile(
    r"^(?:(\d+)d\s+)?(\d+):(\d{2})(?::(\d{2})(?:\.(\d{1,3}))?)?$",
)


def parse(s: str) -> float:
    """Parse a human-readable duration string to seconds.

    Supported formats include "2h30m", "2 hours 30 minutes", "2.5h",
    "150m", "500ms", "1w 2d", "1 day, 3 hours", ISO 8601 ("PT2H30M",
    "P1DT12H"), and colon format ("2:30:00", "1:05").

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

    # Try ISO 8601 format (e.g., "PT2H30M", "P1DT12H", "PT1M30S", "PT0.5S")
    iso_match = _ISO_PATTERN.match(s)
    if iso_match:
        days_str, hours_str, mins_str, secs_str = iso_match.groups()
        total = 0.0
        if days_str:
            total += int(days_str) * 86400
        if hours_str:
            total += float(hours_str) * 3600
        if mins_str:
            total += float(mins_str) * 60
        if secs_str:
            total += float(secs_str)
        return round(total, 6)

    # Try colon format (e.g., "2:30:00", "1:05", "1d 2:30:00", "1:05:30.500")
    colon_match = _COLON_PATTERN.match(s)
    if colon_match:
        day_str, part1, part2, part3, ms_str = colon_match.groups()
        total = 0.0
        if day_str:
            total += int(day_str) * 86400
        if part3 is not None:
            # h:mm:ss format
            total += int(part1) * 3600 + int(part2) * 60 + int(part3)
        else:
            # m:ss format
            total += int(part1) * 60 + int(part2)
        if ms_str:
            total += int(ms_str.ljust(3, "0")) / 1000
        return round(total, 6)

    matches = _PARSE_PATTERN.findall(s)
    if not matches:
        raise ValueError(f"Cannot parse duration string: {s!r}")

    total = 0.0
    for value_str, unit_str in matches:
        unit_lower = unit_str.lower()
        if unit_lower not in _UNIT_MAP:
            raise ValueError(f"Unknown duration unit: {unit_str!r}")
        total += float(value_str) * _UNIT_MAP[unit_lower]

    return round(total, 6)


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


def _decompose(seconds: float) -> tuple[int, int, int, int, int, int, int]:
    """Decompose seconds into weeks, days, hours, minutes, seconds, milliseconds, microseconds."""
    total_us = round(seconds * 1_000_000)
    us = int(total_us % 1000)
    total_ms = int(total_us // 1000)
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

    return w, d, h, m, s, ms, us


def _format_short(seconds: float) -> str:
    w, d, h, m, s, ms, us = _decompose(seconds)
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
    if us:
        parts.append(f"{us}us")
    return " ".join(parts) if parts else "0s"


def _format_long(seconds: float) -> str:
    w, d, h, m, s, ms, us = _decompose(seconds)
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
    if us:
        parts.append(f"{us} {'microsecond' if us == 1 else 'microseconds'}")
    return ", ".join(parts) if parts else "0 seconds"


def _format_colon(seconds: float) -> str:
    total_ms = round(seconds * 1000)
    ms = int(total_ms % 1000)
    total_s = int(total_ms // 1000)
    d = total_s // 86400
    total_s %= 86400
    h = total_s // 3600
    total_s %= 3600
    m = total_s // 60
    s = total_s % 60
    base = f"{h}:{m:02d}:{s:02d}"
    if ms:
        base += f".{ms:03d}"
    if d:
        base = f"{d}d {base}"
    return base


def _format_iso(seconds: float) -> str:
    w, d, h, m, s, ms, us = _decompose(seconds)
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


@dataclass(eq=False)
class Duration:
    """Represents a decomposed duration with individual time components.

    Attributes:
        weeks: Number of weeks.
        days: Number of days (0-6).
        hours: Number of hours (0-23).
        minutes: Number of minutes (0-59).
        seconds: Number of seconds (0-59).
        milliseconds: Number of milliseconds (0-999).
        microseconds: Number of microseconds (0-999).
    """

    weeks: int = 0
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    milliseconds: int = 0
    microseconds: int = 0

    def total_seconds(self) -> float:
        """Return the total duration in seconds."""
        total = (
            self.weeks * 604800
            + self.days * 86400
            + self.hours * 3600
            + self.minutes * 60
            + self.seconds
            + self.milliseconds / 1000
            + self.microseconds / 1_000_000
        )
        return round(total, 6)

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
        w, d, h, m, sec, ms, us = _decompose(s)
        return cls(
            weeks=w, days=d, hours=h, minutes=m, seconds=sec,
            milliseconds=ms, microseconds=us,
        )

    def __add__(self, other: Duration) -> Duration:
        if not isinstance(other, Duration):
            return NotImplemented
        total = self.total_seconds() + other.total_seconds()
        return Duration.from_seconds(total)

    def __sub__(self, other: Duration) -> Duration:
        if not isinstance(other, Duration):
            return NotImplemented
        total = self.total_seconds() - other.total_seconds()
        return Duration.from_seconds(total)

    def __mul__(self, factor: int | float) -> Duration:
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return Duration.from_seconds(self.total_seconds() * factor)

    def __rmul__(self, factor: int | float) -> Duration:
        return self.__mul__(factor)

    def __truediv__(self, factor: int | float) -> Duration:
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return Duration.from_seconds(self.total_seconds() / factor)

    def __floordiv__(self, factor: int | float) -> Duration:
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return Duration.from_seconds(self.total_seconds() // factor)

    def __mod__(self, other: Duration) -> Duration:
        if not isinstance(other, Duration):
            return NotImplemented
        return Duration.from_seconds(self.total_seconds() % other.total_seconds())

    def __neg__(self) -> Duration:
        return Duration.from_seconds(-self.total_seconds())

    def __abs__(self) -> Duration:
        return Duration.from_seconds(abs(self.total_seconds()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented
        return self.total_seconds() == other.total_seconds()

    def __lt__(self, other: Duration) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented
        return self.total_seconds() < other.total_seconds()

    def __le__(self, other: Duration) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented
        return self.total_seconds() <= other.total_seconds()

    def __gt__(self, other: Duration) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented
        return self.total_seconds() > other.total_seconds()

    def __ge__(self, other: Duration) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented
        return self.total_seconds() >= other.total_seconds()

    def __hash__(self) -> int:
        return hash(self.total_seconds())

    def __str__(self) -> str:
        return _format_short(self.total_seconds())
