from typing import List

from cachetools.func import lru_cache
from selenium import webdriver

import consts
from time_of_day import TimeOfDay


@lru_cache(maxsize=10)
def get_times_as_time_of_day_list(month_number: int, place_number: int, year: int) -> List[TimeOfDay]:
    with webdriver.Chrome() as chrome_driver:
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
        times_day_titles = [cell_element.text for cell_element in
                            times_day_titles_element.find_elements_by_css_selector(
                                consts.TABLE_CELL_CSS_SELECTOR
                            )]

        time_of_day_array = []

        for times_row in times_day_table_rows:
            time_of_day_array.append(TimeOfDay([
                _get_rid_of_quotes(times_cell.text) for times_cell in times_row.find_elements_by_css_selector(
                    consts.TABLE_CELL_CSS_SELECTOR
                )],
                times_day_titles
            ))
    return time_of_day_array


def get_shabat_times(place_number: int, year: int) -> List[TimeOfDay]:
    with webdriver.Chrome() as chrome_driver:
        chrome_driver.get(consts.YESHIVA_SHABAT_URL_FORMAT.format(place_number=place_number, year=year))
        chrome_driver.maximize_window()
        chrome_driver.execute_script(consts.SCROLLING_DOWN_SHABAT_SCRIPT)
        shabat_table = chrome_driver.find_element_by_id(consts.TIMES_TABLE_CLASS_NAME)
        shabat_table_body = shabat_table.find_element_by_css_selector(consts.TABLE_BODY_CSS_SELECTOR)
        shabat_titles_element, *shabat_table_rows = shabat_table_body.find_elements_by_css_selector(
            consts.TABLE_ROW_CSS_SELECTOR
        )
        shabat_titles = [cell_element.text for cell_element in
                         shabat_titles_element.find_elements_by_css_selector(
                             consts.TABLE_CELL_CSS_SELECTOR
                         )]
        shabat_array = []

        for times_row in shabat_table_rows:
            shabat_array.append(TimeOfDay([
                _get_rid_of_quotes(times_cell.text) for times_cell in times_row.find_elements_by_css_selector(
                    consts.TABLE_CELL_CSS_SELECTOR
                )],
                shabat_titles
            ))

        return shabat_array


def _get_rid_of_quotes(text: str) -> str:
    return text.replace('"', '').replace("'", '')


def is_year_leaped(year: int) -> bool:
    return year % consts.LEAP_YEAR_MODULO_NUMBER in consts.LEAP_YEARS_MODULO


def convert_month_to_month_number(month: str, year: int) -> int:
    if is_year_leaped(year):
        return consts.LEAP_YEAR_MONTH_NUMBERS[month]
    return consts.NON_LEAP_YEAR_MONTH_NUMBERS[month]
