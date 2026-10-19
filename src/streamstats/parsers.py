import csv
import json
import logging
from datetime import datetime
from pathlib import Path

from streamstats.errors import InvalidEventError, InvalidTimestampError
from streamstats.models import LogEvent

logger = logging.getLogger(__name__)
def parse_events(row):
    if not isinstance(row, dict):
        raise InvalidEventError("Событие не объект типа dict")

    correct_keys = ["timestamp", "level", "source", "message"]
    for key in correct_keys:
        if key not in row:
            raise InvalidEventError(f"Некорректное поле {key}")

    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    try:
        if isinstance(row["timestamp"], str):
            timestamp = datetime.fromisoformat(row["timestamp"])
        else:
            raise InvalidTimestampError("Некорректная дата события")
    except ValueError:
        raise InvalidTimestampError("Некорректная дата события")

    if not isinstance(row["level"], str) or row["level"] not in levels:
        raise InvalidEventError("Некорректный уровень")
    
    if not isinstance(row["source"], str) or not row["source"].strip():
        raise InvalidEventError("Некорректный источник")
  

    if not isinstance(row["message"], str):
        raise InvalidEventError("Некорректное сообщение")

    obj_log_event = LogEvent(timestamp, row["level"], row["source"], row["message"])
    return obj_log_event




def read_csv(path, skip_invalid=False, skip_dict=None):
    if skip_dict is None:
        skip_dict = {"count": 0}
    with Path(path).open(encoding="utf-8", newline="") as file:
        dict_reader = csv.DictReader(file)
        for number_str, row in enumerate(dict_reader, start=2):
            try:
                res = parse_events(row)
            except InvalidEventError as error:
                if skip_invalid is True:
                    logger.warning(
                        "Файл %s, строка %s: событие пропущено: %s",
                        path,
                        number_str,
                        error
                    )
                    skip_dict["count"] += 1
                    continue
                raise InvalidEventError(f"Файл {path}, строка {number_str}: {error}") from error
            except InvalidTimestampError as error:
                if skip_invalid is True:
                    logger.warning(
                        "Файл %s, строка %s: событие пропущено: %s",
                        path,
                        number_str,
                        error
                    )
                    skip_dict["count"] += 1
                    continue
                raise InvalidTimestampError(f"Файл {path}, строка {number_str}: {error}") from error
            yield res




def read_jsonl(path, skip_invalid=False, skip_dict=None):
    if skip_dict is None:
        skip_dict = {"count": 0}
    with Path(path).open(encoding="utf-8", newline="") as file:
        for number_str, string in enumerate(file, start=1):
            try:
                res_event = parse_events(json.loads(string))
            except InvalidEventError as error:
                if skip_invalid is True:
                    logger.warning(
                        "Файл %s, строка %s: событие пропущено: %s",
                        path,
                        number_str,
                        error
                    )
                    skip_dict["count"] += 1
                    continue
                raise InvalidEventError(f"Файл {path}, строка {number_str}: {error}") from error
            except InvalidTimestampError as error:
                if skip_invalid is True:
                    logger.warning(
                        "Файл %s, строка %s: событие пропущено: %s",
                        path,
                        number_str,
                        error
                    )
                    skip_dict["count"] += 1
                    continue
                raise InvalidTimestampError(f"Файл {path}, строка {number_str}: {error}") from error
            except json.JSONDecodeError as error:
                if skip_invalid is True:
                    logger.warning(
                        "Файл %s, строка %s: событие пропущено: %s",
                        path,
                        number_str,
                        error
                    )
                    skip_dict["count"] += 1
                    continue
                raise InvalidEventError(f"Файл {path}, строка {number_str}: некорректный формат JSON") from error
            yield res_event