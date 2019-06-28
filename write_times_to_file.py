from datetime import datetime
from typing import List, Tuple

import consts
from get_times_from_yeshiva_site import get_times_as_titles_and_times, convert_month_to_month_number, is_year_leaped, \
    get_shabat_times


def get_specific_day_times(day_to_extract, day_index: int, time_of_days: List[List[str]]) -> List[List[str]]:
    return [day_times for day_times in time_of_days if day_times[day_index] == day_to_extract]


def get_last_month(month_number: int, year: int) -> Tuple[int, int]:
    if month_number == 1:
        if is_year_leaped(year):
            return max(consts.LEAP_YEAR_MONTH_NUMBERS.values()), year - 1
        return max(consts.NON_LEAP_YEAR_MONTH_NUMBERS.values()), year - 1
    return month_number - 1, year - 1


def put_quotes(un_quoted: str) -> str:
    if len(un_quoted) == 1:
        return un_quoted + "'"
    return un_quoted[:-1] + '"' + un_quoted[-1]


def get_date_string(day_in_month: str, month: str) -> str:
    return put_quotes(day_in_month) + ' ב' + month


def get_specific_time(times: List[str], titles: List[str], title: str) -> str:
    return times[titles.index(title)]


def is_shabat_in_month(shabat_times: List[str], titles: List[str], month: str) -> bool:
    shabat_date = get_specific_time(shabat_times, titles, consts.DATE)
    if month in ['חשון', 'סיון']:
        month = month.replace('ו', 'וו')
    return consts.SHABAT in shabat_date and month in shabat_date


def calculate_minha_time(sun_set_time: str) -> str:
    sun_set_datetime = datetime.strptime(sun_set_time, consts.TIME_FORMAT)
    minha_time = sun_set_datetime - datetime.strptime('40', consts.MINUTES_FORMAT)
    return str(minha_time)[:-3]


def convert_by_gimatria(word: str) -> int:
    return sum(consts.GIMATRIA_DICT.get(c, 0) for c in word)


def main():
    place = input('what place do you want to save the times of? ').strip()
    month = input("what month's times? ").strip()
    year = 5000 + convert_by_gimatria(input("what year's times? "))

    month_number = convert_month_to_month_number(month, year)
    place_number = consts.PLACE_DICT[place]

    times_titles, time_of_days = get_times_as_titles_and_times(month_number, place_number, year)
    shabat_titles, shabat_of_year_times = get_shabat_times(place_number, year)
    shabat_special_times = [one_shabat_times for one_shabat_times in shabat_of_year_times if is_shabat_in_month(
        one_shabat_times,
        shabat_titles,
        month
    )]

    shabat_times = get_specific_day_times(consts.SHABAT, times_titles.index(consts.DAY_IN_WEEK), time_of_days)
    friday_times = get_specific_day_times(consts.FRIDAY, times_titles.index(consts.DAY_IN_WEEK), time_of_days)

    if len(shabat_times) > len(friday_times):
        last_month_number, last_months_year = get_last_month(month_number, year)
        _, last_month_times = get_times_as_titles_and_times(last_month_number, place_number, last_months_year)
        last_month_friday_times = get_specific_day_times(consts.FRIDAY, times_titles.index(consts.DAY_IN_WEEK),
                                                         last_month_times)
        friday_times = [last_month_friday_times[-1], *friday_times]

    if not len(shabat_times) == len(shabat_special_times) == len(friday_times):
        raise Exception(
            f'shabat_times_len == {len(shabat_times)}, shabat_special_times_len == {len(shabat_special_times)}, ' +
            f'friday_times_len == {len(friday_times)}'
        )

    with open('זמני שבת.csv', 'w') as f:
        for i in range(len(shabat_times)):
            # פרשות
            f.write(get_specific_time(shabat_special_times[i], shabat_titles, consts.PARASHA) + consts.SEP)
            # תאריך עברי
            f.write(get_date_string(
                get_specific_time(shabat_times[i], times_titles, consts.DAY_IN_MONTH),
                month
            ) + consts.SEP)
            # תאריך לועזי
            f.write(get_specific_time(shabat_times[i], times_titles, consts.WIERD_DATE) + consts.SEP)
            # מנחה של שישי
            f.write(consts.FRIDAY_MINHA_TIME + consts.SEP)
            # פלג המנחה
            f.write(get_specific_time(friday_times[i], times_titles, consts.PLAG) + consts.SEP)
            # בואי כלה
            f.write(consts.COME_SHABAT_TIME + consts.SEP)
            # הדלקת נרות
            f.write(get_specific_time(shabat_special_times[i], shabat_titles, consts.SHABAT_ENTER) + consts.SEP)
            # שקיעה
            f.write(get_specific_time(friday_times[i], times_titles, consts.SUN_DOWN) + consts.SEP)
            # שיעור בוקר שבת
            f.write(consts.MORNING_LESSON_TIME + consts.SEP)
            # שחרית של שבת
            f.write(consts.MORNING_PRAYER_TIME + consts.SEP)

            # סוף זמן ק"ש
            f.write(get_specific_time(shabat_times[i], times_titles, consts.FIRST_SHMA) + ' ')
            f.write(get_specific_time(shabat_times[i], times_titles, consts.SECOND_SHMA) + consts.SEP)

            # אבות ובנים
            f.write(consts.FATHERS_AND_SONS_TIME + consts.SEP)
            # שיעור אחה"צ שבת
            f.write(consts.NOON_LESSON_TIME + consts.SEP)
            # מנחה של שבת
            f.write(calculate_minha_time(
                get_specific_time(shabat_times[i], times_titles, consts.SUN_DOWN)
            ) + consts.SEP)
            # צאת שבת רש"י
            f.write(get_specific_time(shabat_special_times[i], shabat_titles, consts.SHABAT_END) + consts.SEP)
            # צאת שבת ר"ת
            f.write(consts.FIELD_TO_FILL + consts.SEP)

            f.write('\n')


if __name__ == '__main__':
    main()
