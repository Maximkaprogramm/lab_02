
from datetime import datetime

from streamstats.analysis import analysis_events
from streamstats.models import LogEvent


def test_analysis_counts():
    events = [
        LogEvent(
            datetime.fromisoformat("2026-10-10T12:00:00+03:00"),
            "INFO", "auth", "User logged in"
        ),
        LogEvent(
            datetime.fromisoformat("2026-10-10T12:01:00+03:00"),
            "ERROR", "payments", "Payment failed"
        ),
        LogEvent(
            datetime.fromisoformat("2026-10-10T12:02:00+03:00"),
            "WARNING", "auth", "Too many attempts"
        ),
    ]

    stats = analysis_events(events)
    assert stats["total_events"] == 3
    assert stats["levels"]["INFO"] == 1
    assert stats["levels"]["ERROR"] == 1
    assert stats["levels"]["WARNING"] == 1

    assert stats["sources"]["auth"] == 2
    assert stats["sources"]["payments"] == 1

    assert stats["early"] == datetime.fromisoformat(
        "2026-10-10T12:00:00+03:00"
    )
    assert stats["late"] == datetime.fromisoformat(
        "2026-10-10T12:02:00+03:00"
    )


def test_analysis_error_sources():
    events = [
        LogEvent(datetime.fromisoformat("2026-10-10T12:00:00+03:00"),
                 "ERROR", "payments", "Payment failed"),
        LogEvent(datetime.fromisoformat("2026-10-10T12:01:00+03:00"),
                 "CRITICAL", "payments", "Database down"),
        LogEvent(datetime.fromisoformat("2026-10-10T12:02:00+03:00"),
                 "ERROR", "auth", "Login failed"),
        LogEvent(datetime.fromisoformat("2026-10-10T12:03:00+03:00"),
                 "INFO", "auth", "User logged in"),
    ]

    stats = analysis_events(events)
    assert stats["five_errors"][0] == ("payments", 2)
    assert stats["five_errors"][1] == ("auth", 1)


def test_analysis_empty():
    stats = analysis_events([])

    assert stats["total_events"] == 0
    assert stats["levels"]["CRITICAL"] == 0
    assert stats["sources"] == {}
    assert stats["five_errors"] == []
    assert stats["early"] is None
    assert stats["late"] is None

def test_analysis_multiple_events():
    events = [
        LogEvent(
            datetime.fromisoformat("2026-10-10T12:00:00+03:00"),
            "INFO",
            "auth",
            "User logged in"
        ),
        LogEvent(
            datetime.fromisoformat("2026-10-10T12:01:00+03:00"),
            "ERROR",
            "payments",
            "Payment failed"
        )
    ]

    stats = analysis_events(events)
    assert stats["total_events"] == 2
    assert stats["levels"]["ERROR"] == 1
    assert stats["levels"]["INFO"] == 1
    assert stats["sources"]["auth"] == 1
    assert stats["sources"]["payments"] == 1


def test_analysis_error_sources_equal_counts():
    timestamp = datetime.fromisoformat("2026-10-10T12:00:00+03:00")
    events = [
        LogEvent(timestamp, "ERROR", "payments", "Payment failed"),
        LogEvent(timestamp, "CRITICAL", "auth", "Login failed"),
        LogEvent(timestamp, "ERROR", "database", "Query failed"),
    ]

    stats = analysis_events(events)

    assert stats["five_errors"] == [
        ("payments", 1),
        ("auth", 1),
        ("database", 1),
    ]