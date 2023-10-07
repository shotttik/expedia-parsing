from selenium.webdriver.common.by import By

from Locators.base_locators import BasePageLocators


class SearchPageLocators(BasePageLocators):
    RESULT_COUNT = (
        By.XPATH, "//div[contains(@class,'results-count')]")

    CHEAPEST_BTN = (By.XPATH, "//div[@aria-label='Cheapest']")

    SLIDER_CONTAINER = (
        By.XPATH, "//div[contains(@class, 'G1rD-toggle-section ')]//div[contains(@class,'slider')]")

    SLIDER_TRACK = (
        By.XPATH, SLIDER_CONTAINER[1] + "//span[contains(@class, 'track')]")

    SLIDER_START_BTN = (
        By.XPATH, SLIDER_CONTAINER[1] + "//span[@aria-label='Take-off 1']")

    TIMES_FILTER_RESET_BTN = (
        By.XPATH, "//div[contains(@aria-label, 'Reset all values for Times filter') and not(@aria-disabled)]")

    STOPS_FILTER_RESET_BTN = (
        By.XPATH, "//div[contains(@aria-label, 'Reset all values for Stops filter')]")

    TIMES_CONTAINER = (
        By.XPATH, "//div[contains(@class, 'G1rD-toggle-section')]//div[2]")
