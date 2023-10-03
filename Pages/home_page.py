from Core.webdriver import Browser
from Exceptions.DateExceptions import DepartureDateRequiredException
from Exceptions.InputExceptions import InputTextRequiredException
from Exceptions.VerifyExceptions import VerifyPageException
from .base_page import BasePage
from Locators.home_locators import HomePageLocators
from logger import CustomLogger
import pandas as pd
from selenium.common.exceptions import TimeoutException
from Utils.date_utils import DateUtils
LOGGER = CustomLogger.get_logger(__name__)


class HomePage(BasePage):

    def __init__(self, wait_time):
        LOGGER.info("Initializing HomePage Class.")
        super().__init__(wait_time)

    def verify_page(self):
        result: bool = self.verify_page_by_element(HomePageLocators.HOME_ICON)
        if not result:
            raise VerifyPageException()

    def check_direct_flights(self, check: int):
        LOGGER.info("Checking Direct flights checkbox.")
        if not check:
            return
        self.do_click_with_action(HomePageLocators.DIRECT_INPUT)

    def change_flight_type(self, return_date):
        LOGGER.info("Changing flight way type.")
        # default it already roundtrip
        if return_date:
            return
        self.do_click_with_action(HomePageLocators.ONE_WAY_TAB_BUTTON)

    def open_date_picker(self):
        LOGGER.info("Opening date picker...")
        self.do_click_with_action(HomePageLocators.DEPARTURE_DATE_PICKER_BTN)

    def close_date_picker(self):
        LOGGER.info("Closing date picker...")
        self.do_click_with_action(
            HomePageLocators.DEPART_DATE_DONE_BTN)

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

    def choose_date(self, timestamp):
        LOGGER.info('Choosing departure date.')
        if not timestamp:
            raise DepartureDateRequiredException

        # Format the datetime object as "Tuesday, October 10, 2023"
        # date = DateUtils.timestamp_to_date(timestamp, "%A, %B %d, %Y")
        # Format the timestamp ex. 2023-11-22 00:00:00 object as "22 Oct 2023"
        date = DateUtils.timestamp_to_date(timestamp, "%d %b %Y")
        while True:
            try:
                self.do_click_with_action(
                    HomePageLocators.DEPARTURE_DATE_BTN(date))

                break
            except TimeoutException:
                self.do_click_with_action(HomePageLocators.NEXT_MONTH_BTN)

    def configure_search_controls(self, flight_df: pd.DataFrame):
        LOGGER.info("Started configuration of search controls.")
        self.change_flight_type(flight_df["Return"])
        self.fill_origin_input(flight_df["From"])
        self.fill_destination_input(flight_df["To"])
        self.open_date_picker()
        LOGGER.info(f"DEPARTURE - {flight_df['Depart']}")
        LOGGER.info(f"DEPARTURE - {flight_df['Return']}")
        self.choose_date(flight_df["Depart"])
        if flight_df["Return"]:
            self.choose_date(flight_df["Return"])
        self.close_date_picker()

    def go_to_search_page(self):
        LOGGER.info("Clicking to search button")
        self.do_click_with_action(HomePageLocators.SEARCH_BTN)
