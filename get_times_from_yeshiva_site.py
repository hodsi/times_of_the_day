import json
import os
from typing import List, Tuple

from cachetools.func import lru_cache
from selenium import webdriver

import consts
from time_of_day import TimeOfDay


def load_json_from_file(file_path):
    full_file_path = os.path.join(consts.TIMES_FOLDER_FOR_CACHE, file_path)
    if os.path.isfile(full_file_path):
        with open(full_file_path) as f:
            return json.load(f)


@lru_cache(maxsize=10)
def get_times_as_titles_and_times(
        month_number: int,
        place_number: int,
        year: int,
        driver=None
) -> Tuple[List[str], List[List[str]]]:
    times_day_titles = load_json_from_file(consts.TIMES_DAY_TITLES_FILE)
    times_day_array = load_json_from_file(consts.TIMES_DAY_FILE_FORMAT.format(
        place_number=place_number,
        year_number=year,
        month_number=month_number
    ))
    if times_day_titles and times_day_array:
        return times_day_titles, times_day_array
    chrome_driver = driver or webdriver.Chrome()
    chrome_driver.get(consts.YESHIVA_TIMES_URL_FORMAT.format(
        month_number=month_number,
        year=year,
        place_number=place_number
    ))
    chrome_driver.maximize_window()
    smaller_font_size_element = chrome_driver.find_element_by_css_selector(consts.FONT_SMALLER_SIZE_CSS_SELECTOR)
    for i in range(consts.TIMES_TO_FONT_SIZE_SMALLER):
        smaller_font_size_element.click()
    chrome_driver.execute_script(consts.SCROLLING_DOWN_SCRIPT)
    times_day_table = chrome_driver.find_element_by_class_name(consts.TIMES_TABLE_CLASS_NAME)
    times_day_table_body = times_day_table.find_element_by_css_selector(consts.TABLE_BODY_CSS_SELECTOR)
    times_day_titles_element, *times_day_table_rows = times_day_table_body.find_elements_by_css_selector(
        consts.TABLE_ROW_CSS_SELECTOR
    )
    times_day_titles = times_day_titles or [cell_element.text for cell_element in
                                            times_day_titles_element.find_elements_by_css_selector(
                                                consts.TABLE_CELL_CSS_SELECTOR
                                            )]

    times_day_array = times_day_array or []
    if not times_day_array:
        for times_row in times_day_table_rows:
            times_day_array.append([
                _get_rid_of_quotes(times_cell.text) for times_cell in times_row.find_elements_by_css_selector(
                    consts.TABLE_CELL_CSS_SELECTOR
                )])

    if not driver:
        chrome_driver.close()
    return times_day_titles, times_day_array


@lru_cache(maxsize=10)
def get_shabat_times(place_number: int, year: int, driver=None) -> Tuple[List[str], List[List[str]]]:
    shabat_titles = load_json_from_file(consts.SHABAT_SPECIAL_TIMES_TITLES_FILE)
    shabat_array = load_json_from_file(consts.SHABAT_SPECIAL_TIMES_FILE_FORMAT.format(
        place_number=place_number,
        year_number=year
    ))
    if shabat_titles and shabat_array:
        return shabat_titles, shabat_array
    chrome_driver = driver or webdriver.Chrome()
    chrome_driver.get(consts.YESHIVA_SHABAT_URL_FORMAT.format(place_number=place_number, year=year))
    chrome_driver.maximize_window()
    chrome_driver.execute_script(consts.SCROLLING_DOWN_SHABAT_SCRIPT)
    shabat_table = chrome_driver.find_element_by_id(consts.TIMES_TABLE_CLASS_NAME)
    shabat_table_body = shabat_table.find_element_by_css_selector(consts.TABLE_BODY_CSS_SELECTOR)
    shabat_titles_element, *shabat_table_rows = shabat_table_body.find_elements_by_css_selector(
        consts.TABLE_ROW_CSS_SELECTOR
    )
    shabat_titles = shabat_titles or [cell_element.text for cell_element in
                                      shabat_titles_element.find_elements_by_css_selector(
                                          consts.TABLE_CELL_CSS_SELECTOR
                                      )]
    shabat_array = shabat_array or []

    if not shabat_array:
        for times_row in shabat_table_rows:
            shabat_array.append([
                _get_rid_of_quotes(times_cell.text) for times_cell in times_row.find_elements_by_css_selector(
                    consts.TABLE_CELL_CSS_SELECTOR
                )])

    if not driver:
        chrome_driver.close()
    return shabat_titles, shabat_array


def convert_to_time_of_day(titles, times_of_days):
    return [TimeOfDay(time_of_day, titles) for time_of_day in times_of_days]


def _get_rid_of_quotes(text: str) -> str:
    return text.replace('"', '').replace("'", '')


def is_year_leaped(year: int) -> bool:
    return year % consts.LEAP_YEAR_MODULO_NUMBER in consts.LEAP_YEARS_MODULO


def convert_month_to_month_number(month: str, year: int) -> int:
    if is_year_leaped(year):
        return consts.LEAP_YEAR_MONTH_NUMBERS[month]
    return consts.NON_LEAP_YEAR_MONTH_NUMBERS[month]
