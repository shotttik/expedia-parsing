from selenium.webdriver.common.by import By

from Locators.base_locators import BasePageLocators


class SearchPageLocators(BasePageLocators):
    SORT_FILTER_DROPDOWN = (
        By.XPATH, "//select[@id='sort-filter-dropdown-SORT']")

    DIRECT_FLIGHT_CHECKBOX = (
        By.XPATH, "//input[contains(@id, 'NUM_OF_STOPS-0')]")

    ORIGIN_BTN = (
        By.XPATH, "//button[@data-stid='typeahead-originInput-0-menu-trigger']")

    ORIGIN_INPUT = (
        By.XPATH, "//input[@id='typeahead-originInput-0']")

    ORIGIN_RESULT_ITEM_BTN = (
        By.XPATH, "//button[@data-stid='typeahead-originInput-0-result-item-button']")

    DESTINATION_BTN = (
        By.XPATH, "//button[@data-stid='typeahead-destinationInput-0-menu-trigger']")

    DESTINATION_INPUT = (
        By.XPATH, "//input[@id='typeahead-destinationInput-0']")

    DESTINATION_RESULT_ITEM_BTN = (
        By.XPATH, "//button[@data-stid='typeahead-destinationInput-0-result-item-button']")

    DATE_PICKER_BTN = (By.XPATH, "//button[@data-stid='open-date-picker']")

    FLIGHT_TYPE_MENU_BTN = (
        By.XPATH, "//button[@data-test-id='flights-trip-type-options-toggle']")

    FLIGHT_TYPE_BTN = (
        By.XPATH, "//span[@class='uitk-menu-list-item-label' and contains(text(), 'One way')]")

    # after date picker opened
    DATE_SELECTED = (
        By.XPATH, "//button[contains(@class, 'uitk-date-picker-day') and contains(@class, 'selected')]")
