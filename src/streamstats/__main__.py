import argparse
from itertools import chain

from streamstats.analysis import analysis_events
from streamstats.errors import StreamStatsError
from streamstats.parsers import read_csv, read_jsonl
from streamstats.report import report, save_report

parsers = argparse.ArgumentParser(description="Анализатор событий из JSONL и CSV")
subparsers = parsers.add_subparsers(dest="command", required=True)
analyze_pars = subparsers.add_parser("analyze", help="Анализ файлов события")
analyze_pars.add_argument("input", nargs="+")
analyze_pars.add_argument("--format", choices=("jsonl", "csv"), required=True)
analyze_pars.add_argument("--output", required=True)
analyze_pars.add_argument("--skip-invalid", action="store_true", help="Пропуск некорректных событий")
args = parsers.parse_args()
skip_dict = {"count": 0}
if args.format == "csv":
    events = (read_csv(path_file, skip_invalid=args.skip_invalid, skip_dict=skip_dict) for path_file in args.input)
elif args.format == "jsonl":
    events = (read_jsonl(path_file, skip_invalid=args.skip_invalid, skip_dict=skip_dict) for path_file in args.input)
try:
    stats = analysis_events(chain(*events))
    stats["skip_events"] = skip_dict["count"]
    res_one = report(stats)
    save_report(res_one, args.output)
except (StreamStatsError, OSError) as error:
    parsers.error(str(error))