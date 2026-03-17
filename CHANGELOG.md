# Changelog

## 0.2.0 (2026-03-16)

- Add comparison operators (`<`, `>`, `<=`, `>=`, `==`) to `Duration`
- Add `__sub__`, `__truediv__`, `__floordiv__`, `__mod__`, `__neg__`, `__abs__` to `Duration`
- Add ISO 8601 duration parsing (`"PT2H30M"`)
- Add colon format parsing (`"1:30:00"`)
- Add microsecond support (`us`, `μs` units)
- Fix colon formatter to include days

## 0.1.5

- Add basic import test

## 0.1.4

- Add Development section to README

## 0.1.1

- Re-release for PyPI publishing

## 0.1.0 (2026-03-15)

- Initial release
- Parse human-readable duration strings to seconds
- Format seconds to multiple styles (short, long, colon, ISO 8601)
- Duration dataclass with arithmetic and timedelta conversion
- Millisecond precision support
