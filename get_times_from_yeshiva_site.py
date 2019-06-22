import json
from functools import lru_cache
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

YESHIVA_TIMES_URL_FORMAT = 'https://www.yeshiva.org.il/calendar/timestable?year={year}&month={month}&place={' \
                           'place_number} '
DICT_JSON_FILE = 'place_dict.json'
TIMES_TABLE_CLASS_NAME = 'holydayTableTimes'
TABLE_BODY_CSS_SELECTOR = 'tbody'
TABLE_ROW_CSS_SELECTOR = 'tr'
TABLE_CELL_CSS_SELECTOR = 'td'
SCROLLING_DOWN_SCRIPT = 'scroll(0, 300);'
FONT_SMALLER_SIZE_CSS_SELECTOR = '[class="font-size small"]'
TIMES_TO_FONT_SIZE_SMALLER = 13


def get_times_as_titles_and_array(month, year, place):
    with webdriver.Chrome() as chrome_driver:
        chrome_driver.get(YESHIVA_TIMES_URL_FORMAT.format(
            month=month,
            year=year,
            place_number=convert_place_to_place_num(place)
        ))
        chrome_driver.maximize_window()
        smaller_font_size_element = chrome_driver.find_element_by_css_selector(FONT_SMALLER_SIZE_CSS_SELECTOR)
        for i in range(TIMES_TO_FONT_SIZE_SMALLER):
            smaller_font_size_element.click()
        chrome_driver.execute_script(SCROLLING_DOWN_SCRIPT)
        times_day_table = chrome_driver.find_element_by_class_name(TIMES_TABLE_CLASS_NAME)
        times_day_table_body = times_day_table.find_element_by_css_selector(TABLE_BODY_CSS_SELECTOR)
        times_day_titles_element, *times_day_table_rows = times_day_table_body.find_elements_by_css_selector(
            TABLE_ROW_CSS_SELECTOR
        )
        times_day_titles = [cell_element.text for cell_element in
                            times_day_titles_element.find_elements_by_css_selector(
                                TABLE_CELL_CSS_SELECTOR
                            )]

        times_day_array = []

        for times_row in times_day_table_rows:
            times_day_array.append([
                get_rid_of_quotes(times_cell.text) for times_cell in times_row.find_elements_by_css_selector(
                    TABLE_CELL_CSS_SELECTOR
                )])
    return times_day_titles, times_day_array


def get_rid_of_quotes(text: str) -> str:
    return text.replace('"', '').replace("'", '')


@lru_cache(maxsize=1)
def _get_place_dict():
    with open(DICT_JSON_FILE) as f:
        return json.load(f)


def convert_place_to_place_num(place):
    place_dict = _get_place_dict()
    return place_dict[place]
