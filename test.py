from datetime import datetime, timezone
utc = datetime.now(timezone.utc)
print(utc)
local = utc.replace(tzinfo=None)
formatted = local.strftime('%a %d %b %Y, %I:%M%p')
print(local)