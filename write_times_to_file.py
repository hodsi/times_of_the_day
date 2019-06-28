from datetime import datetime, timedelta
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
    return month_number - 1, year


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


def add_minutes_to_time(input_time: str, minutes_to_add: int) -> str:
    input_datetime = datetime.strptime(input_time, consts.TIME_FORMAT)
    ret_time = input_datetime + timedelta(minutes=minutes_to_add)
    return ret_time.strftime(consts.TIME_FORMAT)


def convert_plag_to_minha(plag_time: str) -> str:
    plag_datetime = datetime.strptime(plag_time, consts.TIME_FORMAT)
    ret_time = plag_datetime - timedelta(minutes=15 + plag_datetime.minute % 15)
    return ret_time.strftime(consts.TIME_FORMAT)


def calculate_minha_time(friday_times, titles):
    plag_min_time = min(get_specific_time(friday_time, titles, consts.PLAG) for friday_time in friday_times)
    return convert_plag_to_minha(plag_min_time)


def convert_by_gimatria(word: str) -> int:
    return sum(consts.GIMATRIA_DICT.get(c, 0) for c in word)


def get_fields_to_write(
        friday_time,
        shabat_time,
        times_titles,
        shabat_special_time,
        shabat_titles,
        month,
        friday_minha_time
):
    # פרשות
    yield get_specific_time(shabat_special_time, shabat_titles, consts.PARASHA)
    # תאריך עברי
    yield get_date_string(get_specific_time(shabat_time, times_titles, consts.DAY_IN_MONTH), month)
    # תאריך לועזי
    yield get_specific_time(shabat_time, times_titles, consts.WIERD_DATE)
    # מנחה של שישי
    yield friday_minha_time
    # פלג המנחה
    yield get_specific_time(friday_time, times_titles, consts.PLAG)
    # בואי כלה
    yield add_minutes_to_time(friday_minha_time, consts.COME_SHABAT_DIFF_FROM_MINHA)
    # הדלקת נרות
    yield get_specific_time(shabat_special_time, shabat_titles, consts.SHABAT_ENTER)
    # שקיעה
    yield get_specific_time(friday_time, times_titles, consts.SUN_SET)
    # שיעור בוקר שבת
    yield consts.MORNING_LESSON_TIME
    # שחרית של שבת
    yield add_minutes_to_time(consts.MORNING_LESSON_TIME, consts.MORNING_PRAYER_DIFF_FROM_LESSON)
    # סוף זמן ק"ש
    yield ' '.join([
        get_specific_time(shabat_time, times_titles, consts.FIRST_SHMA),
        get_specific_time(shabat_time, times_titles, consts.SECOND_SHMA)
    ])
    # אבות ובנים
    yield consts.FATHERS_AND_SONS_TIME
    # שיעור אחה"צ שבת
    yield add_minutes_to_time(consts.FATHERS_AND_SONS_TIME, consts.NOON_LESSON_DIFF_FROM_FATHERS_AND_SONS)
    # מנחה של שבת
    yield add_minutes_to_time(
        get_specific_time(shabat_time, times_titles, consts.SUN_SET),
        -consts.MINHA_TIME_BEFORE_SUN_SET
    )
    # צאת שבת רש"י
    yield get_specific_time(shabat_special_time, shabat_titles, consts.SHABAT_END)
    # צאת שבת ר"ת
    yield consts.FIELD_TO_FILL


def main(place=consts.DEFAULT_PLACE, month=consts.DEFAULT_MONTH, year=consts.DEFAULT_YEAR):
    place = place or input('what place do you want to save the times of? ').strip()
    month = month or input("what month's times? ").strip()
    year = year or (5000 + convert_by_gimatria(input("what year's times? ")))

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

    friday_minha_time = calculate_minha_time(friday_times, times_titles)
    lines_to_write = []
    for i in range(len(shabat_times)):
        lines_to_write.append(consts.SEP.join(get_fields_to_write(
            friday_times[i],
            shabat_times[i],
            times_titles,
            shabat_special_times[i],
            shabat_titles,
            month,
            friday_minha_time
        )))

    with open(consts.TIMES_OUTPUT_FILE_FORMAT.format(month=month), 'w') as f:
        f.write('\n'.join(lines_to_write))


if __name__ == '__main__':
    main()
