class StreamStatsError(Exception):
    pass

class InvalidTimestampError(StreamStatsError):
    pass

class InvalidEventError(StreamStatsError):
    pass

class InvalidFormatError(StreamStatsError):
    pass

class CLIConfigError(StreamStatsError):
    pass