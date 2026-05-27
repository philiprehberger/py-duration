# Changelog

## 0.3.0 (2026-05-26)

- Add `Duration.from_timedelta(td)` classmethod that mirrors `to_timedelta()` for round-tripping a `datetime.timedelta`
- Add package-card image to README

## 0.2.2 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility
- Add GitHub issue templates, dependabot config, and PR template

## 0.2.1 (2026-03-25)

- Add pytest and mypy tool configuration to pyproject.toml

## 0.2.0 (2026-03-16)

- Add comparison operators (`<`, `>`, `<=`, `>=`, `==`) to `Duration`
- Add `__sub__`, `__truediv__`, `__floordiv__`, `__mod__`, `__neg__`, `__abs__` to `Duration`
- Add ISO 8601 duration parsing (`"PT2H30M"`)
- Add colon format parsing (`"1:30:00"`)
- Add microsecond support (`us`, `μs` units)
- Fix colon formatter to include days

## 0.1.5 (2026-03-22)

- Add basic import test

## 0.1.4 (2026-03-19)

- Add Development section to README

## 0.1.1 (2026-03-17)

- Re-release for PyPI publishing

## 0.1.0 (2026-03-15)

- Initial release
- Parse human-readable duration strings to seconds
- Format seconds to multiple styles (short, long, colon, ISO 8601)
- Duration dataclass with arithmetic and timedelta conversion
- Millisecond precision support
