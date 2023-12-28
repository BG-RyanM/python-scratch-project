from datetime import datetime, tzinfo, timedelta
from dateutil import tz

"""
Experiments with datetime
"""


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

current_dt = datetime.now()
print("current_dt is", current_dt)

for h in range(24):
    reg_h = h % 12
    if reg_h == 0:
        reg_h = 12
    am_pm = "am" if (h / 12) < 1 else "pm"
    print(f"mil hour is {h}, regular hour is {reg_h}{am_pm}")


def get_formatted_time(dt: datetime, military_time):
    if military_time:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return dt.strftime("%Y-%m-%d %I:%M:%S %p")


now = datetime.now()
print(get_formatted_time(now, False))
print(get_formatted_time(now, True))

sample_dt = datetime.strptime("2023-02-14 12:34:56.789", "%Y-%m-%d %H:%M:%S.%f")
dt_utc = sample_dt.astimezone(tz.UTC)
sample_timestamp = datetime.timestamp(sample_dt)
print("sample_dt is", sample_dt)
print("dt_utc is", dt_utc)
print("sample_timestamp is", sample_timestamp)

good_iso_string = "2012-10-12"
good_dt = datetime.fromisoformat(good_iso_string)
print("good_dt is", good_dt)
try:
    bad_iso_string = "ham sandwich"
    bad_dt = datetime.fromisoformat(bad_iso_string)
except ValueError:
    print("ham sandwich failed as expected")

utc_now = datetime.utcnow()
iso_str = utc_now.isoformat()
print("iso str is", iso_str)

z_time_str = iso_str + "+00:00"
z_dt = datetime.fromisoformat(z_time_str)
print("z_dt is", z_dt)

now_time = datetime.utcnow()
earlier_time = now_time - timedelta(seconds=5)
if now_time > earlier_time:
    print(f"{now_time} > {earlier_time}, as expected")
