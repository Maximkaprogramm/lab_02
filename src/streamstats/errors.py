class StreamStatsError(Exception):
    pass

class InvalidTimestampError(StreamStatsError):
    pass

class InvalidEventError(StreamStatsError):
    pass

class UnsupportedFormatError(StreamStatsError):
    pass

class CLIConfigError(StreamStatsError):
    pass