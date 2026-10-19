import json
from datetime import datetime

from streamstats.report import report, save_report


def test_report_converts_dates():
    stats = {
        "total_events": 2,
        "early": datetime.fromisoformat("2026-10-10T12:00:00+03:00"),
        "late": datetime.fromisoformat("2026-10-10T12:05:00+03:00"),
    }
    result = report(stats)

    assert result["total_events"] == 2
    assert result["early"] == "2026-10-10T12:00:00+03:00"
    assert result["late"] == "2026-10-10T12:05:00+03:00"




def test_save_report(tmp_path):
    data = {
        "total_events": 3,
        "levels": {"INFO": 2, "ERROR": 1},
    }
    path = tmp_path / "report.json"
    save_report(data, path)
    with path.open(encoding="utf-8") as file:
        result = json.load(file)
    assert result == data

def test_save_report_unicode(tmp_path):
    report = {
        "message": "Ошибка подключения",
         "source": "сервис",
    }
    path = tmp_path / "report.json"
    save_report(report, path)
    content = path.read_text(encoding="utf-8")
    assert "Ошибка подключения" in content
    assert "сервис" in content

    with path.open(encoding="utf-8") as file:
        result = json.load(file)
    assert result == report