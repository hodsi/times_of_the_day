from selenium import webdriver

import consts


def get_times_as_titles_and_array(month, year, place):
    with webdriver.Chrome() as chrome_driver:
        chrome_driver.get(consts.YESHIVA_TIMES_URL_FORMAT.format(
            month=month,
            year=year,
            place_number=consts.PLACE_DICT[place]
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

        times_day_array = []

        for times_row in times_day_table_rows:
            times_day_array.append([
                _get_rid_of_quotes(times_cell.text) for times_cell in times_row.find_elements_by_css_selector(
                    consts.TABLE_CELL_CSS_SELECTOR
                )])
    return times_day_titles, times_day_array


def _get_rid_of_quotes(text: str) -> str:
    return text.replace('"', '').replace("'", '')


def _convert_month_to_month_number(month: str, year: int) -> int:
    if year % consts.LEAP_YEAR_MODULO_NUMBER in consts.LEAP_YEARS_MODULO:
        return consts.LEAP_YEAR_MONTH_NUMBERS[month]
    return consts.NON_LEAP_YEAR_MONTH_NUMBERS[month]
