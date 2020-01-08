from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import Union, List

import consts

MINUTES_IN_HOUR = 60
HOURS_IN_DAY = 24


class TimeOfDay(object):
    def __init__(self, times_of_day: List[str], titles: List[str]):
        self.times_of_day = times_of_day
        self.titles = titles

    def __getitem__(self, item: str) -> str:
        return self.times_of_day[self.titles.index(item)]


class Time(object):
    def __init__(self, time_representer: Union[int, str, datetime, time, Time]):
        self._total_minutes = None
        if isinstance(time_representer, str):
            time_representer = datetime.strptime(time_representer, consts.TIME_FORMAT)
        if isinstance(time_representer, (datetime, time)):
            self._total_minutes = time_representer.hour * MINUTES_IN_HOUR + time_representer.minute
        if isinstance(time_representer, int):
            self._total_minutes = time_representer % (HOURS_IN_DAY * MINUTES_IN_HOUR)
        if isinstance(time_representer, Time):
            self._total_minutes = time_representer._total_minutes
        if self._total_minutes is None:
            raise NotImplementedError

    def __str__(self):
        temp_datetime = datetime(1970, 1, 1)
        temp_datetime += timedelta(minutes=self._total_minutes)
        return temp_datetime.strftime(consts.TIME_FORMAT)

    def __repr__(self):
        return f"{self.__class__.__name__}('{str(self)}')"

    def __iadd__(self, other: Union[int, str, datetime, time, Time]):
        if not isinstance(other, Time) and isinstance(other, (int, str, datetime, time)):
            self.__iadd__(Time(other))
        elif isinstance(other, Time):
            self._total_minutes += other._total_minutes
            self._total_minutes %= HOURS_IN_DAY * MINUTES_IN_HOUR
        else:
            raise NotImplementedError
        return self

    def __add__(self, other: Union[int, str, datetime, time, Time]):
        temp = Time(self)
        temp += other
        return temp

    def __radd__(self, other):
        return Time(other) + self

    def __isub__(self, other: Union[int, str, datetime, time, Time]):
        if not isinstance(other, Time) and isinstance(other, (int, str, datetime, time)):
            self.__isub__(Time(other))
        elif isinstance(other, Time):
            self._total_minutes -= other._total_minutes
            self._total_minutes %= HOURS_IN_DAY * MINUTES_IN_HOUR
        else:
            raise NotImplementedError
        return self

    def __sub__(self, other: Union[int, str, datetime, time, Time]):
        temp_time = Time(self)
        temp_time -= other
        return temp_time

    def __rsub__(self, other: Union[int, str, datetime, time, Time]):
        return Time(other) - self

    def __ifloordiv__(self, other: int):
        if not isinstance(other, int):
            raise NotImplementedError
        self._total_minutes //= other
        return self

    def __floordiv__(self, other: int):
        if not isinstance(other, int):
            raise NotImplementedError
        return Time(self._total_minutes // other)

    def __imod__(self, other: int):
        if not isinstance(other, int):
            raise NotImplementedError
        self._total_minutes %= other
        return self

    def __mod__(self, other):
        if not isinstance(other, int):
            raise NotImplementedError
        return Time(self._total_minutes % other)

    def __imul__(self, other: int):
        if not isinstance(other, int):
            raise NotImplementedError
        self._total_minutes *= other
        return self

    def __mul__(self, other: int):
        if not isinstance(other, int):
            raise NotImplementedError
        return Time(self._total_minutes * other)

    def __neg__(self):
        return Time(0) - self

    def __pos__(self):
        return self

    def __int__(self):
        return self._total_minutes

    def __lt__(self, other: Time):
        if not isinstance(other, Time):
            raise NotImplementedError
        return self._total_minutes < other._total_minutes

    def __le__(self, other: Time):
        if not isinstance(other, Time):
            raise NotImplementedError
        return self._total_minutes <= other._total_minutes

    def __eq__(self, other: Time):
        if not isinstance(other, Time):
            raise NotImplementedError
        return self._total_minutes == other._total_minutes

    def __ne__(self, other: Time):
        if not isinstance(other, Time):
            raise NotImplementedError
        return self._total_minutes != other._total_minutes

    def __ge__(self, other: Time):
        if not isinstance(other, Time):
            raise NotImplementedError
        return self._total_minutes >= other._total_minutes

    def __gt__(self, other: Time):
        if not isinstance(other, Time):
            raise NotImplementedError
        return self._total_minutes > other._total_minutes

    @property
    def minutes(self):
        return self._total_minutes % MINUTES_IN_HOUR

    @property
    def hours(self):
        return self._total_minutes // MINUTES_IN_HOUR
