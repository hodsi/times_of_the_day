import json
import os

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import consts
from get_times_from_yeshiva_site import is_year_leaped, get_times_as_titles_and_times, get_shabat_times


def safe_join_path(path: str, *paths: str):
    joined_path = path
    for path_to_join in paths:
        if not os.path.isdir(joined_path):
            os.mkdir(joined_path)
        joined_path = os.path.join(joined_path, path_to_join)
    return joined_path


def main():
    year = 5779
    ending_year = 5900
    while year <= ending_year:
        try:
            with webdriver.Chrome() as driver:
                while year <= ending_year:
                    if is_year_leaped(year):
                        months_numbers = consts.LEAP_YEAR_MONTH_NUMBERS.values()
                    else:
                        months_numbers = consts.NON_LEAP_YEAR_MONTH_NUMBERS.values()
                    place_number = consts.PLACE_DICT[consts.DEFAULT_PLACE]
                    for month in months_numbers:
                        _, time_day_list = get_times_as_titles_and_times(month, place_number, year, driver)
                        file_path = safe_join_path(consts.TIMES_FOLDER_FOR_CACHE, consts.TIMES_DAY_FILE_FORMAT.format(
                            place_number=place_number,
                            year_number=year,
                            month_number=month
                        ))
                        with open(file_path, 'w') as f:
                            json.dump(time_day_list, f)
                        print(f'done with {month} month out of {max(months_numbers)} in {year} year')
                    _, shabat_times_list = get_shabat_times(place_number, year, driver)
                    file_path = safe_join_path(consts.TIMES_FOLDER_FOR_CACHE, consts.SHABAT_SPECIAL_TIMES_FILE_FORMAT.format(
                        place_number=place_number,
                        year_number=year
                    ))
                    with open(file_path, 'w') as f:
                        json.dump(shabat_times_list, f)
                    print(f'done with {year} year')
                    year += 1
        except NoSuchElementException:
            pass


if __name__ == '__main__':
    main()
