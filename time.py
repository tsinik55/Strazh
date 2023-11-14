from datetime import datetime, date, timezone
import time

print(1698657437000)
print(datetime(*date.today().timetuple()[:6], tzinfo=timezone.utc).timestamp())
print(datetime.now())
print(f'{int(time.mktime(datetime.now().timetuple()))}000')

