from datetime import datetime

current_datetime = datetime.now()

print(f'{current_datetime.strftime("%d/%b/%Y")} at {current_datetime.strftime("%d %b %Y, %H:%M:%S")}')