from Core.webdriver import Browser
from Exceptions.InputTextExceptions import InputTextRequiredException
from Exceptions.VerifyExceptions import VerifyException
from .base_page import BasePage
from Locators.home_locators import HomePageLocators
from logger import CustomLogger
import pandas as pd
LOGGER = CustomLogger.get_logger(__name__)


class HomePage(BasePage):

    def __init__(self, wait_time):
        LOGGER.info("Initializing HomePage Class.")
        super().__init__(wait_time)

    def verify_page(self):
        result: bool = self.verify_page_by_element(HomePageLocators.HOME_ICON)
        if not result:
            raise VerifyException()

    def check_direct_flights(self, check: int):
        LOGGER.info("Checking Direct flights checkbox.")
        if not check:
            return
        self.do_click_with_action(HomePageLocators.DIRECT_INPUT)

    def change_to_one_way_flight(self, return_date):
        LOGGER.info("Checking One way flights.")
        if not return_date:
            return
        self.do_click_with_action(HomePageLocators.ONE_WAY_TAB_BUTTON)

    def fill_origin_input(self, text: str):
        LOGGER.info("Filling origin input with text")
        if not text:
            raise InputTextRequiredException
        self.do_click_with_action(HomePageLocators.ORIGIN_BTN)
        self.send_keys_with_action(HomePageLocators.ORIGIN_INPUT, text)
        self.wait_elements_to_appear(
            HomePageLocators.ORIGIN_SELECT_RESULT_ITEMS)
        self.do_click_with_action(
            HomePageLocators.ORIGIN_SELECT_RESULT_ITEM)

    def fill_destination_input(self, text: str):
        LOGGER.info("Filling destination input with text")
        if not text:
            raise InputTextRequiredException
        self.do_click_with_action(HomePageLocators.DESTINATION_BTN)
        self.send_keys_with_action(HomePageLocators.DESTINATION_INPUT, text)
        self.wait_elements_to_appear(
            HomePageLocators.DESTINATION_SELECT_RESULT_ITEMS)
        self.do_click_with_action(
            HomePageLocators.DESTINATION_SELECT_RESULT_ITEM)

    def configure_search_controls(self, flight_df: pd.DataFrame):
        LOGGER.info("Started configuration of search controls.")
        self.change_to_one_way_flight(flight_df["Return"])
        self.fill_origin_input(flight_df["From"])
        self.fill_destination_input(flight_df["To"])

    def go_to_search_page(self):
        LOGGER.info("Clicking to search button")
        self.do_click_with_action(HomePageLocators.SEARCH_BTN)
