# philiprehberger-duration

[![Tests](https://github.com/philiprehberger/py-duration/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-duration/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-duration.svg)](https://pypi.org/project/philiprehberger-duration/)
[![License](https://img.shields.io/github/license/philiprehberger/py-duration)](LICENSE)

Parse and format human-readable duration strings like "2h30m" or "1 day, 3 hours".

## Install

```bash
pip install philiprehberger-duration
```

## Usage

### Parsing duration strings

```python
from philiprehberger_duration import parse

parse("2h30m")              # 9000.0
parse("1 day, 3 hours")    # 97200.0
parse("500ms")             # 0.5
parse("1w 2d")             # 777600.0
parse("2.5h")              # 9000.0
parse("150m")              # 9000.0
```

### Formatting seconds

```python
from philiprehberger_duration import format

format(9000)                        # "2h 30m"
format(9000, style="long")         # "2 hours, 30 minutes"
format(9000, style="colon")        # "2:30:00"
format(9000, style="iso")          # "PT2H30M"
format(90061.5, style="short")    # "1d 1h 1m 1s 500ms"
```

### Duration object

```python
from philiprehberger_duration import Duration

d = Duration.from_seconds(9000)
d.hours    # 2
d.minutes  # 30

# Arithmetic
d2 = d + Duration(minutes=15)
d3 = d * 2

# Convert to timedelta
td = d.to_timedelta()

# String representation (short format)
str(d)  # "2h 30m"
```

### Timedelta conversion

```python
from philiprehberger_duration import Duration

d = Duration(hours=1, minutes=30, milliseconds=500)
td = d.to_timedelta()  # datetime.timedelta(seconds=5400, microseconds=500000)
```

## API Reference

| Function / Class | Description |
|---|---|
| `parse(s: str) -> float` | Parse a human-readable duration string to seconds. |
| `format(seconds: float, *, style: str = "short") -> str` | Format seconds to a human-readable string. Styles: `"short"`, `"long"`, `"colon"`, `"iso"`. |
| `Duration` | Dataclass with fields: `weeks`, `days`, `hours`, `minutes`, `seconds`, `milliseconds`. |
| `Duration.total_seconds() -> float` | Return total duration in seconds. |
| `Duration.to_timedelta() -> datetime.timedelta` | Convert to a `timedelta` object. |
| `Duration.from_seconds(s: float) -> Duration` | Create a `Duration` from seconds. |

### Supported parse units

| Unit | Aliases |
|---|---|
| Weeks | `w`, `week`, `weeks` |
| Days | `d`, `day`, `days` |
| Hours | `h`, `hr`, `hrs`, `hour`, `hours` |
| Minutes | `m`, `min`, `mins`, `minute`, `minutes` |
| Seconds | `s`, `sec`, `secs`, `second`, `seconds` |
| Milliseconds | `ms`, `millisecond`, `milliseconds` |

## License

MIT
