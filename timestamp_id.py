import datetime_test
import pytz

ct = datetime.datetime.now()
ms = ct.microsecond
print(
    "hour is {}, minute is {}, second is {}, microsecond is {}".format(
        ct.hour, ct.minute, ct.second, ms
    )
)
ms_tag = "{:06d}".format(ms % 1000000)
print("ms_tag is", ms_tag)

id = "{}{}{}{}".format(ct.hour, ct.minute, ct.second, ms_tag)
print("The ID:", id)
print("length is", len(id))

readable_str = "{}:{}:{} {}".format(id[0:2], id[2:4], id[4:6], id[6:12])
print("readable str is", readable_str)

time_stamp = (ct - datetime.datetime(2000, 1, 1)).total_seconds()
print("UNIX timestamp is", time_stamp)
