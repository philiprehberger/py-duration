

# Duration.total_milliseconds / total_microseconds


def test_duration_total_milliseconds_basic() -> None:
    from philiprehberger_duration import Duration

    d = Duration(seconds=1, milliseconds=500)
    assert d.total_milliseconds() == 1500.0


def test_duration_total_milliseconds_from_seconds() -> None:
    from philiprehberger_duration import Duration

    d = Duration.from_seconds(2.5)
    assert d.total_milliseconds() == 2500.0


def test_duration_total_microseconds_basic() -> None:
    from philiprehberger_duration import Duration

    d = Duration(milliseconds=2, microseconds=500)
    assert d.total_microseconds() == 2500.0


def test_duration_total_microseconds_matches_total_seconds() -> None:
    from philiprehberger_duration import Duration

    d = Duration.from_seconds(1.234567)
    assert d.total_microseconds() == round(d.total_seconds() * 1_000_000, 0)
