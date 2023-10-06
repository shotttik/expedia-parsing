from selenium.webdriver.common.by import By

from Locators.base_locators import BasePageLocators


class HomePageLocators(BasePageLocators):

    HOME_TITLE = (
        By.XPATH, "//h2[@class='title dark']")

    DRAWER_CLOSE_BTN = (By.XPATH, "//button[@aria-label='Close drawer']")

    TRIP_TYPE_MENU_SPAN = (
        By.XPATH, "//div[contains(@aria-label, 'Trip type')]//span")

    @staticmethod
    def FLIGHT_TYPE_BTN(one_way):
        if one_way:
            id = "oneway"
        else:
            id = "roundtrip"
        return (By.XPATH, f"//li[@id='{id}']")

    ORIGIN_CLOSE_BTN = (
        By.XPATH, "//div[contains(@class, 'zEiP-origin')]//div[@class='vvTc-item-close']")

    ORIGIN_INPUT = (By.XPATH, "//div[contains(@class, 'zEiP-origin')]//input")

    ORIGIN_SELECT_ITEM = (
        By.XPATH, "//ul[@id='flight-origin-smarty-input-list']//li[1]")

    DESTINATION_CLOSE_BTN = (
        By.XPATH, "//div[contains(@class, 'zEiP-destination')]//div[@class='vvTc-item-close']")

    DESTINATION_INPUT = (
        By.XPATH, "//div[contains(@class, 'zEiP-destination')]//input")

    DESTINATION_SELECT_ITEM = (
        By.XPATH, "//ul[@id='flight-destination-smarty-input-list']//li[1]")

    DIRECT_FLIGHT_INPUT = (
        By.XPATH, "//input[contains(@id, 'direct-flight-toggle')]")

    START_DATE_SPAN = (
        By.XPATH, "//span[@class='sR_k-date' and contains(@aria-label, 'Start')]//span[@class='sR_k-value']")

    NEXT_MONTH_BTN = (By.XPATH, "//button[@aria-label='Next Month']")

    PREVIOUS_MONTH_BTN = (By.XPATH, "//button[@aria-label='Previous month']")

    MONTH_NAME = (By.XPATH, "//div[@class='wHSr-monthName']")

    SEARCH_BTN = (By.XPATH, "//button[contains(@class, 'animation-search')]")

    @staticmethod
    def DATE_PICKER_DAY_BTN(date_str):
        return (
            By.XPATH, f"//div[@aria-label='{date_str}' and not(contains(@class, 'mkUa-isHidden'))]")
