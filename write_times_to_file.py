from datetime import datetime, timedelta
from typing import List, Tuple

from selenium import webdriver

import consts
from get_times_from_yeshiva_site import get_times_as_titles_and_times, convert_month_to_month_number, is_year_leaped, \
    get_shabat_times, convert_to_time_of_day, get_start_of_months
from time_of_day import TimeOfDay


def get_specific_day_times(day_to_extract: str, time_of_days: List[TimeOfDay]) -> List[TimeOfDay]:
    return [day_times for day_times in time_of_days if day_times[consts.DAY_IN_WEEK] == day_to_extract]


def get_last_month(month_number: int, year_number: int) -> Tuple[int, int]:
    if month_number == min(consts.LEAP_YEAR_MONTH_NUMBERS.values()):
        if is_year_leaped(year_number):
            return max(consts.LEAP_YEAR_MONTH_NUMBERS.values()), year_number - 1
        return max(consts.NON_LEAP_YEAR_MONTH_NUMBERS.values()), year_number - 1
    return month_number - 1, year_number


def get_next_month(month_number: int, year_number: int) -> Tuple[int, int]:
    if is_year_leaped(year_number):
        if month_number == len(consts.LEAP_YEAR_MONTH_NUMBERS):
            return min(consts.LEAP_YEAR_MONTH_NUMBERS.values()), year_number + 1
        return month_number + 1, year_number
    if month_number == len(consts.NON_LEAP_YEAR_MONTH_NUMBERS):
        return min(consts.NON_LEAP_YEAR_MONTH_NUMBERS.values()), year_number + 1
    return month_number + 1, year_number


def reverse_dict(dict_to_reverse: dict) -> dict:
    return {value: key for key, value in dict_to_reverse.items()}


def calculate_month_name(month_number: int, year_number: int) -> str:
    if is_year_leaped(year_number):
        return reverse_dict(consts.LEAP_YEAR_MONTH_NUMBERS)[month_number]
    return reverse_dict(consts.NON_LEAP_YEAR_MONTH_NUMBERS)[month_number]


def put_quotes(un_quoted: str) -> str:
    if len(un_quoted) == 1:
        return un_quoted + "'"
    return un_quoted[:-1] + '"' + un_quoted[-1]


def get_date_string(day_in_month: str, month: str) -> str:
    return put_quotes(day_in_month) + ' ב' + month


def is_shabat_in_month(shabat_times: TimeOfDay, month: str) -> bool:
    shabat_date = shabat_times[consts.DATE]
    if month in ['חשון', 'סיון']:
        month = month.replace('ו', 'וו')
    return consts.SHABAT in shabat_date and month in shabat_date


def is_moladot_time_in_month(moladot_time: TimeOfDay, month: str) -> bool:
    return month == moladot_time[consts.HEBREW_MONTH]


def add_minutes_to_time(input_time: str, minutes_to_add: int) -> str:
    input_datetime = datetime.strptime(input_time, consts.TIME_FORMAT)
    ret_time = input_datetime + timedelta(minutes=minutes_to_add)
    return ret_time.strftime(consts.TIME_FORMAT)


def convert_plag_to_minha(plag_time: str) -> str:
    plag_datetime = datetime.strptime(plag_time, consts.TIME_FORMAT)
    ret_time = plag_datetime - timedelta(minutes=15 + plag_datetime.minute % 15)
    return ret_time.strftime(consts.TIME_FORMAT)


def calculate_minha_time(friday_times: List[TimeOfDay]) -> str:
    plag_min_time = min(friday_time[consts.PLAG] for friday_time in friday_times)
    return convert_plag_to_minha(plag_min_time)


def convert_to_good_date_format(date_format: str) -> str:
    words = date_format.split()
    words[1] = words[1].replace(',', '')
    return words[0] + ' ' + words[1] + ' ' + words[2] + words[3] + ' ' + words[4]


def calculate_moladot_of_month(month_moladot: TimeOfDay) -> str:
    lines = month_moladot[consts.MOLADOT_TIME].splitlines(keepends=False)
    lines[consts.GOOD_DATE_FORMAT_LINE] = convert_to_good_date_format(lines[consts.GOOD_DATE_FORMAT_LINE])
    del lines[consts.BAD_DATE_FORMAT_LINE]
    return ' '.join(lines)


def convert_by_gimatria(word: str) -> int:
    return sum(consts.GIMATRIA_DICT.get(c, 0) for c in word)


def get_year_from_number(year_number: int) -> str:
    year = ''
    for gimatria_of_letter in sorted(consts.REVERSE_GIMATRIAA_DICT, reverse=True):
        while year_number >= gimatria_of_letter:
            year += consts.REVERSE_GIMATRIAA_DICT[gimatria_of_letter]
            year_number -= gimatria_of_letter
    return year


