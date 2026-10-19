from datetime import datetime


class LogEvent:
    def __init__(
        self,
        timestamp: datetime,
        level: str,
        source: str,
        message: str
    ):
        self.timestamp = timestamp
        self.level = level
        self.source = source
        self.message = message