import json
import subprocess
import sys


def test_multiple_csv(tmp_path):
    file1 = tmp_path / "first.csv"
    file2 = tmp_path / "second.csv"
    output = tmp_path / "report.json"

    file1.write_text(
        "timestamp,level,source,message\n"
        "2026-10-10T12:00:00+03:00,INFO,auth,User logged in\n",
        encoding="utf-8"
    )

    file2.write_text(
        "timestamp,level,source,message\n"
        "2026-10-10T12:01:00+03:00,ERROR,payments,Payment failed\n",
        encoding="utf-8"
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(file1),
            str(file2),
            "--format",
            "csv",
            "--output",
            str(output)
        ],
        capture_output=True,
        text=True,
        check=False
    )

    assert result.returncode == 0
    assert output.exists()

    with open(output, encoding="utf-8") as file:
        report = json.load(file)

    assert report["total_events"] == 2
    assert report["levels"]["INFO"] == 1
    assert report["levels"]["ERROR"] == 1
    assert report["sources"]["auth"] == 1
    assert report["sources"]["payments"] == 1


def test_invalid_event(tmp_path):
    input_file = tmp_path / "bad.csv"
    output = tmp_path / "report.json"

    input_file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-10T12:00:00+03:00,UNKNOWN,auth,User logged in\n",
        encoding="utf-8"
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(input_file),
            "--format",
            "csv",
            "--output",
            str(output)
        ],
        capture_output=True,
        text=True,
        check=False
    )
    assert "bad.csv" in result.stderr
    assert "2" in result.stderr
    assert result.returncode == 2
    assert "Некорректный уровень" in result.stderr

def test_skip_invalid(tmp_path):
    input_file = tmp_path / "events.csv"
    output_file = tmp_path / "report.json"

    input_file.write_text(
        "timestamp,level,source,message\n"
        "2026-10-14T10:00:00+00:00,INFO,auth,User logged in\n"
        "2026-10-14T11:01:00+00:00,UNKNOWN,payments,Payment failed\n"
        "2026-10-14T12:02:00+00:00,ERROR,database,Connection lost\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(input_file),
            "--format",
            "csv",
            "--output",
            str(output_file),
            "--skip-invalid",
        ],
        capture_output=True,
        text=True,
        check=False
    )

    assert result.returncode == 0
    assert output_file.exists()

    with open(output_file, encoding="utf-8") as file:
        report = json.load(file)

    assert report["total_events"] == 2
    assert report["levels"]["ERROR"] == 1
    assert report["sources"]["database"] == 1
    assert report["skip_events"] == 1

def test_empty_file(tmp_path):
    input_file = tmp_path / "empty.csv"
    output_file = tmp_path / "report.json"

    input_file.write_text(
        "timestamp,level,source,message\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(input_file),
            "--format",
            "csv",
            "--output",
            str(output_file),
        ],
        capture_output=True,
        text=True,
        check=False
    )

    assert result.returncode == 0
    assert output_file.exists()

    with open(output_file, encoding="utf-8") as file:
        report = json.load(file)

    assert report["total_events"] == 0
    assert report["skip_events"] == 0

def test_jsonl(tmp_path):
    input_file = tmp_path / "events.jsonl"
    output_file = tmp_path / "report.json"

    input_file.write_text(
        '{"timestamp": "2026-10-14T10:00:00+01:00", "level": "INFO", '
        '"source": "auth", "message": "User logged in"}\n'
        '{"timestamp": "2026-10-14T10:01:00+07:25", "level": "ERROR", '
        '"source": "payments", "message": "Payment failed"}\n',
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(input_file),
            "--format",
            "jsonl",
            "--output",
            str(output_file),
        ],
        capture_output=True,
        text=True,
        check=False
    )

    assert result.returncode == 0
    assert output_file.exists()

    with open(output_file, encoding="utf-8") as file:
        report = json.load(file)

    assert report["total_events"] == 2
    assert report["levels"]["INFO"] == 1
    assert report["levels"]["ERROR"] == 1
    assert report["sources"]["auth"] == 1
    assert report["sources"]["payments"] == 1