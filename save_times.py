import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import consts
from file_utils import safe_join_path, dump_json_to_file
from get_times_from_yeshiva_site import is_year_leaped, get_times_as_titles_and_times, get_shabat_times, \
    get_start_of_months


def dump_to_file_in_cache(list_to_dump, file_name):
    file_path = safe_join_path(consts.TIMES_FOLDER_FOR_CACHE, file_name)
    dump_json_to_file(list_to_dump, file_path)


def main():
    year = 5779
    ending_year = 5900
    place_number = consts.PLACE_DICT[consts.DEFAULT_PLACE]
    titles_saved = 0

    while year <= ending_year:
        try:
            with webdriver.Chrome() as driver:
                while year <= ending_year:
                    if is_year_leaped(year):
                        months_numbers = consts.LEAP_YEAR_MONTH_NUMBERS.values()
                    else:
                        months_numbers = consts.NON_LEAP_YEAR_MONTH_NUMBERS.values()
                    for month in months_numbers:
                        time_titles, time_day_list = get_times_as_titles_and_times(month, place_number, year, driver)
                        if titles_saved < 1:
                            dump_to_file_in_cache(time_titles, consts.TIMES_DAY_TITLES_FILE)
                            titles_saved += 1
                        dump_to_file_in_cache(time_day_list, consts.TIMES_DAY_FILE_FORMAT.format(
                            place_number=place_number,
                            year_number=year,
                            month_number=month
                        ))
                        print(f'done with {month} month out of {max(months_numbers)} in {year} year')
                    shabat_titles, shabat_times_list = get_shabat_times(place_number, year, driver)

                    if titles_saved < 2:
                        dump_to_file_in_cache(shabat_titles, consts.SHABAT_SPECIAL_TIMES_TITLES_FILE)
                        titles_saved += 1
                    dump_to_file_in_cache(shabat_times_list, consts.SHABAT_SPECIAL_TIMES_FILE_FORMAT.format(
                        place_number=place_number,
                        year_number=year
                    ))

                    moladot_titles, moladot_list = get_start_of_months(year, driver)

                    if titles_saved < 3:
                        dump_to_file_in_cache(moladot_titles, consts.MOLADOT_TITLES_FILE)
                        titles_saved += 1
                    dump_to_file_in_cache(moladot_list, consts.MOLADOT_FILE_FORMAT.format(year_number=year))

                    print(f'done with {year} year')
                    year += 1
        except NoSuchElementException:
            pass


if __name__ == '__main__':
    main()
