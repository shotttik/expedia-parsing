from selenium.webdriver.common.by import By

from Locators.base_locators import BasePageLocators


class HomePageLocators(BasePageLocators):

    HOME_ICON = (
        By.XPATH, "//div[@id='flight-search-form-1']")

    ONE_WAY_TAB_BUTTON = (
        By.XPATH, "//div[@class='uitk-tabs-container']//a[@href='#FlightSearchForm_ONE_WAY']")

    ORIGIN_BTN = (
        By.XPATH, "//button[@data-stid='origin_select-menu-trigger']")

    ORIGIN_INPUT = (By.XPATH, "//input[@id='origin_select']")

    ORIGIN_SELECT_RESULT_ITEMS = (
        By.XPATH, "//ul[@data-stid='origin_select-results']//li"
    )

    ORIGIN_SELECT_RESULT_ITEM = (
        By.XPATH, "//li[@data-stid='origin_select-result-item']//button")

    DESTINATION_BTN = (
        By.XPATH, "//button[@data-stid='destination_select-menu-trigger']")
    DESTINATION_INPUT = (By.XPATH, "//input[@id='destination_select']")

    DESTINATION_SELECT_RESULT_ITEMS = (
        By.XPATH, "//ul[@data-stid='destination_select-results']//li"
    )
    DESTINATION_SELECT_RESULT_ITEM = (
        By.XPATH, "//li[@data-stid='destination_select-result-item']//button"
    )

    DEPARTURE_DATE_PICKER_BTN = (
        By.XPATH, "//button[@id='date_form_field-btn']")

    SEARCH_BTN = (By.XPATH, "//button[@id='search_button']")
