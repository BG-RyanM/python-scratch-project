from datetime import datetime, tzinfo, timedelta
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

some_time = datetime.utcnow()
if some_time is None:
    print("sometime is None")
nonset_dt = datetime.min
if nonset_dt == datetime.min:
    print("nonset worked correctly")
set_dt: datetime = datetime.utcnow()
if set_dt > datetime.min:
    print("set worked correctly")

new_time = some_time - timedelta(milliseconds=float(1000.0 / 60.0))
print("new_time is", new_time, "some_time is", some_time)

some_dates = []
for i in range(5):
    dt = some_time - timedelta(days=i)
    some_dates.append(dt)

some_dates.sort()
print(some_dates)
