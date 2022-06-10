from datetime import datetime, tzinfo
from dateutil import tz

def run_test():
    utc_datetime = datetime.utcnow()
    # Get local timezone
    local_zone = tz.tzlocal()
    # Convert timezone of datetime from UTC to local
    dt_local = utc_datetime.astimezone(local_zone)
    local_tzname = local_zone.tzname(dt_local)
    print(f"local time is: {dt_local}, tz is {local_tzname}")

    dt_now_regular = datetime.now()
    print(f"local time 2 is: {dt_now_regular}")


run_test()