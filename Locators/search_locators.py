from selenium.webdriver.common.by import By

from Locators.base_locators import BasePageLocators


class SearchPageLocators(BasePageLocators):
    RESULT_COUNT = (
        By.XPATH, "//div[contains(@class,'results-count')]")

    TRIP_TYPE_BTN = (By.XPATH, "//div[contains(@class, 'NITa-trip-type ')]")

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
        By.XPATH, "//div[contains(@aria-label, 'Reset all values for Stops filter') and not(@aria-disabled)]")

    NONSTOPS_LABEL = (By.XPATH, "//label[contains(@id, 'stops-0')]")

    NONSTOPS_ONLY_BTN = (By.XPATH, "//div[contains(@aria-label, 'Nonstop')]")

    TIMES_CONTAINER = (
        By.XPATH, "//div[contains(@class, 'G1rD-toggle-section')]//div[2]")

    @staticmethod
    def FLIGHT_TYPE_BTN(oneway):
        if oneway:
            attr_for = 'oneway'
        else:
            attr_for = 'roundtrip'
        return (By.XPATH, f"//span//label[@for='{attr_for}']")

    # after opening search form dialog
    UPDATE_BUTTON = (
        By.XPATH, "//div[contains(@class, 'zEiP-submit')]//button[contains(@class, 'animation-search')]")
