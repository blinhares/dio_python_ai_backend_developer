from datetime import datetime, timezone
print(datetime.utcnow())
print(datetime.now(timezone.utc).replace(tzinfo=None))

