import time
from typing import Dict, Any, Optional
from collections import namedtuple, OrderedDict
from datetime import datetime

dumb = ["Org Chart", "Org Chart", "Org Chart"]
for d in dumb:
    print(f"hash of {d} is {int(hash(d))}")
print("hash of '6' is", hash("6"))

Point = namedtuple("Point", ["x", "y"])
point = Point(2, 4)
print(f"point is {point}, x is {point.x}")
new_point = point._replace(x=3, y=5)
print(f"new_point is {new_point}")


class LogDespammer:
    """
    Class for logging spammy messages. The idea is that a particular message will be displayed on
    the first logging call, but subsequent calls won't display the message unless some amount of
    time has passed since the last display or the call has been made some number of times.
    """

    instance = None
    Entry = namedtuple(
        "Entry",
        [
            "string",
            "id",
            "time_window",
            "silent_repetitions",
            "last_dt",
            "unprinted_count",
        ],
    )

    def __init__(self):
        # Dict[int, LogDespammer.Entry]
        self._line_lookup: OrderedDict = OrderedDict()
        self._num_entries = 0
        self._max_entries = 500

    @staticmethod
    def get_despammer():
        if not LogDespammer.instance:
            LogDespammer.instance = LogDespammer()
        return LogDespammer.instance

    def print(
        self,
        line: str,
        id: Optional[str] = None,
        time_window: Optional[float] = None,
        silent_repetitions: Optional[int] = None,
    ) -> str:
        """
        Logs the line, if permissible. Also sets values specifying when the line may be logged again,
        either after a certain amount of time has elapsed or a certain number of repetitions.

        Each line logged through this method has a unique ID. Normally, the ID is a hash of the line
        itself, but if an ID is explicitly given, this allows lines with different content to be
        treated as the same, e.g.:
            'current time is 1:01:35'
            'current time is 1:01:37'
            'current time is 1:01:39'

        The above can be done with print(current_time_str, id="current time", silent_repetitions=100)

        :param line: the actual line to log
        :param id: if not None, the ID as described above
        :param time_window: this number of seconds must pass before the line can be printed again.
            If not set, then the value passed in an earlier call, if any, is used.
        :param silent_repetitions: if set, only one in every N instances of the line is logged.
            If not set, then the value passed in an earlier call, if any, is used. If both time_window
            and silent_repetitions are set, the logging depends on which expires first.
        :return:
        """
        hash_val = hash(id) if id else hash(line)
        entry = self._line_lookup.get(hash_val)
        time_now = datetime.utcnow()
        if not entry:
            self._line_lookup[hash_val] = entry = self._make_new_entry(
                line, hash_val, time_window, silent_repetitions, time_now
            )
        time_diff = (time_now - entry.last_dt).total_seconds()
        if (
            time_diff == 0.0
            or time_diff > entry.time_window
            or entry.unprinted_count >= entry.silent_repetitions
        ):
            rep_count_str = (
                f" [{entry.unprinted_count} unprinted repetitions]"
                if entry.unprinted_count > 0
                else ""
            )
            print(f"{line}{rep_count_str}")
            self._line_lookup[hash_val] = entry._replace(
                last_dt=time_now, unprinted_count=0
            )
        else:
            new_rep_count = entry.unprinted_count + 1
            self._line_lookup[hash_val] = entry._replace(unprinted_count=new_rep_count)
        return hash_val

    def _make_new_entry(
        self, line, hash_val, time_window, silent_repetitions, time_now
    ):
        while self._num_entries >= self._max_entries:
            self._line_lookup.popitem()
            self._num_entries -= 1

        if time_window is None and silent_repetitions is None:
            time_window = 0
            silent_repetitions = 1000000
        else:
            if time_window is None:
                time_window = 1000000.0
            if silent_repetitions is None:
                silent_repetitions = 1000000

        self._num_entries -= 1
        return LogDespammer.Entry(
            string=line,
            id=hash_val,
            time_window=time_window,
            silent_repetitions=silent_repetitions,
            last_dt=time_now,
            unprinted_count=0,
        )


log_despammer = LogDespammer.get_despammer()

# Timer test
for i in range(12):
    log_despammer.print("timer test", time_window=10.0)
    time.sleep(1.0)

# Counter test
for i in range(101):
    log_despammer.print("counter test", silent_repetitions=99)

# ID test
id = None
for i in range(100):
    id = log_despammer.print(f"ID test {i}", id=id, silent_repetitions=9)
