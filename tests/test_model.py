from datetime import datetime

from streamstats.models import LogEvent

event = LogEvent(
    timestamp=datetime.now(),
    level="INFO",
    source="auth",
    message="User logged in"
)

print(event.level)
print(event.source)
print(event.message)