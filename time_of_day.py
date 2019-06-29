from typing import List


class TimeOfDay(object):
    def __init__(self, times_of_day: List[str], titles: List[str]):
        self.times_of_day = times_of_day
        self.titles = titles

    def __getitem__(self, item: str) -> str:
        return self.times_of_day[self.titles.index(item)]
