
from datetime import datetime
from pathlib import Path

import pytest

from streamstats.errors import (
    InvalidEventError,
    InvalidTimestampError,
    StreamStatsError,
)
from streamstats.parsers import parse_events, read_csv, read_jsonl


def test_read_jsonl_invalid():
    path = Path("examples/bad_events.jsonl")
    with pytest.raises(StreamStatsError):
        for event in read_jsonl(path):
            ...


def test_parse_valid_event():
    row = {
        "timestamp": "2026-10-10T12:00:00+03:00",
        "level": "INFO",
        "source": "auth",
        "message": "User logged in",
    }

    event = parse_events(row)
    assert event.level == "INFO"
    assert event.source == "auth"
    assert event.message == "User logged in"
    assert event.timestamp == datetime.fromisoformat(
        "2026-10-10T12:00:00+03:00"
    )


def test_parse_invalid_level():
    row = {
        "timestamp": "2026-10-10T12:00:00+03:00",
        "level": "UNKNOWN",
        "source": "auth",
        "message": "User logged in",
    }
    with pytest.raises(InvalidEventError):
        parse_events(row)

def test_parse_invalid_timestamp():
    row = {
        "timestamp": "where date",
        "level": "INFO",
        "source": "auth",
        "message": "User logged in",
    }
    with pytest.raises(InvalidTimestampError):
        parse_events(row)


def test_read_csv():
    path = Path("examples/events.csv")
    events = list(read_csv(path))
    assert len(events) == 3
    assert events[0].level == "INFO"
    assert events[1].source == "payments"
    assert events[2].level == "WARNING"



def test_read_jsonl():
    path = Path("examples/events.jsonl")
    events = list(read_jsonl(path))
    assert len(events) == 3
    assert events[0].level == "INFO"
    assert events[1].source == "payments"
    assert events[2].level == "WARNING"

def test_read_jsonl_skip_invalid():
    path = Path("examples/bad_events.jsonl")
    skip_dict = {"count": 0}
    events = list(
        read_jsonl(
            path,
            skip_invalid=True,
            skip_dict=skip_dict
        )
    )
    assert len(events) == 2
    assert skip_dict["count"] == 1


def test_read_csv_skip_invalid():
    path = Path("examples/bad_events.csv")
    skip_dict = {"count": 0}
    events = list(
        read_csv(
            path,
            skip_invalid=True,
            skip_dict=skip_dict
        )
    )
    assert len(events) == 1
    assert skip_dict["count"] == 2