def get_fields_to_write(friday_time, shabat_time, shabat_special_time, month, friday_minha_time):
    # פרשות
    yield shabat_special_time[consts.PARASHA]
    # תאריך עברי
    yield get_date_string(shabat_time[consts.DAY_IN_MONTH], month)
    # תאריך לועזי
    yield shabat_time[consts.WEIRD_DATE]
    # מנחה של שישי
    yield friday_minha_time
    # פלג המנחה
    yield friday_time[consts.PLAG]
    # בואי כלה
    yield add_minutes_to_time(friday_minha_time, consts.COME_SHABAT_DIFF_FROM_MINHA)
    # הדלקת נרות
    yield shabat_special_time[consts.SHABAT_ENTER]
    # שקיעה
    yield friday_time[consts.SUN_SET]
    # שיעור בוקר שבת
    yield consts.MORNING_LESSON_TIME
    # שחרית של שבת
    yield add_minutes_to_time(consts.MORNING_LESSON_TIME, consts.MORNING_PRAYER_DIFF_FROM_LESSON)
    # סוף זמן ק"ש
    yield ' '.join([shabat_time[consts.FIRST_SHMA], shabat_time[consts.SECOND_SHMA]])
    # אבות ובנים
    yield consts.FATHERS_AND_SONS_TIME
    # שיעור אחה"צ שבת
    yield add_minutes_to_time(consts.FATHERS_AND_SONS_TIME, consts.NOON_LESSON_DIFF_FROM_FATHERS_AND_SONS)
    # מנחה של שבת
    yield add_minutes_to_time(shabat_time[consts.SUN_SET], -consts.MINHA_TIME_BEFORE_SUN_SET)
    # צאת שבת רש"י
    yield shabat_special_time[consts.SHABAT_END]
    # צאת שבת ר"ת
    yield consts.FIELD_TO_FILL


def main(place=consts.DEFAULT_PLACE, month=consts.DEFAULT_MONTH, year_number=consts.DEFAULT_YEAR):
    place = place or input('what place do you want to save the times of? ').strip()
    month = month or input("what month's times? ").strip()
    year_number = year_number or (consts.THOUSANDS_OF_YEARS_OFFSET + convert_by_gimatria(input("what year's times? ")))
    year = get_year_from_number(year_number - consts.THOUSANDS_OF_YEARS_OFFSET)

    month_number = convert_month_to_month_number(month, year_number)
    next_month_number, next_months_year = get_next_month(month_number, year_number)
    next_month = calculate_month_name(next_month_number, next_months_year)
    place_number = consts.PLACE_DICT[place]

    with webdriver.Chrome() as driver:
        time_day_list = convert_to_time_of_day(*get_times_as_titles_and_times(
            month_number,
            place_number,
            year_number,
            driver
        ))
        shabat_times_list = convert_to_time_of_day(*get_shabat_times(place_number, year_number, driver))
        moladot_list = convert_to_time_of_day(*get_start_of_months(year_number, driver))
    shabat_special_times = [one_shabat_times for one_shabat_times in shabat_times_list if is_shabat_in_month(
        one_shabat_times,
        month
    )]
    month_moladot, = [one_moladot for one_moladot in moladot_list if is_moladot_time_in_month(one_moladot, next_month)]

    shabat_times = get_specific_day_times(consts.SHABAT, time_day_list)
    friday_times = get_specific_day_times(consts.FRIDAY, time_day_list)

    if len(shabat_times) > len(friday_times):
        last_month_number, last_months_year = get_last_month(month_number, year_number)
        last_month_times = convert_to_time_of_day(*get_times_as_titles_and_times(
            last_month_number,
            place_number,
            last_months_year
        ))
        last_month_friday_times = get_specific_day_times(consts.FRIDAY, last_month_times)
        friday_times = [last_month_friday_times[-1], *friday_times]

    if not len(shabat_times) == len(shabat_special_times) == len(friday_times):
        raise Exception(
            f'shabat_times_len == {len(shabat_times)}, shabat_special_times_len == {len(shabat_special_times)}, ' +
            f'friday_times_len == {len(friday_times)}'
        )

    friday_minha_time = calculate_minha_time(friday_times)
    lines_to_write = []
    for i in range(len(shabat_times)):
        lines_to_write.append(consts.SEP.join(get_fields_to_write(
            friday_times[i],
            shabat_times[i],
            shabat_special_times[i],
            month,
            friday_minha_time
        )))

    lines_to_write.append(calculate_moladot_of_month(month_moladot))

    with open(consts.TIMES_OUTPUT_FILE_FORMAT.format(month=month, year=year), 'w') as f:
        f.write('\n'.join(lines_to_write))


if __name__ == '__main__':
    main()
