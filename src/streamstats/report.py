import json


def report(stats):
    res_events = {}
    for key, value in stats.items():
        if key in ["late", "early"] and value is not None:
            res_events[key] = value.isoformat()
        else:
            res_events[key] = value
    return res_events

def save_report(report_data, path_file):
    with open(path_file, "w", encoding="utf-8") as file:
        json.dump(report_data, file, ensure_ascii=False, indent=2)