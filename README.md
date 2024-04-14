# philiprehberger-duration

[![Tests](https://github.com/philiprehberger/py-duration/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-duration/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-duration.svg)](https://pypi.org/project/philiprehberger-duration/)
[![License](https://img.shields.io/github/license/philiprehberger/py-duration)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-ec6cb9)](https://github.com/sponsors/philiprehberger)

Parse and format human-readable duration strings like "2h30m" or "1 day, 3 hours".

## Installation

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

### ISO 8601 parsing

```python
from philiprehberger_duration import parse

parse("PT2H30M")           # 9000.0
parse("P1DT12H")           # 129600.0
parse("PT1M30S")           # 90.0
parse("PT0.5S")            # 0.5
```

### Colon format parsing

```python
from philiprehberger_duration import parse

parse("1:30:00")           # 5400.0
parse("1:05")              # 65.0
parse("1:05:30.500")       # 3930.5
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
d4 = d - Duration(minutes=10)
d5 = d / 2
d6 = d // 3

# Comparisons
Duration.from_seconds(60) < Duration.from_seconds(120)   # True
Duration.from_seconds(60) == Duration(minutes=1)          # True
Duration(hours=1) >= Duration(minutes=30)                 # True

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
| `parse(s: str) -> float` | Also accepts ISO 8601 (`"PT2H30M"`) and colon format (`"1:30:00"`). |
| `Duration` | Dataclass with fields: `weeks`, `days`, `hours`, `minutes`, `seconds`, `milliseconds`, `microseconds`. |
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
| Microseconds | `us`, `μs`, `microsecond`, `microseconds` |


## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## License

MIT
