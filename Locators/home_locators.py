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

    DIRECT_FLIGHT_INPUT = (
        By.XPATH, "//input[contains(@id, 'direct-flight-toggle')]")

    SEARCH_BTN = (By.XPATH, "//button[contains(@class, 'animation-search')]")

    ACCEPT_COOKIES_BTN = (By.XPATH, "//div[@class='RxNS-button-content']")

    REDIRECT_LINK = (By.XPATH, "//a[contains(@class, 'redirect-link')]")
