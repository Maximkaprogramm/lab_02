




def analysis_events(events):
    count_levels = {
    "DEBUG": 0,
    "INFO": 0,
    "WARNING": 0,
    "ERROR": 0,
    "CRITICAL": 0
}
    total_events = 0 
    early = late = None
    count_errors_sources = {}
    count_sources = {}
    for event in events:
        total_events += 1
        count_levels[event.level] += 1
        count_sources[event.source] = count_sources.get(event.source, 0) + 1
        if early is None or event.timestamp < early:
            early = event.timestamp
        if late is None or event.timestamp > late:
            late = event.timestamp
        if event.level in ["ERROR", "CRITICAL"]:
            count_errors_sources[event.source] = count_errors_sources.get(event.source, 0) + 1
    five_errors = sorted(count_errors_sources.items(), key=lambda el: el[1], reverse=True)[:5]
    result = {
            "total_events": total_events,
            "levels": count_levels,
            "sources": count_sources,
            "five_errors": five_errors,
            "early": early,
            "late": late
            }
    return result
